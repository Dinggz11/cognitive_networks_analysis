import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 设置matplotlib使用的字体，确保包含所需字符
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


def load_and_filter_data(exp_id):
    """加载并过滤数据"""
    exp_my_words = pd.read_excel('../data/07exp_my_words.xlsx')
    exp_my_word_relation = pd.read_excel('../data/07exp_my_word_relation.xlsx')

    filtered_words = exp_my_words[(exp_my_words['deleted'] == 0) & (exp_my_words['exp_id'] == exp_id)]
    filtered_relations = exp_my_word_relation[
        (exp_my_word_relation['deleted'] == 0) & (exp_my_word_relation['exp_id'] == exp_id)]

    return filtered_words, filtered_relations


def build_user_network(user_id, filtered_words, filtered_relations):
    """为每个用户构建网络并返回相关数据"""
    user_words = filtered_words[filtered_words['create_user_id'] == user_id]
    user_relations = filtered_relations[
        (filtered_relations['from_id'].isin(user_words['id'])) &
        (filtered_relations['to_id'].isin(user_words['id']))
        ]

    G = nx.Graph()
    id_to_word = dict(zip(user_words['id'], user_words['word']))
    G.add_nodes_from(user_words['word'])
    edges = [(id_to_word[row['from_id']], id_to_word[row['to_id']]) for _, row in user_relations.iterrows()]
    G.add_edges_from(edges)

    return G, user_words


def compute_graph_metrics(G, word_counts):
    """计算全局网络的各种指标并形成结果数据框"""
    # 计算每个词汇的度
    degrees = dict(G.degree())

    # 计算各项指标
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness = nx.betweenness_centrality(G, normalized=False)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)
    clustering = nx.clustering(G)

    # 整合结果
    result = pd.DataFrame(list(degrees.items()), columns=['word', 'degree'])
    result['word_count'] = result['word'].map(word_counts)
    result['degree_centrality'] = result['word'].map(degree_centrality)
    result['closeness_centrality'] = result['word'].map(closeness_centrality)
    result['betweenness'] = result['word'].map(betweenness)
    result['betweenness_centrality'] = result['word'].map(betweenness_centrality)
    result['eigenvector_centrality'] = result['word'].map(eigenvector_centrality)
    result['clustering_coefficient'] = result['word'].map(clustering)

    # 去除重复的词汇
    result = result.drop_duplicates(subset='word')

    # 调整列顺序
    result = result[['word', 'word_count', 'degree', 'degree_centrality', 'closeness_centrality', 'betweenness',
                     'betweenness_centrality', 'eigenvector_centrality', 'clustering_coefficient']]

    return result


def main(exp_id):
    filtered_words, filtered_relations = load_and_filter_data(exp_id)
    user_ids = filtered_words['create_user_id'].unique()

    G_global = nx.Graph()
    word_counts = {}
    disconnected_users = {}
    connected_count = 0

    for user_id in user_ids:
        G, user_words = build_user_network(user_id, filtered_words, filtered_relations)

        if G.number_of_edges() > 0:
            if nx.is_connected(G):
                connected_count += 1
                # 将连通的词汇网络添加到全局图 G_global 中
                G_global = nx.compose(G_global, G)

                # 统计词汇出现次数
                for word in user_words['word']:
                    if word in word_counts:
                        word_counts[word] += 1
                    else:
                        word_counts[word] = 1
            else:
                disconnected_users[user_id] = user_words['word'].tolist()
        else:
            disconnected_users[user_id] = user_words['word'].tolist()

    # 输出连通的参与者数量
    print(f"Number of participants with connected networks: {connected_count}")

    # 计算并保存全局网络的指标
    result = compute_graph_metrics(G_global, word_counts)

    # 动态生成文件名
    output_filename = f'./07output/02-w_{exp_id}.xlsx'
    result.to_excel(output_filename, index=False)

    # # 绘制全局网络图
    # plt.figure(figsize=(10, 8))
    # pos = nx.spring_layout(G_global)
    # nx.draw(G_global, pos, with_labels=True, node_size=500, node_color='skyblue', font_weight='bold', alpha=0.8)
    # plt.title('Global Network Graph')
    # plt.show()


if __name__ == "__main__":
    exp_id = 2
    main(exp_id)
