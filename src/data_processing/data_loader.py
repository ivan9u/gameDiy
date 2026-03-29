import pandas as pd
import os
from bs4 import BeautifulSoup
from src.utils.http_utils import http_utils
from src.utils.logger import logger

class DataLoader:
    def load_from_file(self, file_path):
        """从文件加载商品数据"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                logger.error(f"不支持的文件格式: {file_ext}")
                return None
            
            # 标准化列名
            df = self._standardize_columns(df)
            logger.info(f"成功加载文件: {file_path}, 共 {len(df)} 条商品数据")
            return df
        except Exception as e:
            logger.error(f"加载文件失败: {str(e)}")
            return None
    
    def load_from_url(self, url):
        """从供应链网址抓取商品数据"""
        try:
            # 去除URL中的反引号和空格
            url = url.strip().strip('`')
            
            response = http_utils.get(url)
            if not response:
                return None
            
            soup = BeautifulSoup(response.text, 'lxml')
            # 这里需要根据具体的供应链网站结构进行解析
            # 以下是一个通用的示例，实际使用时需要根据具体网站调整
            products = []
            
            # 示例：假设商品信息在class为product的div中
            # 注意：这里需要根据实际网站结构调整
            for product_elem in soup.find_all('div', class_=['product', 'item', 'goods']):
                product = {
                    'product_name': self._extract_text(product_elem, ['h2', 'h3', 'h4']),
                    'specs': self._extract_text(product_elem, ['div', 'span'], ['specs', 'spec', 'details']),
                    'sku': self._extract_text(product_elem, ['div', 'span'], ['sku', 'id', 'code']),
                    'supply_price': self._extract_price(product_elem, ['div', 'span', 'p'], ['price', 'cost', 'value'])
                }
                if product['product_name']:
                    products.append(product)
            
            # 如果没有找到商品，尝试其他可能的结构
            if not products:
                # 尝试查找所有可能的商品容器
                for product_elem in soup.find_all(['div', 'li'], class_=lambda x: x and ('product' in x or 'item' in x or 'goods' in x)):
                    product = {
                        'product_name': self._extract_text(product_elem, ['h2', 'h3', 'h4']),
                        'specs': self._extract_text(product_elem, ['div', 'span'], ['specs', 'spec', 'details']),
                        'sku': self._extract_text(product_elem, ['div', 'span'], ['sku', 'id', 'code']),
                        'supply_price': self._extract_price(product_elem, ['div', 'span', 'p'], ['price', 'cost', 'value'])
                    }
                    if product['product_name']:
                        products.append(product)
            
            df = pd.DataFrame(products)
            # 标准化列名
            df = self._standardize_columns(df)
            logger.info(f"成功从URL抓取数据: {url}, 共 {len(df)} 条商品数据")
            return df
        except Exception as e:
            logger.error(f"从URL抓取数据失败: {str(e)}")
            return None
    
    def _standardize_columns(self, df):
        """标准化列名"""
        column_mapping = {
            '商品名称': 'product_name',
            '名称': 'product_name',
            '产品名称': 'product_name',
            '规格': 'specs',
            '规格参数': 'specs',
            'SKU': 'sku',
            'SKU编码': 'sku',
            '供应链价格': 'supply_price',
            '供应价格': 'supply_price',
            '价格': 'supply_price'
        }
        
        df = df.rename(columns=column_mapping)
        # 确保必要的列存在
        required_columns = ['product_name', 'specs', 'sku', 'supply_price']
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
        
        return df
    
    def _extract_text(self, elem, tags, class_names=None):
        """从HTML元素中提取文本"""
        # 确保tags是列表
        if isinstance(tags, str):
            tags = [tags]
        # 确保class_names是列表
        if class_names and isinstance(class_names, str):
            class_names = [class_names]
        
        # 尝试不同的标签和类名组合
        for tag in tags:
            if class_names:
                for class_name in class_names:
                    target = elem.find(tag, class_=class_name)
                    if target:
                        return target.text.strip()
            else:
                target = elem.find(tag)
                if target:
                    return target.text.strip()
        return None
    
    def _extract_price(self, elem, tags, class_names=None):
        """从HTML元素中提取价格"""
        text = self._extract_text(elem, tags, class_names)
        if text:
            # 提取数字部分
            import re
            price_match = re.search(r'\d+(\.\d+)?', text)
            if price_match:
                return float(price_match.group())
        return None

# 导出实例
data_loader = DataLoader()