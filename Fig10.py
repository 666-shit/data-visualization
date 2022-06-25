"""某省421后的折线图"""
import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line

df = pd.read_excel(r'..\中国疫情信息.xlsx')
data = df.groupby(by='provinceName', as_index=False)

# print(list(data))   # df中的数据按省名称分组
data = list(data)  # 为了获取想要的省的数据，将data转换为list对象，方便切片
# 注意，不可将df转换为list对象，否则df就是14个列头，字符串类型，切片不能得到想要的数据

dftw421 = df[2491:2531]  # 从4月21日开始

dftw = np.array(dftw421)  # 转换为数组，为了方便切片取第一列
# dftw421 = np.array(dftw421)
dftw_sum = [i[0] for i in dftw]  # 累计确诊
dftw_curr = [i[4] for i in dftw]  # 现有确诊
dftw_currincur = [i[5] for i in dftw]  # currentConfirmedIncr
# dftw421_currincur = [i[5] for i in dftw421]
dftw_dead = [i[7] for i in dftw]  # 累计死亡
datestr = [i[6] for i in dftw]  # 时间轴 但是格式不对，整型时间轴要转换为日期型，否则图像难看
# datestr421 = [i[6] for i in dftw421]
date = [pd.to_datetime(i, format='%Y%m%d').date() for i in datestr]

line = (
    Line(init_opts=opts.InitOpts(renderer='svg', bg_color='#fff'))
        .add_xaxis(xaxis_data=date)
        .add_yaxis(series_name="新增确诊", y_axis=dftw_currincur, is_smooth=True)
        .extend_axis(
        xaxis=opts.AxisOpts(
            axisline_opts=opts.AxisLineOpts(is_on_zero=False)
        )
    )
        .set_global_opts(title_opts=opts.TitleOpts(title="4月21日后台湾新增折线图"),
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

line.render(r"..\chart\line\4月21日后台湾新增折线图.html")
