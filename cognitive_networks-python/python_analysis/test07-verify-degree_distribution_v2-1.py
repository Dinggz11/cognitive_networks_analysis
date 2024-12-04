# 多图多网络 概率密度函数PDF
import powerlaw
import matplotlib.pyplot as plt
import pandas as pd

suffixes = ['2', '3', '4', '5', '6', '7', '8']
numbers = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight']

# 设置子图的布局
fig, axs = plt.subplots(2, 4, figsize=(15, 8))
# fig.suptitle('Degree Distribution and Power Law Fit of Networks')

# 遍历每个数据表后缀
for i, suffix in enumerate(suffixes):
    # 读取数据表
    df = pd.read_excel(f'./07output/02-w_{suffix}.xlsx')

    # 提取度数数据
    degrees = df['degree']

    # 拟合度分布
    fit = powerlaw.Fit(degrees, discrete=True)

    # 计算子图的位置
    row = i // 4
    col = i % 4

    # 在指定位置绘制度分布图和拟合结果
    fit.plot_pdf(color='b', linewidth=2, ax=axs[row, col])
    fit.power_law.plot_pdf(color='r', linestyle='--', ax=axs[row, col])
    axs[row, col].set_xscale('log')
    axs[row, col].set_yscale('log')
    axs[row, col].set_title(f'Network {numbers[i].capitalize()}')

    # 打印拟合的结果 具有拟合的参数alpha及其标准误差sigma
    print(f"Network {numbers[i].capitalize()}:")
    print(f"  Power law alpha = {fit.power_law.alpha:.2f}, sigma = {fit.power_law.sigma:.2f}")
    print(f"  Kolmogorov-Smirnov statistic: {fit.D:.2f}")

    # 使用统计测试 Kolmogorov-Smirnov 检验
    R, p = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True) # 幂律和指数律
    print(f"  Kolmogorov-Smirnov statistic (power law vs exponential): {R:.2f}, p-value: {p:.4f}")
    print(f"  Kolmogorov-Smirnov statistic (power law vs exponential): {R}, p-value: {p}")

    # 根据结果判断更适合的分布
    if p < 0.05:
        if R > 0:
            print("  Result: Power law distribution is better fitting than exponential distribution.")
        else:
            print("  Result: Exponential distribution is better fitting than power law distribution.")
    else:
        print("  Result: No strong evidence to prefer one distribution over the other.")

    # 可选：比较幂律分布和截断幂律分布
    # R2, p2 = fit.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)
    # print(f"  Kolmogorov-Smirnov statistic (power law vs truncated power law): {R2:.2f}, p-value: {p2:.4f}")

# 隐藏最后一个子图
axs[1, 3].axis('off')

# 调整布局
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 显示图形
plt.show()
