# 数据库配置信息

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'bosszp_db'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


# MAIL_SERVER = 'smtp.qq.com'
# MAIL_USE_SSL = True
# MAIL_PORT = 465
# MAIL_USERNAME = '2252100656@qq.com'
# MAIL_PASSWORD = 'izczlxqxnmgjdjjh'
# MAIL_DEFAULT_SENDER = '2252100656@qq.com'

SECRET_KEY = "asdfsaadfdfgx"