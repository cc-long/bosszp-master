from flask import Flask
from flask import request, redirect
from flask import render_template, url_for
from flask_paginate import Pagination
from sqlalchemy import create_engine,Column,Integer,SmallInteger,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from genres import show_genres
from dbutils import DBUtils
# from list_data import select_score, select_showtime, select_genres, select_areas, film_data
from areas import show_areas
from edunum import show_edunum
from Funnel import show_Funnel
from wordCloud import show_wordCloud
from Bar import show_jobnum

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

#初始化数据库连接
def get_db_conn():
    """
    获取数据库连接
    :return: db_conn 数据库连接对象
    """
    return DBUtils(host='localhost', user='root', password='root', db='bosszp_db')

#创建缓存对象
engine = get_db_conn()
Session =sessionmaker(bind=engine)
session =Session
#声明基类
Base = declarative_base()
#定义Film对象
#基于这个基类来创建我们的自定义类，一个类就是一个数据库表；
class Film(Base):
    #表的名字
    __tablename__= 'boss_zp'
    #表的结构
    id = Column(Integer,primary_key=True,autoincrement=True)
    job_name =Column(String(250))
    com_name =Column(String(50))
    com_type =Column(String)
    com_size =Column(Integer)
    finance_stage =Column(Integer)
    work_year =Column(Integer)
    education =Column(String(20))
    job_benefits =Column(String(50))
    salary_lower =Column(String(50))
    salary_high =Column(String(50))
    city = Column(String(50))
    district = Column(String(50))
    street = Column(String(50))

@app.route('/')
def index():
    # return render_template('pages/echarts/e1.html')
    # return render_template('index.html')
    return render_template('login.html')


@app.route('/welcome')
def welcome():
    return render_template('pages/welcome.html')


@app.route("/page_none")
def page_none():
    return render_template('page_none')

# 验证用户名和密码
@app.route('/login', methods=['POST'])
@app.route('/index')
def login():
    # 需要从request对象读取表单内容：
    if request.form['username'] == 'admin' and request.form['password'] == '123456':
        return render_template('index.html')

# 表单list
# @app.route("/list")
# @app.route("/list/")
# def list(limit=10):
#     # 列表属性
#     alldata = DBUtils.get_all("select * from t_boss_zp_info")
#     # 分页
#     limit = 15
#     page = int(request.args.get("page", 1))
#     start = (page - 1) * limit
#     if request.args.get("low") or request.args.get("high") or request.args.get("showtime") or request.args.get("areas") or request.args.get("genres") or request.args.get("filmname"):
#         # 参数选择
#         r_low = request.args.get("low")
#         r_high = request.args.get("high")
#         r_showtime = request.args.get("showtime")
#         r_genres = request.args.get("genres")
#         r_areas = request.args.get("areas")
#         r_filmname = request.args.get("filmname")
#         # 返回数据
#         print("参数：{},{},{},{},{}".format(r_low, r_high, r_showtime, r_genres, r_areas,r_filmname))
#         print("参数1：{}".format(type(r_low)))
#         print("参数2：{}".format(len(r_low)))
#         r_films = film_data(low=r_low, high=r_high, showtime=r_showtime, genres=r_genres, areas=r_areas, filmname=r_filmname)[0]
#         r_row = film_data(low=r_low, high=r_high, showtime=r_showtime, genres=r_genres, areas=r_areas, filmname=r_filmname)[1]
#         # 分页
#         r_end = page * limit if r_row > page * limit else r_row
#         r_paginate = Pagination(page=page, total=r_row)
#         r_ret = r_films[start:r_end]
#         return render_template('pages/order/list.html', ID=ID, job_name=job_name, com_name=com_name, com_type=com_type,
#         com_size=com_size,finance_stage=finance_stage, work_year=work_year, education=education,job_benefits=job_benefits,salary_lower=salary_benefits,
#         salary_high =salary_high, city=city, district=district,street, films=r_ret, row=r_row,paginate=r_paginate)
#     else:
#         # 返回数据
#         films = film_data()[0]
#         row = film_data()[1]
#         end = page * limit if row > page * limit else row
#         paginate = Pagination(page=page, total=row)
#         ret=films[start:end]
#         print("res:{}".format(ret))
#         return render_template('pages/order/list.html', low=t_low, high=t_high, showtime=t_showtime, genres=t_genres,
#                            areas=t_areas, films=ret,row=row, paginate=paginate)



# Pie e1
@app.route("/e1",methods=['GET'])
def e1():
    return render_template('pages/echarts/e1.html')

@app.route("/genres")
def genres():
    show_genres()
    return render_template('pages/iframes/genres.html')

# Treemap e2
@app.route("/e2",methods=['GET'])
def e2():
    return render_template('pages/echarts/e2.html')

@app.route("/areas")
def areas():
    show_areas()
    return render_template('pages/iframes/areas.html')

# Pie e3
@app.route("/e3",methods=['GET'])
def e3():
    return render_template('pages/echarts/e3.html')

@app.route("/edunum")
def edunum():
    show_edunum()
    return render_template('pages/iframes/edunum.html')

# Funnel e4
@app.route("/e4",methods=['GET'])
def e4():
    return render_template('pages/echarts/e4.html')

@app.route("/Funnel")
def Funnel():
    show_Funnel()
    return render_template('pages/iframes/Funnel.html')

# 时间轴图e5
@app.route("/e5",methods=['GET'])
def e5():
    return render_template('pages/echarts/e5.html')

@app.route("/wordCloud")
def wordCloud():
    show_wordCloud()
    return render_template('pages/iframes/wordCloud.html')

# @app.route("/scores")
# def scores():
#     return render_template('pages/iframes/score_top.html')
#
# @app.route("/comments")
# def comments():
#     return render_template('pages/iframes/comment_top.html')
#
# 饼状图e6
@app.route("/e6",methods=['GET'])
def e6():
    return render_template('pages/echarts/e6.html')

@app.route("/jobnum")
def jobnum():
    show_jobnum()
    return render_template('pages/iframes/jobnum.html')
#
# @app.route("/group_url")
# def group_url():
#     return render_template('pages/iframes/showtime_group.html')
#
# # 词云图e7
# @app.route("/e7",methods=['GET'])
# def e7():
#     return render_template('pages/echarts/e7.html', switch_url=url_for('page_none'))

@app.route("/searchs")
@app.route("/searchs/")
def searchs():
    # if request.args.get("search") == "" or request.args.get("cut") == "":
    #     return redirect("/e7")
    # else:
    #     search = request.args.get("search")
    #     cut = int(request.args.get("cut"))
    #     film_search(search, cut)
        return render_template('pages/echarts/e7.html', search_url=url_for('search_url'))

@app.route("/search_url")
def search_url():
    return render_template('pages/iframes/film_search.html')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
