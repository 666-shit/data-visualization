import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel(r'..\中国疫情信息.xlsx')
data = df.groupby(by='provinceName', as_index=False).last()
data_list_sumconf = list(zip(data['provinceName'].values.tolist(), data['confirmedCount'].values.tolist()))
data_list_currconf = list(zip(data['provinceName'].values.tolist(), data['currentConfirmedCount'].values.tolist()))
data_list_deadcount = list(zip(data['provinceName'].values.tolist(), data['deadCount'].values.tolist()))

fit, axes = plt.subplots(figsize=(16, 8))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
arrPname = np.array(list(data.provinceName))  # matplotlib中画图使用的是数组
arrSumconf = np.array(list(data.confirmedCount))
arrCurrconf = np.array(list(data.currentConfirmedCount))
arrDeadcount = np.array(list(data.deadCount))
xticks_country = np.arange(len(arrPname))
ydata = [ydata for ydata in range(2000000)]

axes.bar(xticks_country, arrSumconf, width=0.25, label="累计确诊人数", color="red")
axes.bar(xticks_country + 0.25, arrCurrconf, width=0.25, label="当前确诊人数", color="blue")
axes.bar(xticks_country + 0.5, arrDeadcount, width=0.25, label="累计死亡人数", color="green")
for i in range(len(arrPname)):
    plt.bar(arrPname[i], ydata[i])
axes.set_title("全国疫情柱状图", fontsize=20)
axes.set_xlabel("省")
axes.set_ylabel("人数")
axes.legend()
plt.savefig(r'C:\Users\c1533\Desktop\全国疫情柱状图.svg')
plt.show()
