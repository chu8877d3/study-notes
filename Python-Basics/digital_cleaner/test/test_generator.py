import os
import random
import string
from pathlib import Path

# === 配置区域 ===
TARGET_DIR = r"D:\Test_None"  # 生成路径 (会自动创建)
FILE_COUNT = 1000  # 生成文件数量
FOLDER_COUNT = 100  # 生成干扰文件夹数量

# === 测试用后缀库 ===
EXTENSIONS = {
    "Image": ["jpg", "png", "gif", "webp", "bmp"],
    "Document": ["txt", "md", "docx", "pdf", "xlsx"],
    "Video": ["mp4", "mkv", "ts", "avi"],
    "Code": ["py", "c", "cpp", "js", "ts", "html"],
    "Archive": ["zip", "rar", "7z", "jar"],
    "Executable": ["exe", "bat", "dll"],
    "Data": ["json", "yaml", "xml", "dat", "bin"],
    "Minecraft": ["mca", "nbt", "litematic"],
}

# === 伪造魔数表 ===
MAGIC_HEADERS = {
    "png": b"\x89PNG\r\n\x1a\n",
    "jpg": b"\xff\xd8\xff",
    "gif": b"GIF89a",
    "zip": b"PK\x03\x04",
    "jar": b"PK\x03\x04",
    "exe": b"MZ",
    "ts": b"\x47" + b"\x00" * 187,
    "nbt": b"\x1f\x8b",
    "litematic": b"\x1f\x8b",
}


def get_random_name(length=8):
    letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for i in range(length))


def create_random_content(ext):
    if ext in MAGIC_HEADERS:
        header = MAGIC_HEADERS[ext]
        body = os.urandom(1024)
        return header + body

    if ext in EXTENSIONS["Code"] or ext in EXTENSIONS["Document"]:
        if ext == "ts":
            return b"import { value } from 'module';\n// This is code."
        return f"This is a random test file for {ext}.".encode("utf-8")

    return os.urandom(512)


def main():
    base_path = Path(TARGET_DIR)

    if not base_path.exists():
        base_path.mkdir(parents=True)
        print(f" 已创建目录: {base_path}")

    print(f" 开始在 {base_path} 生成测试数据...")

    for _ in range(FOLDER_COUNT):
        folder_name = "Folder_" + get_random_name(5)
        (base_path / folder_name).mkdir(exist_ok=True)

    all_exts = [ext for cat in EXTENSIONS.values() for ext in cat]

    for _ in range(FILE_COUNT):
        ext = random.choice(all_exts)
        name = get_random_name()

        if ext == "ts":
            if random.random() > 0.5:
                content = create_random_content("ts")
                final_name = f"{name}_video.ts"
            else:
                content = b"export const x = 10;"
                final_name = f"{name}_code.ts"
        else:
            final_name = f"{name}.{ext}"
            content = create_random_content(ext)

        # 写入文件
        file_path = base_path / final_name
        with open(file_path, "wb") as f:
            f.write(content)

    print(f"生成了 {FILE_COUNT} 个文件。")


if __name__ == "__main__":
    main()
