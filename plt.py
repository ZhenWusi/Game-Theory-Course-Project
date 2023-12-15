import pandas as pd
import matplotlib.pyplot as plt

# 用户输入 Case 数字
case_number = int(input("输入 Case 数字: "))

# 构建 Excel 文件路径
excel_file_name = f'simulation_results/Case_{case_number}_results.xlsx'

# 读取 Excel 文件
df = pd.read_excel(excel_file_name)

# 提取两列数据
pay_off_defender = df['pay_off_defender']
pay_off_attacker = df['pay_off_attacker']

# 绘制图表
plt.xlabel('Time (sec)')
plt.ylabel('Pay Off')
plt.plot(pay_off_defender, label='defender')
plt.plot(pay_off_attacker, label='attacker')
plt.legend()
plt.show()
