import argparse
from src.workflow import workflow
from src.utils.logger import logger

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='电商比价自动化工作流')
    parser.add_argument('input_source', help='输入源，可以是文件路径或URL')
    parser.add_argument('--output-format', choices=['excel', 'csv'], default='excel', help='输出格式')
    
    args = parser.parse_args()
    
    logger.info(f"开始处理输入源: {args.input_source}")
    logger.info(f"输出格式: {args.output_format}")
    
    # 运行工作流
    output_path = workflow.run(args.input_source, args.output_format)
    
    if output_path:
        logger.info(f"工作流运行成功，结果已导出到: {output_path}")
        print(f"\n✅ 工作流运行成功！")
        print(f"📁 结果文件: {output_path}")
    else:
        logger.error("工作流运行失败")
        print(f"\n❌ 工作流运行失败，请查看日志了解详情。")

if __name__ == '__main__':
    main()