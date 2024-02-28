import pandas as pd

# 定义Excel文件路径
file_path = 'overall_summary.xlsx'  # 根据实际情况调整文件路径

# 使用pandas加载Excel文件的第一个sheet
xlsx = pd.ExcelFile(file_path)
first_sheet_name = xlsx.sheet_names[0]  # 获取第一个sheet的名称
data = pd.read_excel(xlsx, sheet_name=first_sheet_name)

# 首先，按照approach和version进行分组，然后计算每组的大小
mutants_per_approach_version = data.groupby(['approach', 'project', 'version']).size()

# 然后，对每个approach计算平均每个版本的变异体数量
average_mutants_per_approach = mutants_per_approach_version.groupby(level=0).mean()

# 打印结果
print("变异体数量（每个版本，按approach分）:")
print(mutants_per_approach_version)
# 输出到文件中

print("\n平均每个版本的变异体数量（按approach分）:")
print(average_mutants_per_approach)
# 准备输出结果
# output_path = '/mnt/data/mutants_per_approach_version.csv'
# 将变异体数量（每个版本，按approach分）的结果保存到CSV文件
# mutants_per_approach_version.to_csv(output_path)