"""某省的折线图"""
import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line

df = pd.read_excel(r'..\中国疫情信息.xlsx')
data = df.groupby(by='provinceName', as_index=False)

# print(list(data))   # df中的数据按省名称分组
data = list(data)  # 为了获取想要的省的数据，将data转换为list对象，方便切片
# 注意，不可将df转换为list对象，否则df就是14个列头，字符串类型，切片不能得到想要的数据
# datatw = data[-1:]  # 这里选择台湾，在df对象的 9298, 10131 台湾1689, 2531行，将其切片出来
# print(datahlj)
dftw = df[1689:2531:45]  # 每隔45天获取一条数据，方便折线图的绘制与观看//选择台湾4月21日到5月30日之间的确诊人数的折线图
# dftw421 = df[2493:2531]  # 从4月21日开始
# print(dfhlj)

dftw = np.array(dftw)  # 转换为数组，为了方便切片取第一列
# dftw421 = np.array(dftw421)
dftw_sum = [i[0] for i in dftw]  # 累计确诊
dftw_curr = [i[4] for i in dftw]  # 现有确诊
dftw_currincur = [i[5] for i in dftw]  # currentConfirmedIncr
# dftw421_currincur = [i[5] for i in dftw421]
dftw_dead = [i[7] for i in dftw]  # 累计死亡
datestr = [i[6] for i in dftw]  # 时间轴 但是格式不对，整型时间轴要转换为日期型，否则图像难看
# datestr421 = [i[6] for i in dftw421]
date = [pd.to_datetime(i, format='%Y%m%d').date() for i in datestr]
# date421 = [pd.to_datetime(i, format='%Y%m%d').date() for i in datestr421]
# pandas库的to_datetime函数，转换为日期格式。to_datetime转换时间从1970年开始，所以加上格式限制，format='%Y%m%d'
# matplotlib不美观且问题多，所以用pyecharts来美化图片
line = (
    Line(init_opts=opts.InitOpts(renderer='svg', bg_color='#fff'))
        .add_xaxis(xaxis_data=date)
        .add_yaxis(series_name="累计确诊", y_axis=dftw_sum, is_smooth=True)
        .add_yaxis(series_name="现有确诊", y_axis=dftw_curr, is_smooth=True)
        .add_yaxis(series_name="新增确诊", y_axis=dftw_currincur, is_smooth=True)
        .add_yaxis(series_name="累计死亡", y_axis=dftw_dead, is_smooth=True)
        .extend_axis(
        xaxis=opts.AxisOpts(
            axisline_opts=opts.AxisLineOpts(is_on_zero=False)
        )
    )
        .set_global_opts(title_opts=opts.TitleOpts(title="台湾疫情折线图"),
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

line.render(r"..\chart\line\台湾疫情折线图.html")
