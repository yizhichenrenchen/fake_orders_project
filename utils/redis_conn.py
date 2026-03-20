import redis
import json
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
REDIS_CONN = redis.Redis(connection_pool=POOL)
#使用全局的REDIS连接对象，避免频繁创建和销毁连接
# 这样可以提高性能，减少资源泄漏


def push_data(key, **values):
    value = json.dumps(values)
#这里使用lpush方法准备将数据传入redis队列中，并且使用json.dumps方法将数据序列化为json格式
    REDIS_CONN.lpush(key, value)
    print(f"数据已入队列: {key}, {values}")

def pop_data(key):
    value = REDIS_CONN.brpop(key, timeout=10)
    if value:
        value_data = value[1]
        logging.info(f"获取到数据: {key}, {value_data}, {type(value_data)}")
        value_load = json.loads(value_data)
        logging.info(f"获取到数据信息: {value_load}, {type(value_load)}")
        return value_load

    return None
