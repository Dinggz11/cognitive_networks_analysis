import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 设置matplotlib使用的字体，确保包含所需字符
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取两个 Excel 表格数据
exp_my_words = pd.read_excel('../data/07exp_my_words.xlsx')
exp_my_word_relation = pd.read_excel('../data/07exp_my_word_relation.xlsx')

exp_id = 5
filtered_words = exp_my_words[(exp_my_words['deleted'] == 0) & (exp_my_words['exp_id'] == exp_id)]
filtered_relations = exp_my_word_relation[(exp_my_word_relation['deleted'] == 0) & (exp_my_word_relation['exp_id'] == exp_id)]

# 获取所有参与者的 user_id
user_ids = filtered_words['create_user_id'].unique()

# 创建一个全局无向图
G_global = nx.Graph()

# 统计变量
total_participants = len(user_ids)
connected_count = 0
disconnected_count = 0
other_count = 0

# 记录不连通的用户及其创建的词汇
disconnected_users = {}

# 对每个参与者构建网络并检查连通性
for user_id in user_ids:
    user_words = filtered_words[filtered_words['create_user_id'] == user_id]
    user_relations = filtered_relations[
        (filtered_relations['from_id'].isin(user_words['id'])) &
        (filtered_relations['to_id'].isin(user_words['id']))
    ]

    # 创建网络图
    G = nx.Graph()

    # 创建一个 id 到 word 的映射
    id_to_word = dict(zip(user_words['id'], user_words['word']))

    # 添加节点和边到图中
    G.add_nodes_from(user_words['word'])
    edges = [(id_to_word[row['from_id']], id_to_word[row['to_id']]) for _, row in user_relations.iterrows()]
    G.add_edges_from(edges)

    # 打印参与者的词汇网络
    # print(f"User ID: {user_id}")
    if G.number_of_edges() > 0:
        # print(f"Edges: {G.edges()}")
        if nx.is_connected(G):
            connected_count += 1
            # 将连通的词汇网络添加到全局图 G_global 中
            G_global = nx.compose(G_global, G)
        else:
            disconnected_count += 1
            disconnected_users[user_id] = user_words['word'].tolist()
    else:
        # print("No connections.")
        other_count += 1
        disconnected_users[user_id] = user_words['word'].tolist()
    # print("\n")

# # 输出统计结果
# print(f"Total participants: {total_participants}")
# print(f"Participants with connected networks: {connected_count}")
# print(f"Participants with disconnected networks: {disconnected_count}")
# print(f"Other participants (no connections): {other_count}")
#
# # 输出不连通的用户及其创建的词汇
# print("\nDisconnected users and their words:")
# for user_id, words in disconnected_users.items():
#     print(f"User ID: {user_id}, Words: {', '.join(words)}")

# 计算并输出全局图的基本网络属性
num_nodes = G_global.number_of_nodes()
num_edges = G_global.number_of_edges()
average_degree = sum(dict(G_global.degree()).values()) / num_nodes if num_nodes > 0 else 0

print("\nGlobal Network Statistics:")
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")
print(f"Average degree: {average_degree:.2f}")

# 绘制全局网络图
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G_global)
nx.draw(G_global, pos, with_labels=True, node_size=500, node_color='skyblue', font_weight='bold', alpha=0.8)
plt.title('Global Network Graph')
plt.show()