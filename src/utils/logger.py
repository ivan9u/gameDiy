from loguru import logger
import os
from src.config.config import config

# 配置日志
logger.add(
    os.path.join(config.LOG_DIR, "{time:YYYY-MM-DD}.log"),
    rotation="00:00",
    retention="7 days",
    level=config.LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

# 导出logger实例
__all__ = ['logger']