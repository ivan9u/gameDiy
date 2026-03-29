import requests
import time
from fake_useragent import UserAgent
from src.config.config import config
from src.utils.logger import logger

class HttpUtils:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
    
    def get(self, url, headers=None, params=None, timeout=None):
        """发送GET请求"""
        if timeout is None:
            timeout = config.SEARCH_TIMEOUT
        
        # 构建请求头
        request_headers = {}
        if config.RANDOM_USER_AGENT:
            request_headers['User-Agent'] = self.ua.random
        if headers:
            request_headers.update(headers)
        
        # 发送请求
        try:
            response = self.session.get(
                url, 
                headers=request_headers, 
                params=params, 
                timeout=timeout,
                verify=False
            )
            response.raise_for_status()
            logger.debug(f"成功请求: {url}")
            # 延迟以避免反爬
            time.sleep(config.REQUEST_DELAY)
            return response
        except requests.RequestException as e:
            logger.error(f"请求失败: {url}, 错误: {str(e)}")
            return None
    
    def post(self, url, data=None, json=None, headers=None, timeout=None):
        """发送POST请求"""
        if timeout is None:
            timeout = config.SEARCH_TIMEOUT
        
        # 构建请求头
        request_headers = {}
        if config.RANDOM_USER_AGENT:
            request_headers['User-Agent'] = self.ua.random
        if headers:
            request_headers.update(headers)
        
        # 发送请求
        try:
            response = self.session.post(
                url, 
                data=data, 
                json=json, 
                headers=request_headers, 
                timeout=timeout,
                verify=False
            )
            response.raise_for_status()
            logger.debug(f"成功请求: {url}")
            # 延迟以避免反爬
            time.sleep(config.REQUEST_DELAY)
            return response
        except requests.RequestException as e:
            logger.error(f"请求失败: {url}, 错误: {str(e)}")
            return None

# 导出实例
http_utils = HttpUtils()