from utils.history import HistoryManager
from core.classifier import FileClassifier
import os

def main_menu():
    while True:
        htma = HistoryManager()
        htma.load_log_json()

        fcer = FileClassifier(htma)
        print("[提示]输入 exit 退出循环,输入 undo 撤回操作")
        src_path = input("请输入原始路径: ").strip()
        if src_path.lower() == "exit":
            break
        if src_path.lower() == "undo":
            fcer.undo()
            continue
        if not os.path.exists(src_path):
            print(f"[错误] 路径: {src_path} 不存在，请重新输入")
            continue
        dst_path = input("请输入目标路径: ").strip()
        if dst_path.lower() == "exit":
            break
        if not os.path.exists(dst_path):
            try:
                os.makedirs(dst_path)
            except Exception as e:
                print(f"创建目标路径失败: {e}")
                continue

        file_list = os.listdir(src_path)
    
        fcer.files_get(file_list, src_path)

        fcer.to_target_folder(dst_path)

        htma.save_log_json()



