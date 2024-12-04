import pandas as pd

# 读取数据表
file_number = 2
data = pd.read_excel(f'./07output/06-merge-T_ij-w_iw_j-s-d-{file_number}.xlsx')

# 读取数据表02-w_2.xlsx中的数据，假设这里包含了word与eigenvector_centrality的对应关系
centrality_data = pd.read_excel(f'./07output/02-w_{file_number}.xlsx')

# 合并数据，以获取word1和word2对应的eigenvector_centrality值
data = data.merge(centrality_data[['word', 'word_count', 'degree', 'degree_centrality', 'closeness_centrality', 'betweenness', 'betweenness_centrality', 'eigenvector_centrality', 'clustering_coefficient']], left_on='word1', right_on='word', how='left')
data.rename(columns={'word_count':'word_count_i', 'degree':'degree_i', 'degree_centrality':'degree_centrality_i', 'closeness_centrality':'closeness_centrality_i', 'betweenness':'betweenness_i', 'betweenness_centrality':'betweenness_centrality_i', 'eigenvector_centrality':'eigenvector_centrality_i', 'clustering_coefficient':'clustering_coefficient_i'}, inplace=True)
data.drop('word', axis=1, inplace=True)

data = data.merge(centrality_data[['word', 'word_count', 'degree', 'degree_centrality', 'closeness_centrality', 'betweenness', 'betweenness_centrality', 'eigenvector_centrality', 'clustering_coefficient']], left_on='word2', right_on='word', how='left')
data.rename(columns={'word_count':'word_count_j', 'degree':'degree_j', 'degree_centrality':'degree_centrality_j', 'closeness_centrality':'closeness_centrality_j', 'betweenness':'betweenness_j', 'betweenness_centrality':'betweenness_centrality_j', 'eigenvector_centrality':'eigenvector_centrality_j', 'clustering_coefficient':'clustering_coefficient_j'}, inplace=True)
data.drop('word', axis=1, inplace=True)

# 保存为新的Excel表格
output_file_path = f'./07output/06-merge-T_ij-w_iw_j-s-d-final-{file_number}.xlsx'
data.to_excel(output_file_path, index=False)
