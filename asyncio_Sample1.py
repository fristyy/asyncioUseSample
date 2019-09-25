#coding:utf-8
import asyncio
import traceback
from concurrent.futures import ThreadPoolExecutor
import datetime

import requests

#TASKS = []
#for url in ['http://116.85.49.73',
	#'http://www.baidu.com',
	#'http://bsonspec.org/',
	#'https://www.element3ds.com/forum-208-1.html']:
	#TASKS.append(get_text(url))

task_done_count = 0
	
def fun(url):
	header = {'User-Agent': 
	          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
	return requests.get(url=url,headers=header)

async def get_text(url):
	try:
		print(url)
		loop = asyncio.get_event_loop()
		resp = await loop.run_in_executor(None, fun, url)
		#非异步模块异步执行的核心方法
		#executor可以是ThreadPoolExecutor/ProcessPool,如果是None则使用默认线程池可使用yield from或await挂起函数
		#可以使用concurrent.futures.ThreadPoolExecutor创建线程，使用with管理线程
		print(url,':',len(resp.content))
	except Exception as err:
		print(err)
		traceback.print_exc()
		return None
	return url,resp

def callback(future):
	global task_done_count 
	task_done_count += 1
	print('callback:',future.result())
	
async def display_date():
	loop = asyncio.get_running_loop() 
	end_time = loop.time() + 60.0
	while True:
		print(datetime.datetime.now(),'----',task_done_count)
		if (loop.time() + 1.0) >= end_time or task_done_count > 1:
			print('tasks done')
			break
		await asyncio.sleep(1)

async def task():

	task1 = asyncio.ensure_future(get_text('http://bsonspec.org/'))
	task1.add_done_callback(callback)
	task2 = asyncio.ensure_future(get_text('http://www.baidu.com/'))
	task2.add_done_callback(callback)
	task3 = display_date()
	await asyncio.gather(task1,task2,task3)

#loop = asyncio.get_event_loop()
##loop.run_until_complete(asyncio.wait(TASKS))
##loop.run_until_complete(asyncio.gather(task1,task2))
#loop.close()

asyncio.run(task())
