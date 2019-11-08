import threading

value = 0
lock = threading.Lock()


def add_value():
    global value
    #  对操作进行加锁
    lock.acquire()
    for i in range(1000000):
        value += 1
    # 执行完成后释放掉锁
    lock.release()
    print(value)


for i in range(2):
    t = threading.Thread(target=add_value)
    t.start()



import threading

value = 0
lock = threading.Lock()
def add_value():
    global value
    #  对操作进行加锁
    global lock
    for i in range(1000000):
        lock.acquire()
        value += 1
    # 执行完成后释放掉锁
        lock.release()
    print(value)

for i in range(2):
    t = threading.Thread(target=add_value)
    t.start()
    t.join()
