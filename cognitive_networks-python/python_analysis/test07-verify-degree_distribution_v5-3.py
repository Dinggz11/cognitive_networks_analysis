# 多图多个网络的度频率分布直方图/散点图，双对数坐标/半对数坐标
# 用具有度k的节点数比总节点数去计算频率，双对数坐标图；scipy.optimize.curve_fit 函数来进行拟合
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

number = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight']
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

    # 计算频率
    total_nodes = len(df)
    degree_freq = degree_counts / total_nodes

    # 获取当前子图的位置
    row = i // 4  # 行数
    col = i % 4   # 列数
    ax = axs[row, col]

    # 绘制双对数坐标图
    ax.scatter(degree_freq.index, degree_freq.values, color='skyblue', s=8)

    # 添加标题和标签
    ax.set_title(f'Network {number[i].capitalize()}')
    ax.set_xlabel('k')
    ax.set_ylabel('P(k)')

    # 设置坐标轴为双对数坐标轴/半对数坐标轴(比如 设置y轴为对数坐标轴，x轴保持线性:把这句注释掉 ax.set_xscale('log') )
    # ax.set_xscale('log')
    ax.set_yscale('log')

    # 对数变换
    log_degrees = np.log(degree_freq.index)
    log_freqs = np.log(degree_freq.values)

    # 使用最小二乘法拟合数据
    popt, _ = curve_fit(power_law, degree_freq.index, degree_freq.values, p0=[1.5])

    # 输出拟合得到的指数a的值
    print(f"Network {number[i].capitalize()}: Exponent a =", popt[0])

    # 绘制拟合直线
    x_fit = np.linspace(min(degree_freq.index), max(degree_freq.index), 100)
    y_fit = power_law(x_fit, *popt)
    ax.plot(x_fit, y_fit, color='red', linestyle='--', label=f'Fit, a={popt[0]:.2f}')
    ax.legend()

    # # 添加网格
    # ax.grid(True)

# 隐藏最后一个子图
axs[1, 3].axis('off')

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 显示图形
plt.show()
