# 多图多个网络的度k-频数，正常坐标图，散点图/直方图
import pandas as pd
import matplotlib.pyplot as plt

numbers = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight']
suffixes = [2, 3, 4, 5, 6, 7, 8]

# 设置子图的布局
fig, axs = plt.subplots(2, 4, figsize=(15, 8))

# 定义拟合函数
def power_law(x, a):
    return x**(-a)

# 遍历每个数据表后缀
for i, suffix in enumerate(suffixes):
    # 读取数据表
    df = pd.read_excel(f'./07output/02-degree_{suffix}.xlsx')

    # 统计每个度数的节点数量
    degree_counts = df['degree'].value_counts()

    # 获取当前子图的位置
    row = i // 4  # 行数
    col = i % 4   # 列数
    ax = axs[row, col]

    # 绘制度数分布直方图
    ax.bar(degree_counts.index, degree_counts.values, color='skyblue', edgecolor='black')

    # # 绘制度数与频数的散点图
    # ax.scatter(degree_counts.index, degree_counts.values, color='skyblue', s=5)

    # 添加标题和标签
    ax.set_title(f'Network {numbers[i].capitalize()}')
    ax.set_xlabel('Degree')
    ax.set_ylabel('Frequency')

    # # 添加网格
    # ax.grid(True)

# 隐藏最后一个子图
axs[1, 3].axis('off')

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 显示图形
plt.show()

