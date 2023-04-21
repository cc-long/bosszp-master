from pyecharts.charts import WordCloud
from pyecharts import options as opts
import pymysql

wcdict = {}
wcdata = []

def select_data():
    wcdata.clear()
    wcdict.clear()
    try:
        # 打开数据库连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='bosszp_db', charset='utf8')
        # cursorclass = pymysql.cursors.DictCursor
        # 使用cursor方法创建一个游标
        cursor = conn.cursor()
        # 查询数据表数据
        sql = "SELECT job_benefits FROM t_boss_zp_info"
        cursor.execute(sql)
        # 取出每部电影的类型集合
        rows = cursor.fetchall()
        for row in rows:
            for word in str(row[0]).split('、'):
                if word not in wcdict:
                    wcdict[word] = 1
                else:
                    wcdict[word] += 1
        # 类型集合分类汇总为类型、数量列表
        for k,v in wcdict.items():
            wcdata.append((k,v))
    except Exception as e:
        print(e)
        # 回滚
        conn.rollback()
    finally:
        # 关闭cursor对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
    return wcdata

# 生成pyecharts图
def show_wordCloud():
    data=select_data()

    wc = WordCloud(init_opts=opts.InitOpts(page_title="企业类型分析"))

    wc.add(
        series_name='岗位福利分析',
        word_size_range=[6,66],

        data_pair = data,
    )
    # 全局配置
    wc.set_global_opts(
        # 标题
        title_opts=opts.TitleOpts(
            title="岗位福利分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True)
    )
    # 生成HTML
    html="pages/iframes/wordCloud.html"
    wc.render("./templates/"+html)
    return html

