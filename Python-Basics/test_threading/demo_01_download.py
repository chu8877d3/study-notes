import threading
import time

def download_task(filename, seconds):
    """
    download_task 的 Docstring
    
    :param filename: 文件名字
    :param seconds: 下载需要多少秒
    """
    print(f"开始下载: {filename}(预计耗时 {seconds}s)")


    time.sleep(seconds)
    print(f"下载完成:{filename}")

if __name__ == "main":
    print("--- 主线程：开始安排任务 ---")
    start_time = time.time

    files = [("python教程.mp4",  2),("电影.mkv", 3),("图片.jpg", 1)]

    threading_list = []

    for name, sec in files:
        t = threading.Thread(target=download_task, args=(name, sec))


        t.start()

        