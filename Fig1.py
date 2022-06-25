import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot

df = pd.read_excel(r'..\中国疫情信息.xlsx')
data = df.groupby(by='provinceName', as_index=False).last()  # 用.last()来取到最后一个值
data_list_sumconf = list(zip(data['provinceName'].values.tolist(), data['confirmedCount'].values.tolist()))

pieces_sumconf = [
    # 因为中国各省的疫情数据差异较大，所以需要选择合适的区间来进行着色，否则会出现大片区域颜色相同，但有的色区没有对应的省，如果区间范围太小，则会出现某些省无法着色的问题，比如将最大的范围设置成10000到99999，则台湾省由于人数过多无法被着色
    {"max": 99, "min": 0, "label": "0-99", "color": "#FFE4E1"},
    {"max": 499, "min": 100, "label": "100-499", "color": "#FF7F50"},
    {"max": 999, "min": 500, "label": "500-999", "color": "#F08080"},
    {"max": 4999, "min": 1000, "label": "1000-4999", "color": "#CD5C5C"},
    {"max": 9999, "min": 5000, "label": "5000-9999", "color": "#990000"},
    {"max": 9999999, "min": 10000, "label": "10000-9999999", "color": "#660000"},
]

s = (
    Map(opts.InitOpts(renderer='svg'))
    .add(series_name="累计确诊病例", data_pair=data_list_sumconf, maptype='china')
    .set_global_opts(
        title_opts=opts.TitleOpts(title='疫情地图(2020-01-25~2022-05-30)'),
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces_sumconf)
    )
)

make_snapshot(snapshot, s.render(r'C:\Users\c1533\Desktop\累计确诊地图.html'), r"C:\Users\c1533\Desktop\累计确诊地图.svg")
