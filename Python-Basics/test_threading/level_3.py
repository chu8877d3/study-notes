import threading
import time


def bacground_monitor():
    count = 0
    while True:
        time.sleep(1)
        count += 1
        print(f"\n[后台] 摄像头正在录像... {count}秒")


t_monitor = threading.Thread(target=bacground_monitor)

 
t_monitor.daemon = True

t_monitor.start()

print("主程序，我是老板，我在处理文件...")
for i in range(3):
    time.sleep(1.5)
    print(f"主程序，处理文件 {i} 完成")

print("主程序：我下班了！(Main Loop End)")
