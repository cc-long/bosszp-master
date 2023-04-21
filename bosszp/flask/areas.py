from pyecharts import options as opts
from pyecharts.charts import TreeMap
from pyecharts.faker import Faker
import pymysql

area_data = []
# 查询电影上映地区与数量的关系
def select_all():
    area_data.clear()
    try:
        #打开数据库连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='bosszp_db', charset='utf8')
        #使用cursor方法创建一个游标
        cursor = conn.cursor()
        #查询数据表数据
        sql1 = "SELECT city,COUNT(1) FROM t_boss_zp_info GROUP BY city"
        sql2 = "SELECT city,district,COUNT(1) FROM t_boss_zp_info GROUP BY city,district"
        cursor.execute(sql1)
        rows1 = cursor.fetchall()
        cursor.execute(sql2)
        rows2 = cursor.fetchall()
        for row in rows1:
            info = {'name':row[0],'value':row[1],'children':[]}
            area_data.append(info)
        for row in rows2:
            children = {'name':row[1],'value':row[2]}
            for i in area_data:
                if i['name'] == row[0]:
                    i['children'].append(children)
        # 类型集合分类汇总为类型、数量列表
        # for k, v ,c in area_dict.items():
        #     area_data.append({"name": k, "value": v, 'children':c})

    except Exception as e:
        print(e)
        # 回滚
        conn.rollback()
    finally:
        # 关闭cursor对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
    return area_data

def show_areas():
    data = select_all()
    # 矩形树图初始化
    treemap = TreeMap(init_opts=opts.InitOpts(page_title="城市岗位分布"))
    # 添加数据
    treemap.add(
        series_name='city',
        data=data,
        visual_min=300,
        leaf_depth=1,
        # 标签居中
        label_opts=opts.LabelOpts(font_size=15, position="inside"),

    )
    # 全局配置
    treemap.set_global_opts(
        # 标题
        title_opts=opts.TitleOpts(
            title="招聘区域分布",pos_left='center'
        ),
        # 标签隐藏
        legend_opts=opts.LegendOpts(is_show=False)
    )
    # 生成HTML
    html = "pages/iframes/areas.html"
    treemap.render("./templates/" + html)
    return html

if __name__ == '__main__':
    show_areas()