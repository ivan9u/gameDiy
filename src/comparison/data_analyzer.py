import pandas as pd
import os
from datetime import datetime
from src.utils.logger import logger
from src.config.config import config

class DataAnalyzer:
    def analyze(self, products, prices_dict):
        """分析商品价格数据"""
        results = []
        
        for idx, product in products.iterrows():
            product_id = idx + 1
            product_name = product.get('product_name', '')
            specs = product.get('specs', '')
            sku = product.get('sku', '')
            supply_price = product.get('supply_price', 0)
            
            # 获取该商品的价格信息
            product_prices = prices_dict.get(product_id, {})
            
            # 计算最低价平台和价格
            min_price = float('inf')
            min_price_platform = None
            for platform_key, price_info in product_prices.items():
                if price_info['price'] < min_price:
                    min_price = price_info['price']
                    min_price_platform = platform_key
            
            # 计算价格差异百分比
            price_diff_percent = 0
            if supply_price and min_price:
                price_diff_percent = ((min_price - supply_price) / supply_price) * 100
            
            # 构建结果字典
            result = {
                '商品ID': product_id,
                '商品名称': product_name,
                '规格参数': specs,
                'SKU编码': sku,
                '供应链价格': supply_price,
                '最低价平台': config.PLATFORMS.get(min_price_platform, {}).get('name', '') if min_price_platform else '',
                '最低价': min_price if min_price != float('inf') else '',
                '价格差异百分比': f"{price_diff_percent:.2f}%" if price_diff_percent else ''
            }
            
            # 添加各平台的价格信息
            for platform_key, platform_info in config.PLATFORMS.items():
                if platform_info['enabled']:
                    price_info = product_prices.get(platform_key, {})
                    result[f"{platform_info['name']}_商品标题"] = price_info.get('title', '')
                    result[f"{platform_info['name']}_价格"] = price_info.get('price', '')
                    result[f"{platform_info['name']}_图片链接"] = price_info.get('image', '')
                    result[f"{platform_info['name']}_购买链接"] = price_info.get('link', '')
            
            results.append(result)
        
        # 创建DataFrame
        df = pd.DataFrame(results)
        logger.info(f"成功生成对比表格，共 {len(df)} 条记录")
        return df
    
    def export_to_excel(self, df, filename=None):
        """导出结果到Excel文件"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"price_comparison_{timestamp}.xlsx"
        
        file_path = os.path.join(config.OUTPUT_DIR, filename)
        
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='价格对比')
                
                # 调整列宽
                worksheet = writer.sheets['价格对比']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"成功导出Excel文件: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"导出Excel文件失败: {str(e)}")
            return None
    
    def export_to_csv(self, df, filename=None):
        """导出结果到CSV文件"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"price_comparison_{timestamp}.csv"
        
        file_path = os.path.join(config.OUTPUT_DIR, filename)
        
        try:
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            logger.info(f"成功导出CSV文件: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"导出CSV文件失败: {str(e)}")
            return None

# 导出实例
data_analyzer = DataAnalyzer()