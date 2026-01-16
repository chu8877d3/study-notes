import os
import shutil

from loguru import logger
from models.file import FileItem
from tqdm import tqdm
from utils.async_logger import AsyncLogger
from utils.history import HistoryManager
from utils.yaml import YamlParser


class FileClassifier:
    def __init__(
        self,
        history_manager: HistoryManager,
        yaml_parser: YamlParser,
        async_logger: AsyncLogger,
    ):
        self.files = []
        self.htma = history_manager
        self.config = yaml_parser
        self.aylg = async_logger

    def files_get(self, files_list, original_path):
        if len(files_list) == 0:
            return

        black_filenames = self.config.black_filenames
        black_extensions = self.config.black_filenames

        if self.config.mode:
            para = None
        else:
            para = "Others"

        for file_str in files_list:
            full_src_path = os.path.join(original_path, file_str)
            if os.path.isdir(full_src_path):
                self.aylg.async_log("DEBUG", f"忽略目录: {file_str}")
                continue
            if file_str in black_filenames:
                continue

            name, ext = os.path.splitext(file_str)
            ext = ext.lower()

            if ext in black_extensions:
                continue

            target_folder = self.config.extension_map.get(ext, para)

            if target_folder is None:
                continue

            if ext == ".ts":
                target_folder = self.classify_ts_file(full_src_path)

            file_obj = FileItem(original_path, name, ext, target_folder)
            self.files.append(file_obj)
            self.aylg.wait_complete()

    def to_target_folder(self, base_dst_path):
        self.htma.start_new_batch()
        pbar = tqdm(self.files, desc="移动文件", unit="个")

        for file_obj in self.files:
            pbar.set_postfix(file=(filename := file_obj.full_name))

            target_folder_path = os.path.join(base_dst_path, file_obj.target_folder)

            target_file_path = os.path.join(target_folder_path, filename)

            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)
                self.htma.log_mkdir(target_folder_path, file_obj.target_folder)

            if os.path.exists(target_file_path):
                self.aylg.async_log("WARNING", f"跳过同名文件: {filename}")

            try:
                shutil.move(file_obj.full_path, target_file_path)
                self.htma.log_move(file_obj.full_path, target_file_path, filename)
                self.aylg.async_log("INFO", f"移动成功: {filename}")
            except Exception as e:
                self.aylg.async_log("ERROR", f"移动失败： {filename}: {e}")
            pbar.update(1)

        pbar.close()
        self.files = []
        self.aylg.wait_complete()

    def undo(self):
        if not self.htma.log:
            logger.warning("没有可以撤回的操作记录")
            return

        last_batch_id = self.htma.get_last_batch()

        last_batch_log = []
        for item in reversed(self.htma.log):
            if item["batch_id"] == last_batch_id:
                last_batch_log.append(item)
            else:
                break

        logger.info(f"开始执行撤回操作: 共{len(file_length := last_batch_log)}个文件")
        count = 0
        pbar = tqdm(file_length, desc="撤回进度", unit="个")

        for execute in file_length:
            pbar.set_postfix(oper=(operand := execute["operand"]))
            action = execute["action"]

            match action:
                case "move":
                    current_path = execute["dst_path"]
                    original_path = execute["src_path"]
                    if not os.path.exists(current_path):
                        self.aylg.async_log("WARNING", f"文件丢失 : {operand}")
                        continue

                    if os.path.exists(original_path):
                        self.aylg.async_log("WARNING", f"跳过同名文件: {operand}")
                        continue

                    try:
                        os.makedirs(os.path.dirname(original_path), exist_ok=True)
                        shutil.move(current_path, original_path)
                        self.aylg.async_log("INFO", f"已恢复: {operand}")
                        count += 1
                    except Exception as e:
                        self.aylg.async_log("ERROR", f"撤回失败 {operand}:{e}")

                case "mkdir":
                    try:
                        os.rmdir(execute["dst_path"])
                        self.aylg.async_log("INFO", f"删除空目录: {operand}")
                        count += 1
                    except FileNotFoundError:
                        self.aylg.async_log(
                            "ERROR", f"{operand}路径不存在(可能已被手动移动)"
                        )
                    except OSError:
                        self.aylg.async_log("ERROR", f"{operand}目录非空,跳过删除")

            pbar.update(1)
        if count > 0:
            self.htma.remove_batch(last_batch_id)
            self.htma.save_log_json()
            self.aylg.async_log("SUCCESS", f"操作完成, 成功恢复 {count} 个项目")

        else:
            self.aylg.async_log("WARNING", "本次没有成功撤回任何文件")

        self.aylg.wait_complete()

    def classify_ts_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read(376)

            if len(data) < 188:
                return "Code"

            if data[0] == 0x47 and (len(data) >= 188 and data[188] == 0x47):
                return "Video"

            if b"\x00" in data:
                return "Video"

            return "Code"
        except Exception:
            return "Others"
