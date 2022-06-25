import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Scatter

df = pd.read_excel(r'..\中国疫情信息.xlsx')
data = df.groupby(by='provinceName', as_index=False).last()

dftw = df[2140:2265:5]
dftw = np.array(dftw)
dftw_sum = [i[0] for i in dftw]  # 确诊总人数除以死亡人数为死亡率
dftw_cured = [i[2] for i in dftw]
dftw_dead = [i[7] for i in dftw]

data_pn = np.array(data)
df_pname = [i[0] for i in data_pn]

datestr = [i[6] for i in dftw]  # 提取原文件字符串格式的日期，需要转换格式，否则显示出错
date = [pd.to_datetime(i, format='%Y%m%d').date() for i in datestr]

s = (
    Scatter(init_opts=opts.InitOpts(renderer='svg', bg_color='#fff'))
        .add_xaxis(xaxis_data=date)
        .add_yaxis('死亡人数', dftw_dead, symbol='triangle', symbol_size=10, color='red')
        .add_yaxis('治愈人数', dftw_cured, symbol_size=10, color='green')
        .add_yaxis('确诊人数', dftw_sum, symbol='rect', symbol_size=10, color='black')
        .set_global_opts(title_opts=opts.TitleOpts(title='台湾疫情散点图', subtitle="202-5-5到2021-9-2"),
                         toolbox_opts=opts.ToolboxOpts(),
                         tooltip_opts=opts.TooltipOpts(is_show=True),
                         xaxis_opts=opts.AxisOpts(
                             axislabel_opts={"rotate": 30}
                         ),
                         yaxis_opts=opts.AxisOpts(
                             # 分割线配置，显示 y 轴每个刻度的分割线
                             splitline_opts=opts.SplitLineOpts(is_show=True),
                         )
                         )
)

s.render("../chart/scatter/台湾疫情散点图.html")
