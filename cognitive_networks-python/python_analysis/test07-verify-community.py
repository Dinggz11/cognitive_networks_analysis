import pandas as pd
import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt

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

    return G


def detect_communities_louvain_and_visualize(G):
    """使用Louvain算法进行社团检测，绘制网络并计算模块度"""
    # 使用Louvain算法检测社团
    partition = community_louvain.best_partition(G)

    # 将社团信息添加到节点属性中
    nx.set_node_attributes(G, partition, 'community')

    # 输出每个节点的社团归属
    print("Community assignment for each node:", nx.get_node_attributes(G, 'community'))

    # 获取节点的社团信息
    community_assignment = nx.get_node_attributes(G, 'community')

    # 节点大小设置，与度关联
    node_size = [G.degree(i)**1 * 30 for i in G.nodes()]

    # 调整社团颜色映射
    cmap = plt.cm.Set1
    colors = [cmap(i % 9) for i in partition.values()]

    # 绘制网络图，按照社团用不同颜色标记节点
    plt.figure(figsize=(10, 8))
    # 布局算法
    pos = nx.kamada_kawai_layout(G)  # 使用kamada_kawai_layout布局，效果较好
    nx.draw(G, pos, with_labels=True, font_size=8, node_color=colors, cmap=cmap, node_size=node_size, edge_color='gray')
    plt.show()

    # 计算模块度
    modularity = community_louvain.modularity(partition, G)
    print("Modularity:", modularity)

    # 将社团信息打印到控制台
    communities = [{'word': word, 'community': community_id} for word, community_id in partition.items()]
    for community in communities:
        print(f"Word: {community['word']}, Community: {community['community']}")


def main(exp_id):
    filtered_words, filtered_relations = load_and_filter_data(exp_id)
    user_ids = filtered_words['create_user_id'].unique()

    G_global = nx.Graph()
    connected_count = 0

    for user_id in user_ids:
        G = build_user_network(user_id, filtered_words, filtered_relations)

        if G.number_of_edges() > 0 and nx.is_connected(G):
            connected_count += 1
            G_global = nx.compose(G_global, G)

    # 输出连通的参与者数量
    print(f"Number of participants with connected networks: {connected_count}")

    # Louvain社区检测及可视化
    detect_communities_louvain_and_visualize(G_global)


if __name__ == "__main__":
    exp_id = 2
    main(exp_id)
