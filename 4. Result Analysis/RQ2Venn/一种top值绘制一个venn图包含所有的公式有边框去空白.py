import pandas as pd # pip install pandas
import matplotlib.pyplot as plt # pip install matplotlib
import matplotlib.patches as patches
from matplotlib_venn import venn2 # pip install matplotlib-venn

# 设置全局字体为Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
# 设置全局字体大小
plt.rcParams['font.size'] = 40  # 您可以根据需要调整这个大小

# 路径可能需要根据您的文件位置进行调整
file_path_1 = 'top5-All-Metallaxis-susMaxMajorType3Rank.xlsx'
file_path_2 = 'top5-All-Metallaxis-susMaxMbertType3Rank.xlsx'
output_pdf_path = 'top5_file.pdf'  # 输出PDF文件的路径

# 检查每个Excel文件的工作表名称
xls_1 = pd.ExcelFile(file_path_1)
xls_2 = pd.ExcelFile(file_path_2)
sheet_names_1 = xls_1.sheet_names
sheet_names_2 = xls_2.sheet_names

# 确保两个文件具有相同数量和名称的工作表
assert sheet_names_1 == sheet_names_2, "Sheet names or counts do not match between the files."

# 设置图表大小和子图布局
fig, axs = plt.subplots(3, 2, figsize=(15, 15))  # 根据工作表数量调整，这里是3行2列
        
axs = axs.flatten()  # 将二维数组扁平化以便遍历

# 遍历工作表名称，为每个工作表绘制韦恩图
for i, sheet_name in enumerate(sheet_names_1):
    # 读取当前工作表
    df1_sheet = pd.read_excel(xls_1, sheet_name)
    df2_sheet = pd.read_excel(xls_2, sheet_name)

    # 提取两个数据集的'faulty_entity'列，并转换为集合
    faulty_entities_1 = set(df1_sheet.apply(lambda row: f"{row['Version']}-{row['faulty_entity']}", axis=1))
    faulty_entities_2 = set(df2_sheet.apply(lambda row: f"{row['Version']}-{row['faulty_entity']}", axis=1))

    print(len(faulty_entities_1))
    # print(faulty_entities_2)

    # 在当前子图上绘制韦恩图
    venn_diagram = venn2([faulty_entities_1, faulty_entities_2],
                         (r'$F_m$', r'$F_n$'),
                         ax=axs[i])
    
    # 将标题设置在每个子图的中间下方
    axs[i].set_axis_on()
    axs[i].text(0.5, 0.15, sheet_name, fontsize=55, ha='center', va='top', transform=axs[i].transAxes)
    axs[i].set_xlim(-0.7, 0.7)
    axs[i].set_ylim(-1, 0.55)

    for spine in axs[i].spines.values():
        spine.set_edgecolor('gray')  # 设置边框颜色为灰色
        spine.set_linewidth(2)  # 设置边框宽度，可以根据需要调整

# plt.figtext(0.5, 0.001, "Top-5", ha="center", fontsize=20, fontfamily='Times New Roman')
# plt.tight_layout(pad=0.001)
# plt.tight_layout(pad=-0.35)


# plt.tight_layout(pad=0.1, h_pad=-0.35, w_pad=-2)
plt.tight_layout(pad=0.1, h_pad=0.18)
# 保存图表为PDF文件
plt.savefig(output_pdf_path, format='pdf')
plt.show()
