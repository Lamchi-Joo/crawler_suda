from random import randrange
from flask import Flask, render_template, request, redirect, render_template, session
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Liquid, Line, Radar
from pyecharts.faker import Faker
from pyecharts.globals import SymbolType
from pyecharts.charts import WordCloud
from pyecharts.charts import Funnel

app = Flask(__name__)

app.secret_key = 'QWERTYUIOP'  # 对用户信息加密


@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'admin' and pwd == '123':
        session['user_info'] = user
        return redirect('/index')
    else:
        return render_template('login.html', msg='用户名或密码输入错误')


def bar_base():
    bar = Bar()
    bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    bar.add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
    bar.add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
    bar.set_global_opts(title_opts=opts.TitleOpts())
    return bar


def pie_base():
    pie = Pie()
    pie.add(
        "",
        [list(z) for z in zip(Faker.choose(), Faker.values())],
        radius=["40%", "55%"],
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
            background_color="#eee",
            border_color="#aaa",
            border_width=1,
            border_radius=4,
            rich={
                "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                "abg": {
                    "backgroundColor": "#e3e3e3",
                    "width": "100%",
                    "align": "right",
                    "height": 22,
                    "borderRadius": [4, 4, 0, 0],
                },
                "hr": {
                    "borderColor": "#aaa",
                    "width": "100%",
                    "borderWidth": 0.5,
                    "height": 0,
                },
                "b": {"fontSize": 16, "lineHeight": 33},
                "per": {
                    "color": "#eee",
                    "backgroundColor": "#334455",
                    "padding": [2, 4],
                    "borderRadius": 2,
                },
            },
        ),
    )
    pie.set_global_opts(title_opts=opts.TitleOpts())
    return pie


def pie_diamond():
    liquid = Liquid()
    liquid.add("lq", [0.3, 0.7], is_outline_show=False, shape=SymbolType.DIAMOND)
    liquid.set_global_opts(title_opts=opts.TitleOpts())
    return liquid


def funnel():
    funnel = Funnel()
    funnel.add(
        "商品",
        [list(z) for z in zip(Faker.choose(), Faker.values())],
        sort_="ascending",
        label_opts=opts.LabelOpts(position="inside"),
    )
    funnel.set_global_opts(title_opts=opts.TitleOpts())
    return funnel


def line_areastyle_boundary_gap():
    line = Line()
    line.add_xaxis(Faker.choose())
    line.add_yaxis("商家A", Faker.values(), is_smooth=True)
    line.set_series_opts(areastyle_opts=opts.AreaStyleOpts(opacity=0.5), label_opts=opts.LabelOpts(is_show=False), )
    line.set_global_opts(title_opts=opts.TitleOpts(title="Line-面积图"),
                         xaxis_opts=opts.AxisOpts(
                             axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                             is_scale=False,
                             boundary_gap=False,
                         ),)
    return line


def word_cloud_diamond():
    words = [
        ("Sam S Club", 10000),
        ("Macys", 6181),
        ("Amy Schumer", 4386),
        ("Jurassic World", 4055),
        ("Charter Communications", 2467),
        ("Chick Fil A", 2244),
        ("Planet Fitness", 1868),
        ("Pitch Perfect", 1484),
        ("Express", 1112),
        ("Home", 865),
        ("Johnny Depp", 847),
        ("Lena Dunham", 582),
        ("Lewis Hamilton", 555),
        ("KXAN", 550),
        ("Mary Ellen Mark", 462),
        ("Farrah Abraham", 366),
        ("Rita Ora", 360),
        ("Serena Williams", 282),
        ("NCAA baseball tournament", 273),
        ("Point Break", 265),
    ]
    word_cloud = WordCloud()
    word_cloud.add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    word_cloud.set_global_opts(title_opts=opts.TitleOpts())
    return word_cloud


def radar_selected_mode():
    v1 = [[4300, 10000, 28000, 35000, 50000, 19000]]
    v2 = [[5000, 14000, 28000, 31000, 42000, 21000]]
    radar = Radar()
    radar.add_schema(
            schema=[
                opts.RadarIndicatorItem(name="销售", max_=6500, color="#0f0f10"),
                opts.RadarIndicatorItem(name="管理", max_=16000, color="#0f0f10"),
                opts.RadarIndicatorItem(name="信息技术", max_=30000, color="#0f0f10"),
                opts.RadarIndicatorItem(name="客服", max_=38000, color="#0f0f10"),
                opts.RadarIndicatorItem(name="研发", max_=52000, color="#0f0f10"),
                opts.RadarIndicatorItem(name="市场", max_=25000, color="#0f0f10"),
            ]
        )
    radar.add("预算分配", v1)
    radar.add("实际开销", v2)
    radar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    radar.set_global_opts(legend_opts=opts.LegendOpts(selected_mode="single"), title_opts=opts.TitleOpts(),)
    return radar


@app.route("/index")
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    return render_template("index.html")


@app.route("/bar_chart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


@app.route("/pie_chart")
def get_pie_chart():
    c = pie_base()
    return c.dump_options_with_quotes()


@app.route("/diamond")
def get_diamond():
    c = pie_diamond()
    return c.dump_options_with_quotes()


@app.route("/funnel")
def get_funnel():
    c = funnel()
    return c.dump_options_with_quotes()


@app.route("/line_areastyle_boundary_gap")
def get_line_areastyle_boundary_gap():
    c = line_areastyle_boundary_gap()
    return c.dump_options_with_quotes()


@app.route("/word_cloud_diamond")
def get_lword_cloud_diamond():
    c = word_cloud_diamond()
    return c.dump_options_with_quotes()


@app.route("/radar_selected_mode")
def get_radar_selected_mode():
    c = radar_selected_mode()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run()
