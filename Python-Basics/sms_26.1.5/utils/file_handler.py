import json
import os
from models.student import Student

current_file_path = os.path.abspath(__file__)
utils_dir = os.path.dirname(current_file_path)
BASE_DIR = os.path.dirname(utils_dir)
DATA_DIR = os.path.join(BASE_DIR, "data")
FILENAME = os.path.join(DATA_DIR, "students.json")

def save_data(student_list):
    '''
    读取对象列表并循环, 同时将对象列表变成字典列表, 方便存入json
    '''
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f">>[系统] 创建了数据文件夹: {DATA_DIR}")

    dict_list = [one_stu.to_dict() for one_stu in student_list]
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(dict_list, f, indent=4, ensure_ascii=False)
        print(f">>存档成功，已写入{FILENAME}")
    except Exception as e:
        print(f">>[错误] 存档失败：{e}")

def load_data():
    '''
    循环读取json列表，同时将字典列表转换回对象列表，并且返回列表
    '''
    stu_list = []
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            dict_list = json.load(f)
    except Exception as e:
        print(f"[错误] 读档异常:{e}")
        return []
    except json.JSONDecodeError:
        print("[警告] 存档文件格式损坏或为空，已重置数据。")
        return []
    for one_stu in dict_list:
        stu_list.append(Student.from_dict(one_stu))
    
    print(f"[系统] 已从 {FILENAME} 加载 {len(stu_list)} 条数据")
    return stu_list