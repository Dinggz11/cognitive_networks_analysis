# 单个网络的度分布频率直方图
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取 Excel 文件
file_path = './07output/02-w_8.xlsx'
df = pd.read_excel(file_path)

# 提取度数数据
degrees = df['degree']

# 绘制度分布图
plt.figure(figsize=(10, 6))
# 选择合适的 bins 数量
bins = max(degrees) - min(degrees) + 1
# 设置 align='mid' 以确保每个柱子的中心对准横轴整数刻度
plt.hist(degrees, bins=bins, color='skyblue', edgecolor='black', density=True, align='mid')
# 使用对数坐标
# plt.xscale('log')
# plt.yscale('log')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Probability')
plt.grid(True)
plt.show()
