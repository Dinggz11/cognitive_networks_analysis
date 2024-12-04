# 单个网络的累积度分布函数（cumulative degree distribution function），双对数坐标图
# 累积分布函数（Cumulative Distribution Function, CDF）
# the cumulative distribution function (CDF; p(X < x))
# 使用powerlaw的plt_cdf()进行
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

# 输出度指数
print("Degree exponent for CDF:", -(fit.power_law.alpha - 1))

# 绘制双对数坐标图
plt.figure()
fit.plot_cdf(color='b', linewidth=2)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Degree')
plt.ylabel('CDF')
plt.title('Cumulative Distribution Function (CDF)')
plt.grid(True, which="both", ls="--")
plt.show()



