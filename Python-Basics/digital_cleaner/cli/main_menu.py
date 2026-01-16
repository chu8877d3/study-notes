import os

from colorama import Fore, Style, init
from core.classifier import FileClassifier
from loguru import logger
from tqdm import tqdm
from utils.async_logger import AsyncLogger
from utils.history import HistoryManager
from utils.yaml import YamlParser

init(autoreset=True)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def help_list():
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "       ✨ Digital Cleaner 文件整理助手 v1.0")
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Fore.YELLOW + "功能指令: ")
    print(Fore.GREEN + "  [路径] " + Fore.WHITE + "直接输入路径开始整理")
    print(Fore.GREEN + "  [undo] " + Fore.WHITE + "撤回上一次操作")
    print(Fore.GREEN + "  [exit] " + Fore.WHITE + "退出程序")
    print(Style.DIM + "-" * 50)


def main_menu():
    aylg = AsyncLogger()
    htma = HistoryManager()
    ympr = YamlParser()

    htma.load_log_json()
    logger.remove()
    logger.add(
        lambda msg: tqdm.write(msg, end=""),
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>",
        enqueue=True,
    )

    while True:
        clear_screen()
        help_list()

        fcer = FileClassifier(htma, ympr, aylg)

        print(Fore.YELLOW + "\n请输入原始路径 (支持多路径, 用空格或逗号隔开):")
        user_input = input(Fore.CYAN + ">>>" + Style.RESET_ALL).strip()

        if user_input.lower() == "exit":
            print(Fore.MAGENTA + "再见")
            break

        if user_input.lower() == "undo":
            print(Fore.YELLOW + "正在读取撤回记录...")
            fcer.undo()
            input(Fore.WHITE + "\n按回车键继续...")
            continue

        if not user_input:
            continue

        raw_path = user_input.replace(",", " ").split()
        src_paths = []

        for p in raw_path:
            clean_path = p.strip('"').strip("'")
            if os.path.exists(clean_path):
                src_paths.append(clean_path)
            else:
                logger.warning(f"路径不存在, 已忽略: {clean_path}")

        if not src_paths:
            input(Fore.RED + "未检测到有效路径, 按回车重试...")
            continue

        print(
            Fore.YELLOW + "\n请输入目标路径 (留空则默认在第一个源路径下创建'Sorted'):"
        )
        dst_input = input(Fore.CYAN + ">>>" + Style.RESET_ALL).strip().strip('"')

        if dst_input.lower() == "exit":
            print(Fore.MAGENTA + "再见")
            break

        if not dst_input:
            dst_path = os.path.join(src_paths[0], "Sorted")
            logger.info(f"使用默认目标路径: {dst_path}")
        else:
            dst_path = dst_input

        if not os.path.exists(dst_path):
            try:
                os.makedirs(dst_path)
            except Exception as e:
                logger.error(f"创建路径失败: {e}")
                input("按回车继续...")
                continue
        print(Fore.GREEN + "\n任务开始...")

        has_files = False
        for src in src_paths:
            file_list = os.listdir(src)
            if file_list:
                has_files = True
                fcer.files_get(file_list, src)

        if has_files:
            fcer.to_target_folder(dst_path)
            htma.save_log_json()
            print(Fore.GREEN + "\n 整理完成!")
        else:
            logger.warning("所选目录下没有可以处理的文件")

        input(Style.DIM + "\n按回车键开始新任务...")
