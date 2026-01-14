from cli.main_menu import main_menu
from loguru import logger

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        logger.error(f"程序发生严重错误: {e}")
    finally:
        input("\n>>>程序运行结束, 按回车键退出...")