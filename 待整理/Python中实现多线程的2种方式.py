import threading
import time
# 实现多线程的2种方式

# 1. 利用threading的Thread类来实现


def work1(*args, **kwargs):
    # do something
    print("work1 is start")
    time.sleep(2)
    print("work1 is end")


def work2(*args, **kwargs):
    # do something
    print("work2 is start")
    time.sleep(4)
    print("work2 is end")


work1_thread = threading.Thread(target=work1, args=("",))
work2_thread = threading.Thread(target=work2, args=("",))
# 默认情况下主线程结束 子线程不会结束 守护进程是False
# work1_thread.setDaemon(False)
# work2_thread.setDaemon(False)

work1_thread.start()
work2_thread.start()
# 主线程必须等所有子线程全部结束后才结束线程
work1_thread.join()
work2_thread.join()

print("主线程end")


# 2. 利用继承threading的Thread类 并重run方法的方式来实现

class Work1(threading.Thread):

    def __init__(self, name):
        super(Work1, self).__init__(name=name)

    def run(self):
        print("work1 is start")
        time.sleep(2)
        print("work1 is end")


class Work2(threading.Thread):
    def __init__(self, name):
        super(Work2, self).__init__(name=name)

    def run(self):
        print("work2 is start")
        time.sleep(4)
        print("work2 is end")


w1 = Work1("work1")
w2 = Work2("work2")

w1.start()
w2.start()

w1.join()
w2.join()
print("主线程结束")
