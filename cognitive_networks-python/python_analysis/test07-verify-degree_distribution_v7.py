# 多图多个网络的度的正常坐标、双对数坐标图、半对数坐标图上秩次图，散点图
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

numbers = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight']
suffixes = [2, 3, 4, 5, 6, 7, 8]

# 设置子图的布局
fig, axs = plt.subplots(2, 4, figsize=(15, 8))

# 遍历每个数据表后缀
for i, suffix in enumerate(suffixes):
    # 读取数据表
    df = pd.read_excel(f'./07output/02-degree_{suffix}.xlsx')
    degree = df['degree']
    rank = df['rank']

    # 获取当前子图的位置
    row = i // 4  # 行数
    col = i % 4   # 列数
    ax = axs[row, col]

    # 绘制双对数坐标图
    ax.scatter(degree, rank, color='skyblue', s=8)

    # 添加标题和标签
    ax.set_title(f'Network {numbers[i].capitalize()}')
    ax.set_xlabel('k')
    ax.set_ylabel('Rank k')

    # 设置坐标轴为对数坐标轴
    # ax.set_xscale('log')
    ax.set_yscale('log')

# 隐藏最后一个子图
axs[1, 3].axis('off')

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 显示图形
plt.show()
