from pyecharts import options as opts
from pyecharts.charts import Funnel
import pymysql

comdata = []

def select_all():

    try:
        #打开数据库连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='bosszp_db', charset='utf8')
        #使用cursor方法创建一个游标
        cursor = conn.cursor()
        #查询数据表数据
        sql = "SELECT t.com_name,COUNT(1) FROM t_boss_zp_info t GROUP BY t.com_name ORDER BY COUNT(1) DESC LIMIT 10"
        cursor.execute(sql)
        # 取出每部电影的地区
        rows = cursor.fetchall()
        for k,v in rows:
            comdata.append([k,v])
    except Exception as e:
        print(e)
        # 回滚
        conn.rollback()
    finally:
        # 关闭cursor对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return comdata

def show_Funnel():
    data = select_all()
    funnel = Funnel()
    funnel.add(
        "企业招聘数量",
        data,
        label_opts=opts.LabelOpts(position='inside')
    )
    funnel.set_global_opts(
        title_opts=opts.TitleOpts(title="企业招聘数量排行榜TOP10", pos_left='center'),
        legend_opts=opts.LegendOpts(is_show=False)
        )
    # funnel.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    # 生成HTML
    html="pages/iframes/Funnel.html"
    funnel.render("./templates/"+html)
    return html
