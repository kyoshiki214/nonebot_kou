from nonebot import require, get_bot, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
import httpx
from typing import Optional
import os
from pathlib import Path

current_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + "/"
# V_PATH = str(Path(f"{current_path}../atri/resources/voice").absolute()) + "/"
V_PATH = "app/src/plugins/atri/resources/voice/"
scheduler = require("nonebot_plugin_apscheduler").scheduler

tmp = on_command('test')

@tmp.handle()
async def test():
    bot = get_bot()
    img_url = (await get_url())
    if img_url:
        # await bot.send_group_msg(group_id='236351615', message='早安铸币们')
        # await bot.send_group_msg(group_id='236351615', message=MessageSegment.record(f"file:///{V_PATH}ohayo.mp3"))
        await bot.send_group_msg(group_id='236351615', message=MessageSegment.image(img_url["imageUrl"]))

async def get_url() -> Optional[str]:
    """
    :return: 早报图片链接
    """
    url = "http://dwz.2xb.cn/zaob"
    async with httpx.AsyncClient() as client:
        r = (await client.get(url=url)).json()
        return r


scheduler.add_job(test, "cron", hour =7, minute=00, id="xxx")
