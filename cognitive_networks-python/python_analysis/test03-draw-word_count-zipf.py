import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import matplotlib as mpl

# 设置默认字体为'Times New Roman'
mpl.rcParams['font.family'] = 'Times New Roman'

suffixes = ['2', '3', '4', '5', '6', '7', '8']
numbers = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight']

# 设置子图的布局
fig, axs = plt.subplots(2, 4, figsize=(15, 8))

# 存储每个数据集的结果
slope_vals = []
pearson_coeffs = []
r_squared_vals = []
rmse_vals = []

# 遍历每个数据表后缀
for i, suffix in enumerate(suffixes):
    # 读取数据表
    df = pd.read_excel(f'./07output/02-word_count_{suffix}.xlsx')
    word_count = df['word_count']
    rank = df['rank_2']

    # 计算子图的位置
    row = i // 4
    col = i % 4

    # 在指定位置绘制子图,绘制双对数图
    color = next(axs[row, col]._get_lines.prop_cycler)['color']
    axs[row, col].loglog(rank, word_count, marker='o', markersize=3, linestyle='None', label='Data', color=color)
    axs[row, col].set_title(f'Network {numbers[i].capitalize()}')
    axs[row, col].set_xlabel('log(Rank $\it{i}$)')
    axs[row, col].set_ylabel('log(Word Count $d_i$)')

    # 进行直线拟合
    coeffs = np.polyfit(np.log(rank), np.log(word_count), 1)
    fitted_line = np.exp(np.polyval(coeffs, np.log(rank)))
    axs[row, col].loglog(rank, fitted_line, color=color, linestyle='-', label='Linear regression fit')

    # 添加理论上期望的齐夫定律的直线
    axs[row, col].plot(rank, np.exp(-np.log(rank)), 'purple')

    # 在期望的齐普夫定律的直线旁边显示内容
    axs[row, col].text(0.4, 0.4, r"$d_{i} \sim \frac{1}{i}$", transform=axs[row, col].transAxes, fontsize=10, color='purple')

    # 显示图例
    axs[row, col].legend(loc='lower left')

    # 存储拟合直线的斜率
    slope_vals.append(coeffs[0])

    # 计算Pearson相关系数
    pearson_coeff, _ = pearsonr(np.log(rank), np.log(word_count))
    pearson_coeffs.append(pearson_coeff)

    # 计算R^2
    r_squared = r2_score(np.log(word_count), np.log(fitted_line))
    r_squared_vals.append(r_squared)

    # 计算均方根误差(RMSE)
    rmse = np.sqrt(mean_squared_error(np.log(word_count), np.log(fitted_line)))
    rmse_vals.append(rmse)

# 打印结果
for i, suffix in enumerate(suffixes):
    print(f"Network {numbers[i].capitalize()}: Slope: {slope_vals[i]:.2f}, Pearson coefficient: {pearson_coeffs[i]:.2f}, R^2: {r_squared_vals[i]:.2f}, RMSE: {rmse_vals[i]:.2f}")

# 隐藏最后一个子图
axs[1, 3].axis('off')

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 显示图形
plt.show()
