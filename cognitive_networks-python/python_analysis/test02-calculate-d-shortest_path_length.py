import pandas as pd
import networkx as nx
import itertools


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


def compute_shortest_path_lengths(G):
    """计算全局网络中任意一对词汇节点之间的最短路径长度并保存到Excel"""
    words = list(G.nodes())
    shortest_path_length = []

    for word1, word2 in itertools.combinations(words, 2):
        try:
            length = nx.shortest_path_length(G, source=word1, target=word2)
            shortest_path_length.append({'word1': word1, 'word2': word2, 'shortest_path_length': length})
        except nx.NetworkXNoPath:
            shortest_path_length.append({'word1': word1, 'word2': word2, 'shortest_path_length': float('inf')})

    shortest_path_length_df = pd.DataFrame(shortest_path_length)
    return shortest_path_length_df


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

    # 计算并保存最短路径长度
    shortest_path_length_df = compute_shortest_path_lengths(G_global)
    shortest_path_output_filename = f'./07output/02-shortest_path_length_{exp_id}.xlsx'
    shortest_path_length_df.to_excel(shortest_path_output_filename, index=False)


if __name__ == "__main__":
    exp_id = 2
    main(exp_id)
