"""疫情地图"""
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot

df = pd.read_excel(r'..\中国疫情信息.xlsx')
data = df.groupby(by='provinceName', as_index=False).last()  # 用.last()来取到最后一个值
data_list_deadcount = list(zip(data['provinceName'].values.tolist(), data['deadCount'].values.tolist()))

pieces_deadcount = [
    {"max": 9, "min": 0, "label": "0-9", "color": "#FFE4E1"},
    {"max": 99, "min": 10, "label": "10-99", "color": "#FF7F50"},
    {"max": 499, "min": 100, "label": "100-499", "color": "#F08080"},
    {"max": 999, "min": 500, "label": "500-999", "color": "#CD5C5C"},
    {"max": 9999, "min": 1000, "label": "1000-9999", "color": "#990000"},
    {"max": 9999999, "min": 10000, "label": "10000-999999", "color": "#660000"},
]

d = (
    Map(opts.InitOpts(renderer='svg'))
    .add(series_name="累计死亡人数", data_pair=data_list_deadcount, maptype='china')
    .set_global_opts(
        title_opts=opts.TitleOpts(title='疫情地图(2020-01-25~2022-05-30)'),
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces_deadcount)
    )
)

make_snapshot(snapshot, d.render('累计死亡地图.html'), "累计死亡地图.svg")
