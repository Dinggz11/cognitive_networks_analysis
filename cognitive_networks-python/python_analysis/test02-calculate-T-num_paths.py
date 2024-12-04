import pandas as pd
import networkx as nx
import itertools
from tqdm import tqdm  # 进度条库


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


def calculate_num_paths(G, cutoff=8):
    """计算全局网络中任意一对节点之间的路径数量，cutoff=8，显示进度条"""
    nodes = list(G.nodes())
    num_paths = []

    # 使用 tqdm 显示进度条，迭代每一对节点
    for word1, word2 in tqdm(itertools.combinations(nodes, 2), total=len(nodes) * (len(nodes) - 1) // 2,
                             desc="Calculating paths"):
        paths_count = len(list(nx.all_simple_paths(G, source=word1, target=word2, cutoff=cutoff)))
        num_paths.append({'word1': word1, 'word2': word2, 'num_paths': paths_count})

    return pd.DataFrame(num_paths)


def main(exp_ids):
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

        if nx.is_connected(G_global):
            # 计算每对节点之间的路径数量
            num_paths_df = calculate_num_paths(G_global, cutoff=8)
            output_file = f'./07output/02-num_paths_cutoff8_{exp_id}.xlsx'
            num_paths_df.to_excel(output_file, index=False)
            print(f"Saved number of paths for exp_id {exp_id} to {output_file}")
        else:
            print("全局网络不连通，无法计算路径数量")


if __name__ == "__main__":
    # exp_ids = [2, 3, 4, 5, 6, 7, 8]
    exp_ids = [2]
    main(exp_ids)
