# 单个网络的概率密度函数（Probability Density Function，PDF）
# powerlaw的plot_pdf
import powerlaw
import matplotlib.pyplot as plt
import pandas as pd
# 读取数据
number = 2
data = pd.read_excel(f'./07output/02-degree_{number}.xlsx')

# 提取度数数据
degrees = data['degree'].values

# 拟合度分布
fit = powerlaw.Fit(degrees, discrete=True)

# 输出度指数
print("Degree exponent:", fit.power_law.alpha)

# 绘制拟合结果
fit.plot_pdf(color='b', linewidth=2)
fit.power_law.plot_pdf(color='r', linestyle='--', ax=plt.gca())
plt.xscale('log')
plt.yscale('log')
plt.show()