from pyecharts.charts import Bar
from pyecharts import options as opts
import pymysql

job_data = []

def select_data():
    job_data.clear()
    try:
        # 打开数据库连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='bosszp_db', charset='utf8')
        # cursorclass = pymysql.cursors.DictCursor
        # 使用cursor方法创建一个游标
        cursor = conn.cursor()
        # 查询数据表数据
        sql = "SELECT city,COUNT(city) FROM t_boss_zp_info GROUP BY city"
        cursor.execute(sql)
        # 取出每部电影的类型集合
        rows = cursor.fetchall()
        for k,v in rows:
            job_data.append([k,v])
    except Exception as e:
        print(e)
        # 回滚
        conn.rollback()
    finally:
        # 关闭cursor对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
    return job_data

def show_jobnum():
    data = select_data()
    bar = Bar()
    bar.add_xaxis([i[0] for i in data])
    bar.add_yaxis('数量',[i[1] for i in data])
    bar.set_global_opts(title_opts=opts.TitleOpts(title='城市岗位数量'))
    # 生成HTML
    html = "pages/iframes/jobnum.html"
    bar.render("./templates/" + html)
if __name__ == '__main__':
    show_jobnum()