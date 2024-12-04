# 单个网络的互补累积分布函数CCDF
import pandas as pd
import powerlaw
import matplotlib.pyplot as plt

# 读取数据
number = 2
data = pd.read_excel(f'./07output/02-degree_{number}.xlsx')

# 提取度数数据
degree = data['degree']

# 创建 PowerLaw 拟合对象
fit = powerlaw.Fit(degree, discrete=True)

# 绘制互补累积分布函数（CCDF）的双对数坐标图
plt.figure()
fit.plot_ccdf(color='b', linewidth=2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Degree')
plt.ylabel('CCDF')
plt.title('Complementary Cumulative Distribution Function (CCDF)')
plt.grid(True, which="both", ls="--")
# 输出度指数
print("Degree exponent for CCDF:", fit.power_law.alpha - 1)
plt.show()
