from socket import MSG_CONFIRM
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot import on_command
from pixivpy3 import *

pixiv = on_command("pixiv", aliases={"pix"}, priority=2, block=True)


@pixiv.handle()
async def pix_sender(bot: Bot, event: MessageEvent):
    plain_msg = str(event.get_message())
    uid = plain_msg.split(' ')[1]
    # if not uid[5].isdigit():
    #     uid = uid[6:]
    # else:
    #     uid = uid[4:]
    print(uid)
    try:
        await pixiv.send(message='bot加载中')
        msg, sub_msg, is_r = get_pixiv(uid)
        print(msg)
        # await pixiv.send(message=msg)
        gid = event.get_session_id()
        gid = int(gid[6:15])
        print(gid)
        # for i in range(len(msg)):
        if is_r == True:
            await pixiv.send(message="nsfw警告")
        await bot.send_group_forward_msg(group_id=gid, messages=msg)
    except AttributeError as a:
        await pixiv.finish(message="未找到图片，请检查id是否正确")
    except TimeoutError as t:
        await pixiv.finish(message="加载超时，也许过一会儿就发出来了（")
    except ActionFailed as act:
        await pixiv.send(message="图片被河蟹，将以兼容模式发送（")    
        await bot.send_group_forward_msg(group_id=gid, messages=sub_msg)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        await pixiv.finish(message='未知错误，请检查日志')


def get_pixiv(str):
    uin = 425831926
    name = '雪豹'
    api = AppPixivAPI()
    api.auth(refresh_token='MjD2JK6YTYgYri88ZwTUXL6dG_eKVpKNHFu732Ryol8')
    json_result = api.illust_detail(str)
    illust = json_result.illust
    url = illust.image_urls['large'].replace('i.pximg.net', 'i.pixiv.re')
    url = url.replace('_webp', '')
    # url = f'[CQ:image,url={url}]'
    print(url)
    title = illust.title
    id = illust.user.id
    author = illust.user.name
    tag = illust.tags
    page_count = illust.page_count
    is_ai = illust.illust_ai_type
    length = len(tag)
    tags = ''
    is_r = False
    for i in range(length):
        t = tag[i].name
        if (t == 'r18' or t == 'R18' or t == 'r-18' or t == 'R-18'):
            is_r = True
        tags += t + ','
    tags = tags[:-1]
    msg = f'title: {title}\nauthor: {author}, uid:{id}\ntags: {tags}\n'
    msg = [
        {
            "type": "node",
            "data": {
                    "name": name,
                    "uin": uin,
                    "content": msg
            }
        }
    ]
    sub_msg = f'title: {title}\nauthor: {author}, uid:{id}\n'
    sub_msg = [
        {
            "type": "node",
            "data": {
                    "name": name,
                    "uin": uin,
                    "content": sub_msg
            }
        }
    ]
    if page_count > 1:
        for i in range(page_count):
            img = url.replace('_p0_', f'_p{i}_')
            sub_img = {
                "type": "node",
                "data": {
                    "name": name,
                    "uin": uin,
                    "content": img
                }
            }
            img = {
                "type": "node",
                "data": {
                    "name": name,
                    "uin": uin,
                    "content": MessageSegment.image(img)
                }
            }
            
            msg.append(img)
            sub_msg.append(sub_img)
    else:
        img = {
            "type": "node",
            "data": {
                "name": name,
                "uin": uin,
                "content": MessageSegment.image(url)
            }
        }
        sub_img = {
            "type": "node",
            "data": {
                "name": name,
                "uin": uin,
                "content": url
            }
        }
        msg.append(img)
        sub_msg.append(sub_img)
    if is_ai == 2:
        dz = {
            "type": "node",
            "data": {
                "name": name,
                "uin": uin,
                "content": "一眼丁真，鉴定为ai"
            }
        }
        msg.append(dz)
        sub_msg.append(dz)
    return msg, sub_msg, is_r
