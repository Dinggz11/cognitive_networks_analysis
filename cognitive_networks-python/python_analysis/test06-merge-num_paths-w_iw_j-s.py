import pandas as pd
import numpy as np

# 读取三个Excel文件
exp_id = 2
df_num_paths = pd.read_excel(f'./07output/06-merge-T_ij-w_iw_j-{exp_id}.xlsx')
df_s1 = pd.read_excel(f'./07output/02-preferential_attachment_{exp_id}.xlsx')

# 对 word1 和 word2 列进行排序
df_num_paths[['word1', 'word2']] = np.sort(df_num_paths[['word1', 'word2']], axis=1)
df_s1[['word1', 'word2']] = np.sort(df_s1[['word1', 'word2']], axis=1)

# 合并 df_num_paths 和 df_s1，基于 'word1' 和 'word2' 列
merged_df = pd.merge(df_num_paths, df_s1, on=['word1', 'word2'], how='inner')

# 去除重复的词汇对记录
merged_df = merged_df.drop_duplicates(subset=['word1', 'word2', 'num_paths', 'preferential_attachment'])

merged_df.to_excel(f'./07output/06-merge-T_ij-w_iw_j-s-{exp_id}.xlsx', index=False)