# Model: OLS
import pandas as pd
import numpy as np
import statsmodels.api as sm

# 读取数据表
file_number = 2
data = pd.read_excel(f'./07output/06-merge-T_ij-w_iw_j-s-d-final-{file_number}.xlsx')

# 将零或负值替换为一个极小的数
epsilon = 1e-10
data['num_paths'] = data['num_paths'].apply(lambda x: x if x > 0 else epsilon)
data['clustering_coefficient_i'] = data['clustering_coefficient_i'].apply(lambda x: x if x > 0 else epsilon)
data['clustering_coefficient_j'] = data['clustering_coefficient_j'].apply(lambda x: x if x > 0 else epsilon)

# 读取数据并进行log变换
data['log_T_ij'] = np.log(data['num_paths'])
data['log_w_i'] = np.log(data['clustering_coefficient_i'])
data['log_w_j'] = np.log(data['clustering_coefficient_j'])

# 多元线性回归模型(使用StatsModels库中的OLS（普通最小二乘）函数来拟合多元线性回归模型)
X = data[['log_w_i', 'log_w_j', 'shortest_path_length']]
X = sm.add_constant(X)
y = data['log_T_ij']

model = sm.OLS(y, X)
results = model.fit(cov_type='HC3')

# 打印回归结果
print(results.summary())

# 计算RSS
rss = np.sum((results.resid) ** 2)
print(f'Residual Sum of Squares (RSS): {rss}')
