import queue
import threading
import time

# 创建传送带（篮子）
sushi_belt = queue.Queue()


# 厨师（生产者）
def chef():
    for i in range(5):
        food = f"寿司-{i}"
        print(f"厨师做好了: {food}")

        sushi_belt.put(food)

        time.sleep(0.5)


# 食客（消费者）
def customer():
    while True:
        try:
            food = sushi_belt.get(timeout=3)
            print(f"    食客吃掉了：{food}")
            sushi_belt.task_done()
        except queue.Empty:
            print("    没吃的了，食客走了")
            break


# --- 开始营业 ---
# 创建食客线程
t_customer = threading.Thread(target=customer)
t_customer.start()

chef()

t_customer.join()
