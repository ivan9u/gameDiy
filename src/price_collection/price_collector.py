import urllib.parse
from bs4 import BeautifulSoup
from src.utils.http_utils import http_utils
from src.utils.logger import logger
from src.config.config import config

class PriceCollector:
    def __init__(self):
        self.platform_collectors = {
            'manmanbuy': self._collect_manmanbuy,
            'pinduoduo': self._collect_pinduoduo,
            'fanli': self._collect_fanli
        }
    
    def collect_prices(self, product):
        """为单个商品收集各平台价格"""
        prices = {}
        
        # 构建搜索关键词
        search_keyword = self._build_search_keyword(product)
        logger.info(f"为商品 '{product['product_name']}' 构建搜索关键词: {search_keyword}")
        
        # 遍历启用的平台
        for platform_key, platform_info in config.PLATFORMS.items():
            if platform_info['enabled']:
                logger.info(f"开始在 {platform_info['name']} 上搜索商品")
                try:
                    price_info = self.platform_collectors[platform_key](search_keyword, product)
                    if price_info:
                        prices[platform_key] = price_info
                        logger.info(f"在 {platform_info['name']} 上找到价格: {price_info['price']}")
                    else:
                        logger.warning(f"在 {platform_info['name']} 上未找到商品")
                except Exception as e:
                    logger.error(f"在 {platform_info['name']} 上搜索失败: {str(e)}")
        
        return prices
    
    def _build_search_keyword(self, product):
        """构建搜索关键词"""
        keyword = product['product_name']
        if product['specs']:
            keyword += f" {product['specs']}"
        return keyword
    
    def _collect_manmanbuy(self, keyword, product):
        """从慢慢买收集价格"""
        search_url = config.PLATFORMS['manmanbuy']['search_url'].format(
            urllib.parse.quote(keyword)
        )
        
        response = http_utils.get(search_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, 'lxml')
        # 这里需要根据慢慢买的页面结构进行解析
        # 以下是示例代码，实际使用时需要调整
        products = []
        
        # 示例：假设商品列表在class为search-result的div中
        for item in soup.find_all('div', class_='search-result-item'):
            # 提取商品信息
            title = self._extract_text(item, 'h3')
            price = self._extract_price(item, 'span', 'price')
            link = self._extract_link(item, 'a')
            image = self._extract_image(item, 'img')
            
            if title and price:
                products.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'image': image
                })
        
        # 按价格排序，返回最低价
        if products:
            products.sort(key=lambda x: x['price'])
            return products[0]
        return None
    
    def _collect_pinduoduo(self, keyword, product):
        """从拼多多收集价格"""
        search_url = config.PLATFORMS['pinduoduo']['search_url'].format(
            urllib.parse.quote(keyword)
        )
        
        response = http_utils.get(search_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, 'lxml')
        # 这里需要根据拼多多的页面结构进行解析
        # 以下是示例代码，实际使用时需要调整
        products = []
        
        # 示例：假设商品列表在class为goods-list的div中
        for item in soup.find_all('div', class_='goods-item'):
            # 提取商品信息
            title = self._extract_text(item, 'div', 'goods-title')
            price = self._extract_price(item, 'div', 'goods-price')
            link = self._extract_link(item, 'a')
            image = self._extract_image(item, 'img')
            
            if title and price:
                products.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'image': image
                })
        
        # 按价格排序，返回最低价
        if products:
            products.sort(key=lambda x: x['price'])
            return products[0]
        return None
    
    def _collect_fanli(self, keyword, product):
        """从返利网收集价格"""
        search_url = config.PLATFORMS['fanli']['search_url'].format(
            urllib.parse.quote(keyword)
        )
        
        response = http_utils.get(search_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, 'lxml')
        # 这里需要根据返利网的页面结构进行解析
        # 以下是示例代码，实际使用时需要调整
        products = []
        
        # 示例：假设商品列表在class为search-results的div中
        for item in soup.find_all('div', class_='product-item'):
            # 提取商品信息
            title = self._extract_text(item, 'h4')
            price = self._extract_price(item, 'span', 'price')
            link = self._extract_link(item, 'a')
            image = self._extract_image(item, 'img')
            
            if title and price:
                products.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'image': image
                })
        
        # 按价格排序，返回最低价
        if products:
            products.sort(key=lambda x: x['price'])
            return products[0]
        return None
    
    def _extract_text(self, elem, tag, class_name=None):
        """从HTML元素中提取文本"""
        if class_name:
            target = elem.find(tag, class_=class_name)
        else:
            target = elem.find(tag)
        return target.text.strip() if target else None
    
    def _extract_price(self, elem, tag, class_name=None):
        """从HTML元素中提取价格"""
        text = self._extract_text(elem, tag, class_name)
        if text:
            # 提取数字部分
            import re
            price_match = re.search(r'\d+(\.\d+)?', text)
            if price_match:
                return float(price_match.group())
        return None
    
    def _extract_link(self, elem, tag, class_name=None):
        """从HTML元素中提取链接"""
        if class_name:
            target = elem.find(tag, class_=class_name)
        else:
            target = elem.find(tag)
        return target.get('href') if target else None
    
    def _extract_image(self, elem, tag, class_name=None):
        """从HTML元素中提取图片链接"""
        if class_name:
            target = elem.find(tag, class_=class_name)
        else:
            target = elem.find(tag)
        return target.get('src') if target else None

# 导出实例
price_collector = PriceCollector()