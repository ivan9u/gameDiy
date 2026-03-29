import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目配置
class Config:
    # 数据输入配置
    INPUT_FORMATS = ['csv', 'excel']
    
    # 电商平台配置
    PLATFORMS = {
        'manmanbuy': {
            'name': '慢慢买',
            'search_url': 'https://www.manmanbuy.com/searchnew.aspx?key={}',
            'enabled': True
        },
        'pinduoduo': {
            'name': '拼多多',
            'search_url': 'https://mobile.yangkeduo.com/search_result.html?search_key={}',
            'enabled': True
        },
        'fanli': {
            'name': '返利网',
            'search_url': 'https://www.fanli.com/search/?keyword={}',
            'enabled': True
        }
    }
    
    # 搜索配置
    SEARCH_RETRY_LIMIT = 3
    SEARCH_TIMEOUT = 30
    
    # 验证配置
    VALIDATION_RETRY_LIMIT = 2
    
    # 反爬配置
    USE_PROXIES = False
    RANDOM_USER_AGENT = True
    REQUEST_DELAY = 2  # 秒
    
    # 输出配置
    OUTPUT_FORMATS = ['excel', 'csv']
    OUTPUT_DIR = 'output'
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_DIR = 'logs'

# 初始化配置
config = Config()

# 创建必要的目录
os.makedirs(config.OUTPUT_DIR, exist_ok=True)
os.makedirs(config.LOG_DIR, exist_ok=True)