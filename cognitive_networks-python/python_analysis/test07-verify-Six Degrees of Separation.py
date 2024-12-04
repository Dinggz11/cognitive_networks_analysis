import pandas as pd
import networkx as nx


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

    # 计算实际网络的聚类系数和平均路径长度
    if nx.is_connected(G_global):
        real_clustering_coefficient = nx.average_clustering(G_global)
        real_avg_shortest_path_length = nx.average_shortest_path_length(G_global)
        print("Real Network:")
        print(f"Average Shortest Path Length: {real_avg_shortest_path_length:.3f}")
        print(f"Clustering Coefficient: {real_clustering_coefficient:.3f}")

        # 计算实际网络的节点数和边数
        N = len(G_global.nodes)
        n = len(G_global.edges)

        # 使用连接概率法确定 p
        p = 2 * n / (N * (N - 1))

        # 生成 ER 随机图并确保它是连通的
        er_random_graph = nx.erdos_renyi_graph(N, p)
        while not nx.is_connected(er_random_graph):
            er_random_graph = nx.erdos_renyi_graph(N, p)

        # 计算 ER 随机图的特征路径长度和聚集系数
        er_avg_shortest_path_length = nx.average_shortest_path_length(er_random_graph)
        er_clustering_coefficient = nx.average_clustering(er_random_graph)

        # 输出 ER 随机图的特征路径长度和聚集系数
        print(f"Average Shortest Path Length (ER Random Graph): {er_avg_shortest_path_length:.3f}")
        print(f"Clustering Coefficient (ER Random Graph): {er_clustering_coefficient:.3f}")

        print("N:", N)
        print("n:", n)
        # print("p:", p)
        print(f"p: {p:.3f}")
    else:
        print("全局网络不连通，无法计算实际网络的聚类系数和平均路径长度")


if __name__ == "__main__":
    exp_id = 2
    main(exp_id)
