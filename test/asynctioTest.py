# -*- coding: utf-8 -*-
import asyncio
import time

from WebSocket.app.controller.performance_testing.mobile_terminal.apm import CPU, Flow, FPS, Battery
from WebSocket.app.controller.performance_testing.mobile_terminal.common import Devices

d = Devices()
device = '3c2691fe'
pkgname = "com.qiyi.video"
deviceId = d.getIdbyDevice(device)
pid = d.getPid(deviceId=deviceId, pkgName=pkgname)
cpu = CPU(pkgName=pkgname, deviceId=deviceId)
fps_monitor = FPS(pkgName=pkgname, deviceId=deviceId)
battery_monitor = Battery(deviceId=deviceId)
flow = Flow(pkgName=pkgname, deviceId=deviceId)

async def say_after():
    res = await cpu.getSingCpuRate()
    return res


async def say_after1():
    res = await fps_monitor.getFPS()
    return res


async def say_after2():
    res = await battery_monitor.getBattery()
    return res

async def say_after3():
    send = await flow.getUpFlow()
    recv = await flow.getDownFlow()
    return send, recv

async def main():
    task1 = asyncio.create_task(
        say_after()
    )
    task2 = asyncio.create_task(
        say_after1()
    )
    task3 = asyncio.create_task(
        say_after2()
    )
    task4 = asyncio.create_task(
        say_after3()
    )
    print(f"starter at {time.strftime('%X')}")
    ret = await asyncio.gather(task1, task2)
    print(ret)
    print(f"starter at {time.strftime('%X')}")


asyncio.run(main())
