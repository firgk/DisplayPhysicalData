from datetime import datetime
from threading import Timer
import os
import time

'''
每个 10 秒打印当前时间。
'''

def timedTask():
    '''
    第一个参数: 延迟多长时间执行任务(单位: 秒)
    第二个参数: 要执行的任务, 即函数
    第三个参数: 调用函数的参数(tuple)
    '''
    Timer(10, task, ()).start()

# 定时任务
def task():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("定时任务执行")
    os.system("python makeStudent.py")






if __name__ == '__main__':

    timedTask()

    while True:
        # 获取当前时间
        current_time = datetime.now()
        # 如果当前时间是每天的2点（凌晨2点），执行定时任务
        if current_time.hour == 2 and current_time.minute == 0 and current_time.second == 0:
            task()
        # 每隔5秒打印一次当前时间戳
        print(time.time())
        time.sleep(5)



