# -*- coding:utf-8 -*-

# redis数据库地址
REDIS_HOST = 'localhost'

# redis数据库端口
REDIS_PORT = 6379

# redis数据库密码
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'

# 代理分数
INITIAL_SCORE = 10
MIN_SCORE = 0
MAX_SCORE = 100

# 代理池数量界限
POOL_UPPER_THRESHOLD = 10000

# 测试网站
TEST_URL = "https://www.csdn.net"
VALID_STATUS_CODES = [200, 302]

# 最大批测试量
BATCH_TEST_SIZE = 100

# 检查周期
TESTER_CYCLE = 20

# 测试周期
GETTER_CYCLE = 20

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# api端口
API_HOST = '0.0.0.0'
API_PORT = '5555'


# 随机代理获取地址
PROXY_POOL_URL = "http://127.0.0.1:5000/random"


