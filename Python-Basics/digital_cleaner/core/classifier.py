import os
import shutil
from types import MappingProxyType

from models.file import FileItem
from utils.history import HistoryManager
from loguru import logger
from tqdm import tqdm

EXTENSION_MAP = MappingProxyType({
    # === Image ===
    "Image": {
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
        ".svg", ".psd", ".raw"
    },

    # === Document ===
    "Document": {
        ".txt", ".md", ".pdf", ".docx", ".xlsx",
        ".pptx", ".log"
    },

    # === Audio ===
    "Audio": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg",
        ".wma", ".m4a", ".opus", ".mid", ".ape"
    },

    # === Video ===
    "Video": {
        ".mp4", ".mkv", ".mov", ".avi", ".wmv",
        ".flv", ".webm", ".m4v", ".rmvb", ".ts"
    },

    # === Code ===
    "Code": {
        ".c", ".cpp", ".py", ".java", ".js", ".ts",
        ".html", ".css", ".php", ".go", ".rs"
    },

    # === Data ===
    "Data": {
        ".json", ".yaml", ".yml", ".xml", ".sql",
        ".csv", ".nbt", ".dat", ".db", ".sqlite"
    },

    # === Archive ===
    "Archive": {
        ".zip", ".rar", ".7z", ".tar", ".gz",
        ".bz2", ".xz"
    },

    # === Executable ===
    "Executable": {
        ".exe", ".msi", ".bat", ".sh", ".ps1",
        ".dll", ".sys", ".iso", ".com", ".bin",
        ".deb", ".rpm", ".jar"
    },

    # === Specialized ===
    "Specialized": {
        ".litematic", ".schem", ".ttf", ".otf", ".cur"
    }
})

class FileClassifier:
    def __init__(self, history_manager: HistoryManager):
        self.files = []
        self.htma = history_manager
    
    def files_get(self, files_list, original_path):
        if  len(files_list) == 0:
            return

        for file_str in files_list:
            full_src_path = os.path.join(original_path, file_str)
            if os.path.isdir(full_src_path):
                logger.info(f"忽略目录: {file_str}")
                continue

            name, ext = os.path.splitext(file_str)
            
            target_folder = "Other"
            for category, extensions in EXTENSION_MAP.items():
                if ext.lower() in extensions:
                    target_folder = category
                    break

            file_obj = FileItem(original_path, name, ext, target_folder)
            self.files.append(file_obj)

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
                logger.warning(f"跳过同名文件: {filename}")

            try:
                shutil.move(file_obj.full_path, target_file_path)
                self.htma.log_move(
                    file_obj.full_path,
                    target_file_path,
                    filename
                    )
                logger.info(f"移动成功: {filename}")
            except Exception as e:
                logger.error(f"移动失败： {filename}: {e}")
            pbar.update(1)

        pbar.close()
        self.files = []
    
    def undo(self):
        if not self.htma.log:
            logger.warning("没有可以撤回的操作记录")
            return
        
        last_batch_id = self.htma.get_last_batch()
        
        last_batch_log = []
        for item in reversed(self.htma.log):
            if item['batch_id'] == last_batch_id:
                last_batch_log.append(item)
            else:
                break
            
        logger.info(f"开始执行撤回操作: 共{len(file_length := last_batch_log)}个文件")
        count = 0
        pbar = tqdm(file_length, desc="撤回进度", unit="个")
        
        for execute in file_length:
            pbar.set_postfix(oper=(operand := execute['operand']))
            action = execute['action']
            
            match action:
                case 'move':
                    current_path = execute["dst_path"] 
                    original_path = execute["src_path"] 
                    if not os.path.exists(current_path):      
                        logger.warning(f"文件丢失 : {operand}")
                        continue
                    
                    if os.path.exists(original_path):
                        logger.warning(f"跳过同名文件: {operand}")
                        continue
                    
                    try:
                        os.makedirs(os.path.dirname(original_path), exist_ok=True)
                        shutil.move(current_path, original_path)
                        logger.info(f"已恢复: {operand}")
                        count += 1
                    except Exception as e:
                        logger.error(f"撤回失败 {operand}:{e}")
                
                case 'mkdir':
                    try:
                        os.rmdir(execute['dst_path'])
                        logger.info(f"删除空目录: {operand}")
                        count += 1
                    except FileNotFoundError:
                        logger.error(f"{operand}路径不存在(可能已被手动移动)")
                    except OSError:
                        logger.error(f"{operand}目录非空,跳过删除")                
                        
            pbar.update(1)
        if count > 0:
            self.htma.remove_batch(last_batch_id)
            self.htma.save_log_json()
            logger.success(f"操作完成, 成功恢复 {count} 个项目")
        
        else:
            logger.warning("本次没有成功撤回任何文件")