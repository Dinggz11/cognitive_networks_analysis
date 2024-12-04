# 多图多个网络的度频率分布直方图/散点图，正常坐标轴
import pandas as pd
import matplotlib.pyplot as plt

number = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight']
suffixes = [2, 3, 4, 5, 6, 7, 8]

# 设置子图的布局
fig, axs = plt.subplots(2, 4, figsize=(15, 8))
fig.suptitle('Degree Distribution of Networks')

# 遍历每个数据表后缀
for i, suffix in enumerate(suffixes):
    # 读取数据表
    df = pd.read_excel(f'./07output/02-w_{suffix}.xlsx')

    # 统计每个度数的节点数量
    degree_counts = df['degree'].value_counts()

    # 计算每个度数所占比例
    total_nodes = len(df)
    degree_probabilities = degree_counts / total_nodes

    # 计算子图的位置
    row = i // 4
    col = i % 4

    # 在指定位置绘制子图
    axs[row, col].bar(degree_probabilities.index, degree_probabilities)
    # axs[row, col].plot(degree_probabilities.index, degree_probabilities, marker='o', linestyle='-')
    axs[row, col].set_title(f'Network {number[i].capitalize()}')

# 隐藏最后一个子图
axs[1, 3].axis('off')

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 显示图形
plt.show()
