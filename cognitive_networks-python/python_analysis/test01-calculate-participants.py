# total_participants 统计所有参与者人数
# connected_count 统计有创建词汇且连通的参与者人数
# disconnected_count 统计有创建词汇但不连通的参与者人数
# other_count 统计其他参与者人数（没有连接的网络）

# 为每个参与者创建一个网络，边数是否为零的处理，使用nx.is_connected(G)来确定网络是否连通
# 是否有边（有边：进一步判断是否有连通：（完全连通；没完全连通））   （没边）

import pandas as pd
import networkx as nx

# 读取数据
exp_my_words = pd.read_excel('../data/07exp_my_words.xlsx')
exp_my_word_relation = pd.read_excel('../data/07exp_my_word_relation.xlsx')

# 指定初始词汇数量的实验 ID (exp_id=2~8)
exp_id = 2

# 筛选数据
filtered_words = exp_my_words[(exp_my_words['deleted'] == 0) & (exp_my_words['exp_id'] == exp_id)]
filtered_relations = exp_my_word_relation[
    (exp_my_word_relation['deleted'] == 0) & (exp_my_word_relation['exp_id'] == exp_id)]

# 获取所有参与者的 user_id
user_ids = filtered_words['create_user_id'].unique()

# 统计变量
total_participants = len(user_ids)
connected_count = 0
disconnected_count = 0
other_count = 0

# 记录不连通的用户及其创建的词汇
disconnected_users = {}
# 记录连通的用户及其创建的词汇
connected_users = {}

# 对每个参与者构建网络并检查连通性
for user_id in user_ids:
    user_words = filtered_words[filtered_words['create_user_id'] == user_id]
    user_relations = filtered_relations[
        (filtered_relations['from_id'].isin(user_words['id'])) & (filtered_relations['to_id'].isin(user_words['id']))]

    # 创建网络图
    G = nx.Graph()

    # 创建一个 id 到 word 的映射
    id_to_word = dict(zip(user_words['id'], user_words['word']))

    # 添加节点和边到图中
    G.add_nodes_from(user_words['word'])
    edges = [(id_to_word[row['from_id']], id_to_word[row['to_id']]) for index, row in user_relations.iterrows()]
    G.add_edges_from(edges)

    # 打印参与者的词汇网络
    print(f"User ID: {user_id}")
    if G.number_of_edges() > 0:
        print(f"Edges: {G.edges()}")
        if nx.is_connected(G):
            connected_count += 1
            connected_users[user_id] = user_words['word'].tolist()
        else:
            disconnected_count += 1
            disconnected_users[user_id] = user_words['word'].tolist()
    else:
        print("No connections.")
        other_count += 1
        disconnected_users[user_id] = user_words['word'].tolist()
    print("\n")

# 输出统计结果
print(f"Total participants: {total_participants}")
print(f"Participants with connected networks: {connected_count}")
print(f"Participants with disconnected networks: {disconnected_count}")
print(f"Other participants (no connections): {other_count}")

# 输出不连通的用户及其创建的词汇
print("\nDisconnected users and their words:")
for user_id, words in disconnected_users.items():
    print(f"User ID: {user_id}, Words: {', '.join(words)}")

# 输出连通的用户及其创建的词汇
print("\nConnected users and their words:")
for user_id, words in connected_users.items():
    print(f"User ID: {user_id}, Words: {', '.join(words)}")