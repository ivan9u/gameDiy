import re
from src.utils.http_utils import http_utils
from src.utils.logger import logger
from src.config.config import config

class ResultValidator:
    def validate_results(self, product, prices):
        """验证所有平台的搜索结果"""
        validated_prices = {}
        
        for platform_key, price_info in prices.items():
            logger.info(f"开始验证 {config.PLATFORMS[platform_key]['name']} 的搜索结果")
            
            # 验证商品规格一致性
            if not self._validate_specs(product, price_info['title']):
                logger.warning(f"{config.PLATFORMS[platform_key]['name']} 的商品规格与目标不一致")
                continue
            
            # 验证价格有效性
            if not self._validate_price(price_info['price']):
                logger.warning(f"{config.PLATFORMS[platform_key]['name']} 的价格无效")
                continue
            
            # 验证链接可访问性
            if price_info.get('link') and not self._validate_link(price_info['link']):
                logger.warning(f"{config.PLATFORMS[platform_key]['name']} 的商品链接无法访问")
                continue
            
            # 所有验证通过
            validated_prices[platform_key] = price_info
            logger.info(f"{config.PLATFORMS[platform_key]['name']} 的搜索结果验证通过")
        
        return validated_prices
    
    def _validate_specs(self, product, title):
        """验证商品规格与搜索目标的一致性"""
        # 提取商品名称和规格中的关键词
        product_keywords = self._extract_keywords(product['product_name'])
        if product['specs']:
            product_keywords.extend(self._extract_keywords(product['specs']))
        
        # 提取搜索结果标题中的关键词
        title_keywords = self._extract_keywords(title)
        
        # 计算匹配度
        matched_keywords = set(product_keywords) & set(title_keywords)
        match_ratio = len(matched_keywords) / len(product_keywords) if product_keywords else 0
        
        # 如果匹配度高于阈值，则认为规格一致
        return match_ratio >= 0.6
    
    def _validate_price(self, price):
        """验证价格信息的有效性"""
        # 价格必须是正数
        if not isinstance(price, (int, float)) or price <= 0:
            return False
        
        # 价格不能过高（根据实际情况调整阈值）
        if price > 100000:
            return False
        
        return True
    
    def _validate_link(self, link):
        """验证商品链接的可访问性和真实性"""
        try:
            # 发送HEAD请求检查链接是否可访问
            response = http_utils.get(link, timeout=10)
            if response and response.status_code < 400:
                return True
            return False
        except Exception as e:
            logger.error(f"验证链接失败: {str(e)}")
            return False
    
    def _extract_keywords(self, text):
        """从文本中提取关键词"""
        if not text:
            return []
        
        # 移除标点符号
        text = re.sub(r'[\s\p{P}\p{S}]+', ' ', text)
        
        # 分词（简单分词，实际使用时可考虑使用更复杂的分词方法）
        keywords = text.lower().split()
        
        # 过滤停用词
        stop_words = {'的', '了', '是', '在', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        keywords = [keyword for keyword in keywords if keyword not in stop_words and len(keyword) > 1]
        
        return keywords

# 导出实例
result_validator = ResultValidator()