import json
import os
from core.repository import Repository

current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
data_dir = os.path.join(base_dir, "data")
filename = os.path.join(data_dir, "products.json")

class Jsonhandler:
    def __init__(self):
        os.makedirs(data_dir, exist_ok=True)
        
    def load(self):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"[系统] 已读取数据: {len(data)}条")
                return data
        except Exception as e:
            print(f"[错误] 读档异常: {e}")
            return []

    def save(self, list_data):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(list_data, f, indent=4, ensure_ascii=False)
                print(f"[系统]成功保存至:{filename}")
        except Exception as e:
            print(f"[错误] 存档失败: {e}")

        
        