import threading
import time


def sing():
    for i in range(5):
        print(f"我在唱歌...{i}")
        time.sleep(1)


def bath():
    for i in range(5):
        print(f"我在洗澡...{i}")
        time.sleep(1)


t_sing = threading.Thread(target=sing)

t_sing.start()

bath()

t_sing.join()

print("搞定 总共耗时约 5 秒")
