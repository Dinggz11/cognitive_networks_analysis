# 单个网络的度分布频率直方图
# 输出每种度的比例，计算每个度数出现的频率，并将其作为字典或数据框输出
import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 文件
file_path = './07output/02-w_3.xlsx'
df = pd.read_excel(file_path)

# 计算每种度的频率
degree_counts = df['degree'].value_counts(normalize=True).sort_index()

# 输出每种度的比例
print("Degrees\tProbability")
for degree, probability in degree_counts.items():
    print(f"{degree}\t{probability}")

# 绘制度分布图
plt.figure(figsize=(10, 6))
plt.bar(degree_counts.index, degree_counts.values, color='skyblue', edgecolor='black')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Probability')
plt.grid(True)
plt.show()
