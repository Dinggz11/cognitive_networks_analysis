# 单个图-七个网络的互补累积分布函数CCDF(the complementary cumulative distribution function (CCDF;
# p(X ≥ x)) 折线图
import powerlaw
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

suffixes = [2, 3, 4, 5, 6, 7, 8]
markers = ['o', 's', '^', 'd', 'x', '+', '*']
colors = [(183/255, 83/255, 71/255), (109/255, 47/255, 32/255), (148/255, 181/255, 148/255), (34/255, 75/255, 94/255),
          (224/255, 147/255, 81/255), (223/255, 126/255, 102/255), (237/255, 199/255, 117/255)]

# 创建一个坐标轴
fig, ax = plt.subplots(figsize=(10, 8))

# 存储alpha值
alpha_values = []

# 存储KS检验的p-value值
p_values = []

# 存储KS统计量
KS_stats = []

# 存储alpha标准误差
alpha_errors = []
pdf_alphas = []

# 遍历每个数据表后缀
for i, suffix in enumerate(suffixes):
    # 读取数据表
    df = pd.read_excel(f'./07output/02-degree_{suffix}.xlsx')

    # 提取度数数据
    degrees = df['degree']

    # 统计当前表的节点数量
    node_count = len(degrees)

    # 拟合度分布
    fit = powerlaw.Fit(degrees, discrete=True)

    # 获取alpha标准误差
    alpha_error = fit.power_law.sigma
    pdf_alpha = fit.power_law.alpha
    alpha_errors.append(alpha_error)
    pdf_alphas.append(pdf_alpha)

    # 进行KS检验和p-value检验
    KS_stat, p_value = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    KS_stats.append(KS_stat)
    p_values.append(p_value)

    # 获取拟合的alpha值
    alpha = fit.power_law.alpha - 1
    alpha_values.append(alpha)

    x, y = fit.ccdf()
    ax.plot(x, y, color=colors[i], markersize=8, linestyle='-',
            label=f"N={node_count}, $\\alpha$={alpha:.2f}")

# 输出KS统计量和p-value值
for i, p_value in enumerate(p_values):
    print(f"N={node_count}, KS statistic={KS_stats[i]:.2f}, p-value={p_value:.6f}")

# 添加具有指数α = 2的幂律概率密度函数（PDF）
x_values = np.logspace(0, 1, 100)
y_values = x_values**(-2.40)  # 这里指定了α = 2.40
color = (255/255, 208/255, 111/255)
ax.plot(x_values, y_values, linestyle='--', color=color, label=r'$\alpha = 2.40$')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('$Degree \quad k$')
plt.ylabel('$CCDF \quad Q(k)$')
plt.legend()
plt.show()

# 输出alpha值
for i, alpha in enumerate(alpha_values):
    print(f"N={node_count}, alpha={alpha:.2f}")

# 输出alpha值和标准误差
for i, (pdf_alpha, alpha_error) in enumerate(zip(pdf_alphas, alpha_errors)):
    print(f"N={node_count}, pdf_alpha={pdf_alpha:.2f}, alpha_error={alpha_error:.2f}")