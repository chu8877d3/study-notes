import os

from core.classifier import FileClassifier
from loguru import logger
from tqdm import tqdm
from utils.history import HistoryManager
from utils.yaml import YamlParser


def main_menu():
    htma = HistoryManager()
    ympr = YamlParser()
    htma.load_log_json()
    logger.remove()
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
    while True:
        src_paths = []
        fcer = FileClassifier(htma, ympr)
        logger.info(
            "\n[提示]输入 exit 退出循环\n,输入 undo\n撤回操作,输入stop停止多源路径输入\n "
        )
        first_path = input("请输入原始路径: ").strip()
        if first_path.lower() == "exit":
            break
        if first_path.lower() == "undo":
            fcer.undo()
            continue
        if not os.path.exists(first_path):
            logger.warning(f"路径: {first_path} 不存在，请重新输入")
            continue
        src_paths.append(first_path)
        while True:
            current_path = input("继续输入路径:)").strip()
            if current_path.lower() == "stop":
                break
            if not os.path.exists(current_path):
                logger.warning(f"路径: {current_path} 不存在，请重新输入")
                continue
            src_paths.append(current_path)
        dst_path = input("请输入目标路径: ").strip()
        if dst_path.lower() == "exit":
            break
        if not os.path.exists(dst_path):
            try:
                os.makedirs(dst_path)
            except Exception as e:
                logger.error(f"创建目标路径失败: {e}")
                continue
        for src_path in src_paths:
            file_list = os.listdir(src_path)

            fcer.files_get(file_list, src_path)

            fcer.to_target_folder(dst_path)

            htma.save_log_json()
