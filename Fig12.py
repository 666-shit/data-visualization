"""全国疫情饼图"""
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Pie

df = pd.read_excel(r'..\中国疫情信息.xlsx')
data = df.groupby(by='provinceName', as_index=False).last()

data_list_sumconf = list(zip(data['provinceName'].values.tolist(), data['confirmedCount'].values.tolist()))
data_list_currconf = list(zip(data['provinceName'].values.tolist(), data['currentConfirmedCount'].values.tolist()))
data_list_deadcount = list(zip(data['provinceName'].values.tolist(), data['deadCount'].values.tolist()))
data_pn = np.array(data)
df_pname = [i[0] for i in data_pn]
df_pname = list(map(str, df_pname))
print(df_pname)

color_series = ['#FAE927', '#E9E416', '#C9DA36', '#9ECB3C', '#6DBC49',
                '#37B44E', '#3DBA78', '#14ADCF', '#209AC9', '#1E91CA',
                '#2C6BA0', '#2B55A1', '#2D3D8E', '#44388E', '#6A368B',
                '#7D3990', '#A63F98', '#C31C88', '#D52178', '#D5225B',
                '#D02C2A', '#D44C2D', '#F57A34', '#FA8F2F', '#D99D21',
                '#CF7B25', '#CF7B25', '#CF7B25']  # 每个省对应不同的颜色
a = (i[1] for i in data_list_sumconf)
df = pd.DataFrame({'provinces': df_pname, 'num': a})
df.sort_values(by='num', ascending=False, inplace=True)
pname = df['provinces'].values.tolist()
pdata = df['num'].values.tolist()

df_sort = df
arr_df = df.values  # 转二维数组删除前5
arr_notop5 = np.delete(arr_df, [0, 1, 2, 3, 4], axis=0)
df_notop5 = pd.DataFrame(arr_notop5)  # 转回df
df_notop5.columns = ['provinces', 'num']
pname_notop5 = df_notop5['provinces'].values.tolist()
pdata_notop5 = df_notop5['num'].values.tolist()

pie_notop5 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px', renderer='svg', bg_color='white'))
pie_notop5.set_colors(color_series)
pie_notop5.add(
    "", [list(z) for z in zip(pname_notop5, pdata_notop5)],
    radius=["30%", "135%"],
    center=["50%", "65%"],
    rosetype="area"
)
pie_notop5.set_global_opts(
    title_opts=opts.TitleOpts(title='疫情数据玫瑰图(无前五名省份)'),
    legend_opts=opts.LegendOpts(is_show=False),
    toolbox_opts=opts.ToolboxOpts()
)
pie_notop5.set_series_opts(
    label_opts=opts.LabelOpts(
        is_show=True, position="inside", font_size=10,
        formatter="{b}:{c}人", font_style="italic",
        font_weight="bold", font_family="Microsoft YaHei", color="blue", border_color="green"
    ),
)

pie_notop5.render(r"..\chart\pie\全国疫情玫瑰图(无前五名省份).html")
