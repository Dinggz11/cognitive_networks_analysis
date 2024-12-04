# 单个网络的度分布频率直方图
# 输出每种度的数量
import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 文件
file_path = './07output/02-w_2.xlsx'
df = pd.read_excel(file_path)

# 计算每种度的数量
degree_counts = df['degree'].value_counts().sort_index()

# 计算总节点数
total_nodes = len(df)

# 输出每种度的数量以及总节点数
print("Degrees\tCount")
for degree, count in degree_counts.items():
    print(f"{degree}\t{count}")

print(f"\nTotal nodes: {total_nodes}")

# 绘制度分布图
plt.figure(figsize=(10, 6))
plt.bar(degree_counts.index, degree_counts.values, color='skyblue', edgecolor='black')
plt.title('Degree Distribution')
plt.xlabel('Degree')
plt.ylabel('Count')
plt.grid(True)
plt.show()
