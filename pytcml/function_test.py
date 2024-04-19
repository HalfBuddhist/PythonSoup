from pyTCML import *    # 导入模块
import os

tcmlInitWithFlags(0)  # 调用其它接口前，先调用tcmlInit()

# 先调用 tcmlDeviceGetCount()获取设备数，再调用 tcmlDeviceGetGpuBusyPercent()和 tcmlDeviceGetMemBusyPercent()获取每个设备算力和内存使用率
device_count = tcmlDeviceGetCount()
for i in range(device_count):
    sn = tcmlDeviceGetSerialNum(i)
    print("sn: %s" % sn)
    bus = tcmlDeviceGetPciBus(i)
    print("bus: %s" % bus)
    listProcess = tcmlDeviceGetProcessInfo(i)   # 接口返回一个列表，列表内以字典的形式存放指定设备上的所有进程信息
    pid = os.getpid()
    print("list all processes:")
    for dic in listProcess:    
        print(dic.items())  # 打印列表内的所有字典；字典中包含三个key：'pid', 'name', 'usemem'；即进程号，进程名，进程使用内存的具体大小
        if dic.get('pid') == pid:   # 获取测例自身进程
            print("show current process:\n", dic.items())
 
tcmlShutdown()  # 调用其它接口结束后，调用tcmlShutDown()
