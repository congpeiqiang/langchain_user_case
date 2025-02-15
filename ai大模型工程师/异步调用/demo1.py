# -*- coding: utf-8 -*-
# @Time    : 2025/2/13 下午2:38
# @Author  : CongPeiQiang
# @File    : demo1.py
# @Software: PyCharm
import time

import asyncio


# # 1
# async def func():
#     print(111)
#
#
# result = func()
# asyncio.run(result)  # python3.7及以后才能这么用
#
#
# # 2
# async def func():
#     print(111)
#     await asyncio.sleep(2)
#     print(222)
#
#
# asyncio.run(func())


# 3
# async def func():
#     print(333)
#     response = await other()
#     print(response)
#
#     response1 = await other()
#     print(response1)
#
#     print(444)
#
# async def other():
#     print(555)
#     # await asyncio.sleep(2)
#     print(666)
#     return "other"
# asyncio.run(func())

# 4
# async def func():
#     print(111)
#     await asyncio.sleep(2)
#     print(222)
#     return "func"
#
#
# async def func1():
#     print(333)
#     await asyncio.sleep(2)
#     print(444)
#     return "func1"
#
#
# async def f():
#     print("start")
#     task1 = asyncio.create_task(func()) # 创建Task对象
#     task2 = asyncio.create_task(func1()) # 创建Task对象
#     res1 = await task1
#     res2 = await task2
#     print(res1)
#     print(res2)
#
# asyncio.run(f())

# 5
async def func():
    print(111)
    await asyncio.sleep(2)
    print(222)
    return "func"


async def func1():
    print(333)
    await asyncio.sleep(2)
    print(444)
    return "func1"


async def f():
    a = await asyncio.gather(func(), func1())
    print(type(a), a)

asyncio.run(f())


