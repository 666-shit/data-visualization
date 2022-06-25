"""湖北台湾死亡率对比图"""
from __future__ import unicode_literals
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar

df = pd.read_excel(r'..\中国疫情信息.xlsx')
data = df.groupby(by='provinceName', as_index=False).last()
data_list_sumconf = list(zip(data['provinceName'].values.tolist(), data['confirmedCount'].values.tolist()))
data_list_currconf = list(zip(data['provinceName'].values.tolist(), data['currentConfirmedCount'].values.tolist()))
data_list_deadcount = list(zip(data['provinceName'].values.tolist(), data['deadCount'].values.tolist()))

dftw = df[1687:2531:45]
dftw = np.array(dftw)
dftw_sum = [i[0] for i in dftw]  # 确诊总人数除以死亡人数为死亡率
dftw_dead = [i[7] for i in dftw]
dftw_dead = np.array(dftw_dead)
dftw_sum = np.array(dftw_sum)
tw_list_deadrate = list(dftw_dead / dftw_sum)
tw_list_deadrate = [float('{:.3f}'.format(i)) for i in tw_list_deadrate]  # 控制保留小数点后3位左右

dfhb = df[21949:22975:45]
dfhb = np.array(dfhb)
dfhb_sum = [i[0] for i in dfhb]
dfhb_dead = [i[7] for i in dfhb]
dfhb_dead = np.array(dfhb_dead)
dfhb_sum = np.array(dfhb_sum)
hb_list_deadrate = list(dfhb_dead / dfhb_sum)
hb_list_deadrate = [float('{:.3f}'.format(i)) for i in hb_list_deadrate]  # 控制保留小数点后3位左右

data_pn = np.array(data)
df_pname = [i[0] for i in data_pn]

datestr = [i[6] for i in dftw]  # 提取原文件字符串格式的日期，需要转换格式，否则显示出错
date = [pd.to_datetime(i, format='%Y%m%d').date() for i in datestr]
# to_datetime.date, 将字符串的日期转换为日期格式，后面的.date用来去掉时分秒只保留日期

bar_tw_vs_hb = (
    Bar(init_opts=opts.InitOpts(renderer='svg', bg_color='#fff'))
        .add_xaxis(xaxis_data=date)
        .add_yaxis('台湾死亡率', tw_list_deadrate)  # 对比45天为间隔的每一阶段的死亡率
        .add_yaxis('湖北死亡率', hb_list_deadrate)
        .set_global_opts(title_opts=opts.TitleOpts(title='台湾湖北疫情死亡率比较', subtitle="截至2022-05-30"),
                         toolbox_opts=opts.BrushOpts(),
                         tooltip_opts=opts.TooltipOpts(is_show=False),
                         xaxis_opts=opts.AxisOpts(
                             axislabel_opts={"rotate": 30}
                         ),
                         yaxis_opts=opts.AxisOpts(
                             # 分割线配置，显示 y 轴每个刻度的分割线
                             splitline_opts=opts.SplitLineOpts(is_show=True),
                         )
                         )
)
bar_tw_vs_hb.render(path="台湾湖北疫情死亡率对比.html", delay=3)
