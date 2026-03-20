from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor
import pymysql
#使用连接池机制，避免频繁创建和销毁连接
# 连接池参数说明：
# maxconnections: 最大连接数，默认0表示不限制
# mincached: 初始化时，连接池中空闲的连接数量，默认0
# maxcached: 连接池中空闲的最大连接数量，默认0表示不限制
# maxshared: 共享连接的最大数量，默认0表示不限制
# blocking: 连接数超过最大连接数时，是否阻塞等待，默认False
# maxusage: 每个连接的最大使用次数，默认None表示不限制
# setsession: 会话设置，默认[]
# ping: 连接检查间隔，默认0表示不检查
# host: 数据库主机地址，默认localhost
# port: 数据库端口号，默认3306
# user: 数据库用户名，默认root
# password: 数据库密码，默认空字符串
# database: 数据库名称，默认空字符串
# charset: 数据库字符集，默认utf8mb4
POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=5,

    blocking=True,

    setsession=[],
    ping=0,
    host='localhost',
    port=3306,
    user='root',
    password='CWB&hyd20010915',
    database='fake_orders',
    charset='utf8mb4'
)
# 封装一个查询单条数据的函数
#with语句确保在使用完连接后自动关闭连接，避免资源泄漏
#with语句确保在使用完游标后自动关闭游标，避免资源泄漏
def fetch_one(sql, params):
    with POOL.connection() as conn:
        with conn.cursor(DictCursor) as cursor:#将查询结果转换为字典格式
            cursor.execute(sql, params)
            result = cursor.fetchone()#查询单条数据
            return result


def fetch_all(sql, params):
    with POOL.connection() as conn:
        with conn.cursor(DictCursor) as cursor:#将查询结果转换为字典格式
            cursor.execute(sql, params)
            result = cursor.fetchall()#查询多条数据
            return result

def execute(sql, params):
    with POOL.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()


def update(sql, params):
    with POOL.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()
