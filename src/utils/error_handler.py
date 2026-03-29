from src.utils.logger import logger

class PriceComparisonError(Exception):
    """价格对比工作流的基础异常类"""
    pass

class DataLoadError(PriceComparisonError):
    """数据加载错误"""
    pass

class PriceCollectionError(PriceComparisonError):
    """价格采集错误"""
    pass

class ValidationError(PriceComparisonError):
    """验证错误"""
    pass

class ExportError(PriceComparisonError):
    """导出错误"""
    pass

def handle_error(func):
    """错误处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PriceComparisonError as e:
            logger.error(f"工作流错误: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            raise PriceComparisonError(f"未知错误: {str(e)}") from e
    return wrapper