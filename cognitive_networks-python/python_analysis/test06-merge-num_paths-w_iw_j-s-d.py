import pandas as pd
import numpy as np

# 读取两个Excel文件
exp_id = 2
df_merged_data = pd.read_excel(f'./07output/06-merge-T_ij-w_iw_j-s-{exp_id}.xlsx')
df_shortest_path = pd.read_excel(f'./07output/02-shortest_path_length_{exp_id}.xlsx')

# 对 word1 和 word2 列进行排序，确保无论词汇对的位置如何都能匹配
df_merged_data[['word1', 'word2']] = np.sort(df_merged_data[['word1', 'word2']], axis=1)
df_shortest_path[['word1', 'word2']] = np.sort(df_shortest_path[['word1', 'word2']], axis=1)

# 合并两个数据框，基于 'word1' 和 'word2' 列
merged_df = pd.merge(df_merged_data, df_shortest_path, on=['word1', 'word2'], how='inner')

# 去除重复的词汇对记录
merged_df = merged_df.drop_duplicates()

# 保存结果
merged_df.to_excel(f'./07output/06-merge-T_ij-w_iw_j-s-d-{exp_id}.xlsx', index=False)
