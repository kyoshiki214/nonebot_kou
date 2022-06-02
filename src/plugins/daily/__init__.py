from typing import Optional
from nonebot import logger
from nonebot import on_command, logger, require, get_driver
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

scheduler = require("nonebot_plugin_apscheduler").scheduler 

sixty = on_command("60s", aliases={"早报", "六十"}, priority=2, block=True)


@sixty.handle()
async def mor(bot: Bot, event: MessageEvent):
    img_url = (await get_url())
    if img_url:
        print(img_url)
        await sixty.send(message=MessageSegment.image(img_url["imageUrl"]))
    else:
        logger.info('获取时出现错误')


async def get_url() -> Optional[str]:
    """
    :return: 早报图片链接
    """
    url = "http://dwz.2xb.cn/zaob"
    async with httpx.AsyncClient() as client:
        r = (await client.get(url=url)).json()
        return r

# plugin_config = get_driver().config.dict()
# for index, time in enumerate(plugin_config.morning_inform_time):
#     logger.info("id:{},time:{}".format(index, time))
#     scheduler.add_job(mor, "cron", hour=time.hour, minute=time.minute, id=str(index))