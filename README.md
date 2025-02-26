
# GTM-CSec仿真
本仓库由甄五四、刘涛、梁浩哲基于SCI二区论文“GTM-CSec: Game theoretic model for cloud security based on IDS and honeypot”合作完成的博弈仿真实验。
论文链接：https://www.sciencedirect.com/science/article/pii/S0167404820300195
## 摘要：
在本文中，我们提出了一种名为GTM-CSec 的博弈论模型。该模型以智能的方式选择基于签名、异常和蜜罐的检测模块，以便更有效地检测防御攻击。与同时使用所有模块相比，选择特定的检测模块不仅有助于降低能耗，还能提高整体防御系统的效率。模型对防御者和攻击者策略进行了全面评估，并使用纳什均衡（NE）确定了最佳策略。最后，我们引入该模型进行仿真实验，结果证明防系统在抵御攻击方面取得显著成就。 
## 使用方法：
* 环境要求：windows 10，python==3.10.0
* 安装依赖项:
    - `pip install -r requirements.txt`
* 运行脚本:
    - `python simulation.py`

* 注意：我们的仿真结果数据保存simulation_results文件夹中，检查结果保存到images文件夹中

## 我们的仿真可视化结果:

1) Case 2: 
<img src="images/Case_2_Result.png"/>

2) Case 3: 
<img src="images/Case_3_Result.png"/>

3) Case 4: 
<img src="images/Case_4_Result.png"/>

4) Case 5: 
<img src="images/Case_5_Result.png"/>

5) Case 6: 
<img src="images/Case_6_Result.png"/>

6) Case 7: 
<img src="images/Case_7_Result.png"/>

* 由于基于随机数的仿真结果，每次运行均会不同，但攻击者和防御者pay off趋势是相同的。如果你想得到我们的检查结果你可以直接运行
    - `python plt.py`
    
### 如有错误，感谢您的批评指正。
