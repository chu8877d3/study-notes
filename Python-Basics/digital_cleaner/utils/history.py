from models.file import FileItem
from datetime import datetime
import uuid
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)

class HistoryManager:
    def __init__(self):
        self.log = []
        self.filename = os.path.join(base_dir, "log.json")

    def get_now(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")  
        
    
    def save_log_json(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.log, f, indent=4, ensure_ascii=False )
                print(f"{self.filename}已存入:{base_dir}")
        except Exception as e:
            print(f"{self.filename}创建失败: {e}")

    def load_log_json(self):
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.log = json.load(f)
        except Exception as e:
            print(f"日志读取失败: {e}")
        
    def append_log_list(self, src_path, dst_path, filename):
        log_time = self.get_now()
        uid = str(uuid.uuid4())
        one_log =  {
            'uuid': uid,
            'Operand': filename,
            'time': log_time,
            'src_path': src_path,
            'dst_path': dst_path
        }
        self.log.append(one_log)

        
        