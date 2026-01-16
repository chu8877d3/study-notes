import json
import os
import sys
import uuid
from datetime import datetime

from loguru import logger

if getattr(sys, "frozen", False):
    base_dir = os.path.dirname(sys.executable)
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
file_name = "log.json"
file_path = os.path.join(base_dir, file_name)


class HistoryManager:
    def __init__(self):
        self.log = []
        self.filename = file_path
        self.current_batch_id = None

    def start_new_batch(self):
        self.current_batch_id = str(uuid.uuid4())

    def get_now(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def get_last_batch(self):
        try:
            last_action = self.log[-1]
            last_batch_id = last_action.get("batch_id")
            if not last_batch_id:
                logger.warning("日志记录格式旧, 无法按批次撤回")
                return
            return last_batch_id
        except IndexError:
            return

    def remove_batch(self, batch_id):
        self.log = [item for item in self.log if item["batch_id"] != batch_id]

    def save_log_json(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.log, f, indent=4, ensure_ascii=False)
                logger.debug(f"{self.filename}已存入:{base_dir}")
        except Exception as e:
            logger.warning(f"{self.filename}日志保存失败: {e}")

    def load_log_json(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, encoding="utf-8") as f:
                self.log = json.load(f)
        except Exception as e:
            logger.error(f"日志读取失败: {e}")

    def append_log(self, action, src_path, dst_path, operand):
        if not self.current_batch_id:
            self.start_new_batch()

        log_time = self.get_now()
        record = {
            "batch_id": self.current_batch_id,
            "action": action,
            "time": log_time,
            "operand": operand,
            "src_path": src_path,
            "dst_path": dst_path,
        }
        self.log.append(record)

    def log_move(self, src_path, dst_path, filename):
        self.append_log("move", src_path, dst_path, filename)

    def log_mkdir(self, dst_path, folder):
        self.append_log("mkdir", None, dst_path, folder)
