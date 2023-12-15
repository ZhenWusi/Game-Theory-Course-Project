import sklearn
import numpy as np
import pandas as pd
import time
import schedule
import matplotlib.pyplot as plt
from drawnow import drawnow
import random
# 全局变量声明
global count, x_axis, defender, attacker, generated_values ,case_number
def check_constraint(time, a, u, y, B, G, R, V, E, H):
    global generated_values
    if generated_values['E'] < E or generated_values['H'] < H or generated_values['R'] < R:
        return True
    else:
        return False
def generate():
    global count, defender, attacker, x_axis, generated_values
    if count == seconds + 1:
        raise RuntimeError("仿真完成！")
    # 从 get_random_value 函数中获取随机生成的变量值。
    a, u, y, B, G, R, V, E, H = get_random_value(count)
    # 根据用户输入的Case数字选择调用的函数
    if case_number == 2:
        while(u+a-y)==0 or (u-y-a)==0:  # 如果为0重新生成
            a, u, y, B, G, R, V, E, H = get_random_value(count)
        Ud = case_2_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_2_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif case_number == 3:
        Ud = case_3_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_3_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif case_number == 4:
        while (u + a - y) == 0 or (u - y - a) == 0:  # 如果为0重新生成
            a, u, y, B, G, R, V, E, H = get_random_value(count)
        Ud = case_4_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_4_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif case_number == 5:
        Ud = case_5_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_5_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif case_number == 6:
        while u==y:  # 如果u-y or y-u为0重新生成
            a, u, y, B, G, R, V, E, H = get_random_value(count)
        Ud = case_6_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_6_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    elif case_number == 7:
        Ud = case_7_get_pay_off_defender(a, u, y, B, G, R, V, E, H)
        Ua = case_7_get_pay_off_attacker(a, u, y, B, G, R, V, E, H)
    else:
        raise ValueError("无效的Case数字")
    if check_constraint(count, a, u, y, B, G, R, V, E, H):
        # 将时间点添加到 x 轴列表中
        x_axis.append(count)
        # 将防守方的支付添加到 defender 列表中
        defender.append(Ud)
        # 将攻击方的支付添加到 attacker 列表中
        attacker.append(Ua)
        # 使用 drawnow 模块更新绘图，调用 create_plot 函数。
        drawnow(create_plot)
        # 更新 generated_values 字典，记录当前生成的变量值。
        generated_values = {
            'a': a,
            'u': u,
            'y': y,
            'B': B,
            'G': G,
            'R': R,
            'V': V,
            'E': E,
            'H': H
        }
    count += 1
    global df
    # 数据添加
    new_row = {
        'anomaly': a,
        'signature': u,
        'honeypot': y,
        'gain_detection': B,
        'gain_attack': G,
        'resource': R,
        'asset_value': V,
        'ids_energy': E,
        'ids_honeypot': H,
        'pay_off_defender': Ud,
        'pay_off_attacker': Ua,
    }
    df = df._append(new_row, ignore_index=True)
    # 保存仿真数据到excel中
    excel_file_name = f'simulation_results/Case_{case_number}_results.xlsx'
    df.to_excel(excel_file_name, index=False)
def create_plot():
    plt.xlabel('Time (sec)')
    plt.ylabel('Pay Off')
    plt.plot(x_axis, defender, label='defender')
    plt.plot(x_axis, attacker, label='attacker')
    plt.legend()
    plt.pause(1e-3)
    # 保存图像文件
    plot_file_name = f'images/Case_{case_number}_Result.png'
    plt.savefig(plot_file_name)
# 定义了一系列函数，用于计算不同情况下防守方和攻击方的支付。

def case_2_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = u/(u+a-y)
    q = (u-y-2*a)/(u-y-a)-(V)/((u-y-a)*(B+V))-(H)/((u-y-a)*(B+V))
    return (p*q*u*B) + (p*q*u*V) + (p*V) + (q*y*B) + (q*y*V) - (p*q*y*B) - (p*q*y*V) - (p*a*B) - (p*a*V) + (p*H) - (q*a*B) - (q*a*V) + (p*q*a*B) + (p*q*a*V)

def case_2_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = u/(u+a-y)
    q = (u-y-2*a)/(u-y-a)-(V)/((u-y-a)*(B+V))-(H)/((u-y-a)*(B+V))
    return  (4*G) - (p*u*G) + (p*a*G) - (2*p*G) - (q*y*G) + (q*a*G) - (p*q*u*G) + (p*q*y*G) - (p*q*a*G) - (a*G) - (2*R)

def case_3_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p=a/(a+u+y)
    q=(u+y)/(u+a+y) + V/((u+a+y)*(B+V)) + H/((u+y+a)*(B+V))
    return (p*a*B) - (p*V) + (p*a*V) - (p*q*a*B) - (p*q*a*V) + (p*u*B) - (2*q*V) - (q*y*B) + (q*y*V) - (q*H) - (p*q*u*B) - (p*q*u*V) - (p*q*y*B) - (p*q*y*V) + (p*H) + (q*E) + (2*q*V) + (q*H)

def case_3_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p=a/(a+u+y)
    q=(u+y)/(u+a+y) + V/((u+a+y)*(B+V)) + H/((u+y+a)*(B+V))
    return (p*G) - (p*a*G) - (p*R) + (p*q*a*G) - (u*q*G) - (q*a*G) + (p*q*u*G) + (p*q*y*G) + (2*G) - (2*R) - (2*p*G) + (2*p*R)

def case_4_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = y/(y+a-u)
    q=(y-u-2*a)/(y-u-a) + V/((y-u-a)*(B+V)) + H/((y-u-a)*(B+V)) - (2*E)/((y-u-a)*(B+V))
    return (p*q*y*B) + (p*q*y*V) - (p*H) - (p*V) - (p*q*u*B) - (p*q*u*V) - (p*a*B) + (2*p*V) - (p*a*V) + (2*p*E) + (p*q*a*B) + (p*q*a*V)

def case_4_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = y/(y+a-u)
    q=(y-u-2*a)/(y-u-a) + V/((y-u-a)*(B+V)) + H/((y-u-a)*(B+V)) - (2*E)/((y-u-a)*(B+V))
    return ((-p*q*y*G) + (p*G) - (p*R) - (y*u*G) + (p*q*u*G) + (2*G) - (2*R) - (a*G) - (2*p*G) + (2*p*R) + (p*a*G) + (y*a*G) - (p*q*a*G))

def case_5_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = a/(u+a)
    q = p
    return ((p*q*u*B) + (p*q*a*B) + (p*q*u*V) + (p*q*a*V) - (p*a*B) - (p*a*V) - (q*a*B) - (q*a*V))

def case_5_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = a/(u+a)
    q = p
    return ((-p*q*u*G) + 1 - (a*G) - R + (p*a*G) + (q*a*G) - (p*q*a*G))\

def case_6_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p = y/(y-u)
    q = (E-H)/(u-y)
    return (p*q*u*B) + (p*q*u*V) + (q*y*B) + (q*y*V) - (p*q*y*B) - (p*q*y*V) - (H) - (V) + (p*H) - (p*E)

def case_6_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p = y/(y-u)
    q = (E-H)/(u-y)
    return (-p*q*u*G) - (q*y*G) - (p*q*G) + (p*q*a*G) + (p*q*R) + (G) - (R) + (p*q*G) - (p*q*R)

def case_7_get_pay_off_defender(a, u, y, B, G, R, V, E, H):
    p=y/(y+a)
    q=a/(a+y)
    return (q*y*B) + (q*y*V) - (p*q*y*B) - (p*q*a*V) + (p*a*B) + (p*a*V) - (p*q*a*B) - (p*q*a*V) - (H) - (V)
def case_7_get_pay_off_attacker(a, u, y, B, G, R, V, E, H):
    p=y/(y+a)
    q=a/(a+y)
    return (p*a*G) + (p*q*a*G) - (p*y*G) + (p*q*y*G) + (G) - (R)
# 定义了 get_random_value 函数，用于获取随机生成的变量值。
def get_random_value(time):
    a = random.choice(alpha)  # IDS异常检测率
    y = random.choice(gamma)  # 蜜罐检测率
    u = random.choice(mue)    # IDS 误用检测率
    B = random.choice(Bds)    # 成功检测的增益
    G = random.choice(Gat)    # 攻击成功获得的增益
    R = random.choice(Rat)    # 攻击者消耗的资源
    V = random.choice(Vass)   # 受攻击资产的价值
    H = random.choice(Hhp)    # 蜜罐消耗的能量
    E = random.choice(Eds)    # IDS 消耗的能量
    return a, u, y, B, G, R, V, E, H

if __name__ == "__main__":
    # 用户输入秒数并将其转换为整数
    seconds = int(input("请输入您的仿真实验次数: "))
    # 用户输入 Case 数字
    case_number = int(input("输入 Case 数字: "))
    # 防御系统的检测率（μ、α、γ）取值范围为0到0.99
    mue = list(np.arange(0, 1.00, 0.01))  # 值从0到0.99,IDS 误用检测率
    alpha = mue  # 值从0到0.99,IDS异常检测率
    gamma = mue  # 值从0到0.99,蜜罐检测率
    Bds = list([-5, 0, 5])  # bds成功检测的增益
    # 防御者和攻击者的增益被取为-5、0或5。玩家要么输掉并获得-5，要么获胜并获得5，要么保持静止并获得0增益。
    Gat = Bds  # gat:攻击成功获得的增益
    Eds = list(np.arange(0, 1.00, 0.01))  # eds:IDS 消耗的能量
    Hhp = Eds # Hhp:蜜罐消耗的能量
    Rat = Hhp # rat:攻击者消耗的资源,资产的价值范围为1到5。该值应等于或小于收益
    Vass = list(np.arange(1, 5, 1))  # 受攻击资产的价值
    x_axis = []
    defender = []
    attacker = []
    count = 1 # 我们从1开始每秒调用一次函数，count为调用次数
    # 创建了一个带有指定列名的空pandas DataFrame
    df = pd.DataFrame(columns=[
        'anomaly',  # a
        'signature',  # u
        'honeypot',  # y 蜜罐的指标
        'gain_detection',  # B 检测到攻击时系统获得的收益
        'gain_attack',  # G 攻击者成功发动攻击时获得的收益
        'resource',  # R 表示系统资源的指标
        'asset_value',  # V 表示系统资产的价值
        'ids_energy',  # E 入侵检测系统（IDS）的能量或资源
        'ids_honeypot',  # H 代表IDS中用于处理蜜罐的资源
    ])
    # 用键对应于不同变量的字典generated_values进行了初始化
    generated_values = {
        'a': 0,
        'u': 0,
        'y': 0,
        'B': 0,
        'G': 0,
        'R': 0,
        'V': 0,
        'E': 0,
        'H': 0
    }
    # 每隔1秒执行一次 generate 函数
    schedule.every(1).second.do(generate)
    while True:
        schedule.run_pending() # 在每次循环之后，程序会暂停（休眠）1秒钟#
        time.sleep(1)

