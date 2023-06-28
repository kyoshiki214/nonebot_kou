from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Bot
import os
import time
from pathlib import Path

current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + "/"
py = on_command('python', aliases={'py'}, priority=2, block=True)

@py.handle()
async def python(bot:Bot, event:MessageEvent):
	sid = event.get_session_id().split('_')
	uid = sid[2]
	gid = sid[1]
	if str(uid) not in ['1207968383']:
		await bot.send(message='权限不足，请联系bot管理员(误触发请无视)', at_sender=False)
		return
	content = f'# coding: utf-8\n\'\'\'\n群号:{gid}\nqq号:{uid}\n\'\'\'\n' + event.get_plaintext().split(":")[1]
	print(current_path)
	current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) 
	path = f'{current_path}../../../data/log/py/{current_time}.py'
	f = open(path, 'w', encoding='utf-8')
	f.write(content)
	f.close()
	fl = os.popen(f'python {path}')
	msg = fl.read()
	await py.finish(message=''.join(msg), at_sender=False)