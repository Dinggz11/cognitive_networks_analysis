# 幂律分布与截断幂律分布 power_law', 'truncated_power_law'
# 20240809 运行结果只有Network Four符合截断幂律分布，整体符合的还是幂律分布更适合
import powerlaw
import pandas as pd

suffixes = ['2', '3', '4', '5', '6', '7', '8']
numbers = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight']

for i, suffix in enumerate(suffixes):
    # 读取数据表
    df = pd.read_excel(f'./07output/02-w_{suffix}.xlsx')

    # 提取度数数据
    degrees = df['degree']

    # 拟合幂律和截断幂律分布
    fit_power_law = powerlaw.Fit(degrees, discrete=True)
    fit_truncated_power_law = powerlaw.Fit(degrees, discrete=True, xmin=fit_power_law.xmin)

    # 比较拟合结果
    R, p = fit_power_law.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)

    # 输出比较结果
    print(f"Network {numbers[i].capitalize()}:")
    print(f"Comparing Power Law and Truncated Power Law: R = {R}, p-value = {p}")

    # 判断哪个分布更适合
    if R > 0:
        print("Truncated Power Law fits the data better.")
    else:
        print("Power Law fits the data better.")

    print()  # 添加空行分隔不同网络的结果
