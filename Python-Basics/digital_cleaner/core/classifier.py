import os
import shutil
from models.file import FileItem
class FileClassifier:
    def __init__(self, history_manager):
        self.files = []
        self.htma = history_manager
        self.EXTENSION_MAP = {
        # === Image ===
        '.jpg': 'Image', '.jpeg': 'Image', '.png': 'Image', '.gif': 'Image',
        '.webp': 'Image', '.svg': 'Image', '.psd': 'Image', '.raw': 'Image',
    
        # === Document ===
        '.txt': 'Document', '.md': 'Document', '.pdf': 'Document', '.docx': 'Document',
        '.xlsx': 'Document', '.pptx': 'Document', '.log': 'Document',
    
        # === Audio ===
        '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio', '.aac': 'Audio',
        '.ogg': 'Audio', '.wma': 'Audio', '.m4a': 'Audio', '.opus': 'Audio',
        '.mid': 'Audio', '.ape': 'Audio',
    
        # === Video ===
        '.mp4': 'Video', '.mkv': 'Video', '.mov': 'Video', '.avi': 'Video',
        '.wmv': 'Video', '.flv': 'Video', '.webm': 'Video', '.m4v': 'Video',
        '.rmvb': 'Video', '.ts': 'Video',
    
        # === Code ===
        '.c': 'Code', '.cpp': 'Code', '.py': 'Code', '.java': 'Code',
        '.js': 'Code', '.ts': 'Code', '.html': 'Code', '.css': 'Code',
        '.php': 'Code', '.go': 'Code', '.rs': 'Code',
    
        # === Data  ===
        '.json': 'Data', '.yaml': 'Data', '.yml': 'Data', '.xml': 'Data',
        '.sql': 'Data', '.csv': 'Data', '.nbt': 'Data', '.dat': 'Data',
        '.db': 'Data', '.sqlite': 'Data',
    
        # === Archive ===
        '.zip': 'Archive', '.rar': 'Archive', '.7z': 'Archive', '.tar': 'Archive',
        '.gz': 'Archive', '.bz2': 'Archive', '.xz': 'Archive',
    
        # === Executable ) ===
        '.exe': 'Executable', '.msi': 'Executable', '.bat': 'Executable',
        '.sh': 'Executable', '.ps1': 'Executable', '.dll': 'Executable',
        '.sys': 'Executable', '.iso': 'Executable', '.com': 'Executable',
        '.bin': 'Executable', '.deb': 'Executable', '.rpm': 'Executable',
        '.jar': 'Executable',
    
        # === Specialized  ===
        '.litematic': 'Specialized', '.schem': 'Specialized',
        '.ttf': 'Specialized', '.otf': 'Specialized', '.cur': 'Specialized'
    }
   
    def files_get(self, files_list, original_path):
        if  len(files_list) == 0:
            return
        
        for file_str in files_list:
            full_src_path = os.path.join(original_path, file_str)
            if os.path.isdir(full_src_path):
                print(f"[忽略目录] {file_str}")
                continue

            name, ext = os.path.splitext(file_str)

            target_folder = self.EXTENSION_MAP.get(ext.lower(), "Others")
            file_obj = FileItem(original_path, name, ext, target_folder)
            self.files.append(file_obj)
    
    def to_target_folder(self, base_dst_path):
        for file_obj in self.files:
            
            filename = file_obj.basename + file_obj.ext

            original_full_path = os.path.join(file_obj.parent, filename)

            target_folder_path = os.path.join(base_dst_path, file_obj.target_folder)

            target_file_path = os.path.join(target_folder_path, filename)

            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)
            if not os.path.exists(target_file_path):
                try:
                    shutil.move(original_full_path, target_file_path)
                    self.htma.append_log_list(original_full_path, target_file_path, filename)
                    print(f"移动成功: {filename}")
                except Exception as e:
                    print(f"移动失败： {filename}: {e}")
            else:
                print(f"跳过同名文件: {filename}")
        
        self.files = []
        
    def undo(self):
        if not self.htma.log:
            print("没有可以撤回的操作记录")
            return
        print(f"开始执行撤回操作: 共{len(self.htma.log)}个文件")
        count = 0
        for action in self.htma.log:
            filename = action["Operand"]
            original_full_path = action["dst_path"]
            target_file_path = action["src_path"]

            if os.path.exists(original_full_path):
                try:
                    if not os.path.exists(target_file_path):

                        shutil.move(original_full_path, target_file_path)
                    
                        action["src_path"] = original_full_path
                        action["dst_path"] = target_file_path
                        action["time"] = self.htma.get_now()

                        print(f"已撤回: {filename}")
                        count += 1
                    else:
                        print(f"跳过同名文件: {filename}")
                except Exception as e:
                    print(f"移动失败 {filename}:{e}")
            else:
                print(f"文件失踪(可能已被手动移动) : {filename}")
        
        print(f"操作完成。共撤回 {count}个文件")