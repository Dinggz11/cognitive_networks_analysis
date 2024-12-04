import pandas as pd

# 读取两个 Excel 文件=n(n=2~8) 的数据
exp_id = 2
df1 = pd.read_excel(f'../07data_analysis/07output/02-num_paths_cutoff8_{exp_id}.xlsx')
df2 = pd.read_excel(f'../07data_analysis/07output/02-w_{exp_id}.xlsx')

# 合并两个数据框，根据共同的列 word1 和 word2
merged_df = pd.merge(df1, df2, left_on=['word1'], right_on=['word'], how='inner')
merged_df = pd.merge(merged_df, df2, left_on=['word2'], right_on=['word'], how='inner', suffixes=('_word1', '_word2'))

# 创建新的字段
merged_df['word_count_wiwj'] = merged_df['word_count_word1'] * merged_df['word_count_word2']
merged_df['degree_wiwj'] = merged_df['degree_word1'] * merged_df['degree_word2']
merged_df['degree_centrality_wiwj'] = merged_df['degree_centrality_word1'] * merged_df['degree_centrality_word2']
merged_df['closeness_centrality_wiwj'] = merged_df['closeness_centrality_word1'] * merged_df['closeness_centrality_word2']
merged_df['betweenness_wiwj'] = merged_df['betweenness_word1'] * merged_df['betweenness_word2']
merged_df['betweenness_centrality_wiwj'] = merged_df['betweenness_centrality_word1'] * merged_df['betweenness_centrality_word2']
merged_df['eigenvector_centrality_wiwj'] = merged_df['eigenvector_centrality_word1'] * merged_df['eigenvector_centrality_word2']
merged_df['clustering_coefficient_wiwj'] = merged_df['clustering_coefficient_word1'] * merged_df['clustering_coefficient_word2']

# 选择需要的列
new_df = merged_df[['word1', 'word2', 'num_paths', 'word_count_wiwj', 'degree_wiwj', 'degree_centrality_wiwj', 'closeness_centrality_wiwj', 'betweenness_wiwj', 'betweenness_centrality_wiwj', 'eigenvector_centrality_wiwj', 'clustering_coefficient_wiwj']]

# 保存结果到新的 Excel 文件
new_df.to_excel(f'./07output/06-merge-T_ij-w_iw_j-{exp_id}.xlsx', index=False)
