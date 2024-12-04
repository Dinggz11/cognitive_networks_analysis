# 多图多个网络的度频率分布直方图/散点图，正常坐标轴
# 方法不同，但绘制结果差不多，只是优化了一下细节（坐标轴标签、网格线等）
import pandas as pd
import matplotlib.pyplot as plt

number = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight']
suffixes = [2, 3, 4, 5, 6, 7, 8]

# 设置子图的布局
fig, axs = plt.subplots(2, 4, figsize=(15, 8))
# fig.suptitle('Degree Distribution of Networks')

# 遍历每个数据表后缀
for i, suffix in enumerate(suffixes):
    # 读取数据表
    df = pd.read_excel(f'./07output/02-w_{suffix}.xlsx')

    # 统计每个度数的节点数量
    degree_counts = df['degree'].value_counts()

    # 计算合适的 bins 数量
    bins = max(degree_counts.index) - min(degree_counts.index) + 1

    # 获取当前子图的位置
    row = i // 4  # 行数
    col = i % 4   # 列数
    ax = axs[row, col]

    # 绘制度数分布直方图
    ax.hist(df['degree'], bins=bins, color='skyblue', edgecolor='black', density=True, align='mid')

    # 添加标题和标签
    ax.set_title(f'Network {number[i].capitalize()}')
    ax.set_xlabel('k')
    ax.set_ylabel('P(k)')

    # 添加网格
    ax.grid(True)

# 隐藏最后一个子图
axs[1, 3].axis('off')

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 显示图形
plt.show()
