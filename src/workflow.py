from src.data_processing.data_loader import data_loader
from src.price_collection.price_collector import price_collector
from src.validation.result_validator import result_validator
from src.comparison.data_analyzer import data_analyzer
from src.utils.logger import logger
from src.config.config import config

class PriceComparisonWorkflow:
    def run(self, input_source, output_format='excel'):
        """运行完整的价格对比工作流"""
        try:
            logger.info("开始运行价格对比工作流")
            
            # 1. 加载商品数据
            logger.info("加载商品数据")
            if input_source.startswith('http'):
                # 从URL加载
                products = data_loader.load_from_url(input_source)
            else:
                # 从文件加载
                products = data_loader.load_from_file(input_source)
            
            if products is None or products.empty:
                logger.error("未加载到商品数据")
                return None
            
            # 2. 收集各平台价格
            logger.info("收集各平台价格")
            prices_dict = {}
            for idx, product in products.iterrows():
                product_id = idx + 1
                logger.info(f"处理商品 {product_id}: {product.get('product_name', '')}")
                
                # 收集价格
                prices = price_collector.collect_prices(product)
                
                # 验证结果
                validated_prices = result_validator.validate_results(product, prices)
                
                prices_dict[product_id] = validated_prices
            
            # 3. 分析数据
            logger.info("分析价格数据")
            df = data_analyzer.analyze(products, prices_dict)
            
            # 4. 导出结果
            logger.info(f"导出结果到 {output_format} 格式")
            if output_format == 'excel':
                output_path = data_analyzer.export_to_excel(df)
            elif output_format == 'csv':
                output_path = data_analyzer.export_to_csv(df)
            else:
                logger.error(f"不支持的输出格式: {output_format}")
                return None
            
            logger.info("价格对比工作流运行完成")
            return output_path
        except Exception as e:
            logger.error(f"工作流运行失败: {str(e)}")
            return None

# 导出实例
workflow = PriceComparisonWorkflow()