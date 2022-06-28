import json
import random
import time
import sqlite3
import numpy as np
from nonebot import Bot, on_command, get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from scipy.special import erfinv

db_path = get_driver().config.jrrp_db[0]
con = sqlite3.connect(db_path)
cur = con.cursor()


jrrp = on_command('jrrp', aliases={'.jrrp', '。jrrp'}, priority=2, block=True)


@jrrp.handle()
async def _(bot: Bot, event: MessageEvent):
    init_db(cur)
    uid = int(event.get_user_id())
    gid = event.get_session_id()
    gid = int(gid[6:15])
    info = await bot.get_group_member_info(group_id=gid, user_id=uid)
    current_day = time.strftime("%Y-%m-%d", time.localtime())
    name = info.get('card', '')
    if name == '':
        name = info.get('nickname', '')
    rand = get_jrrp(cur, uid, current_day)
    if rand is None:
        rand = avg_rand()
        cur.execute(
            f"insert into jrrp values(null, {uid}, \'{current_day}\', {rand})")
        con.commit()
        await jrrp.finish(message=f'{name}今天的人品值是: {rand}')
    else:
        await jrrp.finish(message=f'{name}今天的人品值是: {rand[0]}（刷不了初始，爬)')


def avg_rand():
    random.seed(time.time())
    rand1 = random.randint(1, 100)
    rand2 = random.randint(1, 100)
    return round(0.75 * rand1 + 0.25 * rand2)


def init_db(cur: sqlite3.Cursor):
    cur.execute(
        'CREATE TABLE IF NOT EXISTS jrrp(id integer PRIMARY KEY, uid integer, date text, jrrp integer)')


def get_jrrp(cur: sqlite3.Cursor, uid: str, date: str):
    cur.execute(f'select jrrp from jrrp where uid=={uid} and date==\'{date}\'')
    row = cur.fetchone()
    return row
