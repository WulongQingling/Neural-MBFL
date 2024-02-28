import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

plt.rcParams.update({'font.size': 20, 'font.family': 'Times New Roman'})

# 加载数据
data_path = 'repair_patterns_actions_corrected_ratios.xlsx'
data = pd.read_excel(data_path)

# 定义自定义颜色
colors = ["#93C9DE", "#9CE29C"]

# 设置图形和轴
fig, ax = plt.subplots(figsize=(10, 9))

# 绘制堆叠条形图
data.set_index("Item")[["Neural-MBFL", "MBFL"]].plot(kind="bar", stacked=True, ax=ax, color=colors)

# 设置标签和标题
ax.set_ylabel("Percentage")
ax.set_xlabel("Repair Pattern")
ax.set_ylim(0, 1)  # 设置y轴的限制为0-100%

# 将y轴标签转换为百分比nm
ax.yaxis.set_major_formatter(PercentFormatter(1))

# 将图例移动到图表外部，避免重叠
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)

plt.tight_layout()
plt.savefig("repair_pattern_percent_combine_top5.pdf")
plt.show()
