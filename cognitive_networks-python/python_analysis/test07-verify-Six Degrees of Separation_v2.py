# 相比test07-verify-Six Degrees of Separation.py增加计算 Pearson 相关系数部分
# 计算的是样本量为7个词汇网络的Pearson 相关系数部分
import pandas as pd
import networkx as nx
from scipy.stats import pearsonr


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


def main(exp_ids):
    clustering_coefficients = []
    path_lengths = []

    for exp_id in exp_ids:
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
        print(f"Experiment ID: {exp_id}")
        print(f"Number of participants with connected networks: {connected_count}")

        # 计算实际网络的聚类系数和平均路径长度
        if nx.is_connected(G_global):
            real_clustering_coefficient = nx.average_clustering(G_global)
            real_avg_shortest_path_length = nx.average_shortest_path_length(G_global)
            print("Real Network:")
            print(f"Average Shortest Path Length: {real_avg_shortest_path_length:.3f}")
            print(f"Clustering Coefficient: {real_clustering_coefficient:.3f}")

            clustering_coefficients.append(real_clustering_coefficient)
            path_lengths.append(real_avg_shortest_path_length)
        else:
            print("全局网络不连通，无法计算实际网络的聚类系数和平均路径长度")

    # 计算 Pearson 相关系数
    if len(clustering_coefficients) > 1 and len(path_lengths) > 1:
        correlation, p_value = pearsonr(clustering_coefficients, path_lengths)
        print(f"Pearson Correlation Coefficient: {correlation:.2f}")
        print(f"P-value: {p_value:.3f}")

        # 获取有效数据点的数量和计算自由度
        n = len(clustering_coefficients)  # 样本量是有效的特征对的数量
        df = n - 2  # 自由度为样本量减去 2
        print("样本量 n:", n)
        print("自由度 df:", df)

        # 判断 p 值的显著性
        if p_value < 0.001:
            p_str = "<0.001"
        elif p_value < 0.01:
            p_str = "<0.01"
        elif p_value < 0.05:
            p_str = "<0.05"
        else:
            p_str = f"={p_value:.3f}"

        # 打印结果
        print(
            f"Knowledge networks exhibit small-world structure. We find a negative Pearson correlation between the average clustering coefficient and the characteristic path length (r({df})={correlation:.2f}, p{p_str}), such that people high in clustering tend to have short path lengths.")
    else:
        print("Not enough data to compute Pearson correlation.")


if __name__ == "__main__":
    exp_ids = [2, 3, 4, 5, 6, 7, 8]
    main(exp_ids)
