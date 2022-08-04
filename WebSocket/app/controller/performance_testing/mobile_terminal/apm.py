import datetime
import platform
import re
from functools import reduce
from logzero import logger

from .ADB import adb
from .common import Devices, file
from .fps import FPSMonitor, TimeUtils

d = Devices()


class CPU:

    def __init__(self, pkgName, deviceId):
        self.pkgName = pkgName
        self.deviceId = deviceId
        self.apm_time = datetime.datetime.now().strftime('%H:%M:%S.%f')

    def getprocessCpuStat(self):
        """获取某个时刻的某个进程的cpu损耗"""
        pid = d.getPid(pkgName=self.pkgName, deviceId=self.deviceId)
        cmd = f'cat /proc/{pid}/stat'
        result = adb.shell(cmd=cmd, deviceId=self.deviceId)
        r = re.compile("\\s+")
        toks = r.split(result)
        processCpu = float(int(toks[13]) + int(toks[14]))
        return processCpu

    def getTotalCpuStat(self):
        """获取某个时刻的总cpu损耗"""
        if platform.system() != 'Windows':
            cmd = f'cat /proc/stat |grep ^cpu'
        else:
            cmd = f'cat /proc/stat |findstr ^cpu'
        result = adb.shell(cmd=cmd, deviceId=self.deviceId)
        r = re.compile(r'(?<!cpu)\d+')
        toks = r.findall(result)
        idleCpu = float(toks[3])
        totalCpu = float(reduce(lambda x, y: int(x) + int(y), toks))
        return totalCpu

    def getSingCpuRate(self):
        """获取进程损耗cpu的占比%"""
        processCpuTime_1 = self.getprocessCpuStat()
        totalCpuTime_1 = self.getTotalCpuStat()
        processCpuTime_2 = self.getprocessCpuStat()
        totalCpuTime_2 = self.getTotalCpuStat()
        cpuRate = int((processCpuTime_2 - processCpuTime_1) / (totalCpuTime_2 - totalCpuTime_1) * 100)
        return cpuRate


class MEM:
    def __init__(self, pkgName, deviceId):
        self.pkgName = pkgName
        self.deviceId = deviceId
        self.apm_time = datetime.datetime.now().strftime('%H:%M:%S.%f')

    def getProcessMem(self):
        """获取进程内存Total、NativeHeap、NativeHeap;单位MB"""
        pid = d.getPid(pkgName=self.pkgName, deviceId=self.deviceId)
        cmd = f'dumpsys meminfo {pid}'
        output = adb.shell(cmd=cmd, deviceId=self.deviceId)
        m = re.search(r'TOTAL\s*(\d+)', output)
        # m1 = re.search(r'Native Heap\s*(\d+)', output)
        # m2 = re.search(r'Dalvik Heap\s*(\d+)', output)
        PSS = round(float(float(m.group(1))) / 1024, 2)
        # with open(f'{file().report_dir}/mem.log', 'a+') as f:
        #     f.write(f'{self.apm_time}={str(PSS)}' + '\n')
        # NativeHeap = round(float(float(m1.group(1))) / 1024, 2)
        # DalvikHeap = round(float(float(m2.group(1))) / 1024, 2)
        return PSS


class Battery:
    def __init__(self, deviceId):
        self.deviceId = deviceId
        self.apm_time = datetime.datetime.now().strftime('%H:%M:%S.%f')

    def getBattery(self):
        """获取手机电量"""
        # 切换手机电池为非充电状态
        cmd = 'dumpsys battery set status 1'
        adb.shell(cmd=cmd, deviceId=self.deviceId)
        # 获取手机电量
        cmd = 'dumpsys battery'
        output = adb.shell(cmd=cmd, deviceId=self.deviceId)
        battery = int(re.findall(u'level:\s?(\d+)', output)[0])
        return battery


class Flow:

    def __init__(self, pkgName, deviceId):
        self.pkgName = pkgName
        self.deviceId = deviceId
        self.apm_time = datetime.datetime.now().strftime('%H:%M:%S.%f')

    def getUpFlow(self):
        """获取上行流量，单位MB"""
        pid = d.getPid(pkgName=self.pkgName, deviceId=self.deviceId)
        if platform.system() != 'Windows':
            cmd = f'cat /proc/{pid}/net/dev |grep wlan0'
        else:
            cmd = f'cat /proc/{pid}/net/dev |findstr wlan0'
        output = adb.shell(cmd=cmd, deviceId=self.deviceId)
        m = re.search(r'wlan0:\s*(\d+)\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*(\d+)', output)
        if m:
            return round(float(float(m.group(2)) / 1024 / 1024), 2)
        else:
            logger.error("Couldn't get rx and tx data from: %s!" % output)

    def getDownFlow(self):
        """获取下行流量，单位MB"""
        pid = d.getPid(pkgName=self.pkgName, deviceId=self.deviceId)
        if platform.system() != 'Windows':
            cmd = f'cat /proc/{pid}/net/dev |grep wlan0'
        else:
            cmd = f'cat /proc/{pid}/net/dev |findstr wlan0'
        output = adb.shell(cmd=cmd, deviceId=self.deviceId)
        m = re.search(r'wlan0:\s*(\d+)\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*(\d+)', output)
        if m:
            return round(float(float(m.group(1)) / 1024 / 1024), 2)
        else:
            logger.error("Couldn't get rx and tx data from: %s!" % output)

    def getAllFlow(self):
        return dict(
            upFlow=self.getUpFlow(),
            downFlow=self.getDownFlow()
        )

class FPS:

    def __init__(self, pkgName, deviceId):
        self.pkgName = pkgName
        self.deviceId = deviceId
        self.apm_time = datetime.datetime.now().strftime('%H:%M:%S.%f')

    def getFPS(self):
        monitors = FPSMonitor(device_id=self.deviceId, package_name=self.pkgName, frequency=1,
                              start_time=TimeUtils.getCurrentTimeUnderline())
        monitors.start()
        collects_fps, collects_jank = monitors.stop()
        return collects_fps, collects_jank


if __name__ == '__main__':
    fps = FPS("com.qiyi.video", '3c2691fe')
    print(fps.getFPS())
