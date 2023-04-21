from pyecharts.charts import Pie
from pyecharts import options as opts
import pymysql

# 电影类型字典
genres_dict = {}
# 电影类型集合
genres_date = []

def select_data():
    genres_dict.clear()
    genres_date.clear()
    try:
        # 打开数据库连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='bosszp_db', charset='utf8')
        # cursorclass = pymysql.cursors.DictCursor
        # 使用cursor方法创建一个游标
        cursor = conn.cursor()
        # 查询数据表数据
        # sql = "SELECT com_type, ROUND(COUNT(1)/(SELECT SUM(t1.num) FROM (SELECT COUNT(1) num FROM t_boss_zp_info GROUP BY com_type) t1)*100,2) percent FROM t_boss_zp_info GROUP BY com_type"
        sql = "SELECT com_type,COUNT(1) num FROM t_boss_zp_info GROUP BY com_type"
        cursor.execute(sql)
        # 取出每部电影的类型集合
        rows = cursor.fetchall()
        for row in rows:
            genres = row[0].split('/')
            # 电影类型分类汇总
            for j in range(len(genres)):
                if genres[j] in genres_dict.keys():
                    genres_dict[genres[j]] = genres_dict[genres[j]] + row[1]
                else:
                    genres_dict[genres[j]] = row[1]
        # 类型集合分类汇总为类型、数量列表
        for k, v in genres_dict.items():
            genres_date.append({v,k})
        # print(genres_date)
    except Exception as e:
        print(e)
        # 回滚
        conn.rollback()
    finally:
        # 关闭cursor对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
    return genres_date


# 生成pyecharts图
def show_genres():
    data=select_data()
    # 扇形树图初始化
    pie = Pie(init_opts=opts.InitOpts(page_title="企业类型分析"))
    # 添加数据
    pie.add(
        'Business',
        data,
        # 标签居中
        label_opts=opts.LabelOpts(font_size=15, position="inside"),
    )
    # 全局配置
    pie.set_global_opts(
        # 标题
        title_opts=opts.TitleOpts(
            title="企业类型分析", pos_left='center'
        ),
        # 标签隐藏
        legend_opts=opts.LegendOpts(is_show=False)
    )
    # 生成HTML
    html="pages/iframes/genres.html"
    pie.render("./templates/"+html)
    return html


