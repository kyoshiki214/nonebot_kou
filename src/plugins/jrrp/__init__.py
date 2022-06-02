import json
import random
import time

import numpy as np
from nonebot import Bot, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from scipy.special import erfinv

jrrp = on_command('jrrp', aliases={'.jrrp', '。jrrp'}, priority=2, block=True)


@jrrp.handle()
async def _(bot: Bot, event: MessageEvent):
    uid = int(event.get_user_id())
    gid = event.get_session_id()
    gid = int(gid[6:15])
    info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    current_day = time.strftime("%Y-%m-%d", time.localtime())
    path = f'src/log/jrrp/{current_day}.json'
    name = info.get('card', '')
    if name == '':
        name = info.get('nickname', '')
    try:
        f = open(path, 'r')
    except FileNotFoundError:
        with open(path, 'w') as f:
            f.write('{}')
    with open(path, 'r') as f:
        content = f.read()
        dic = json.loads(content)  
        try:
            rand = dic[str(uid)]
            await jrrp.finish(message=f'{name}今天的人品值是: {rand}（刷不了初始，爬)')
        except KeyError:
            rand = avg_rand()
            dic[str(uid)] = rand
        content = json.dumps(dic)
    with open(path, 'w') as f:
        f.write(content)
    
    await jrrp.send(message=f'{name}今天的人品值是: {rand}')

def avg_rand():
    random.seed(time.time())
    rand1 = random.randint(1,100)
    rand2 = random.randint(1,100)
    return round(0.75 * rand1 + 0.25 * rand2)



