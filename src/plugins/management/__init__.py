from nonebot import on_keyword, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, PrivateMessageEvent
import json

config_path = "src/plugins/management/config.json"

with open(config_path, 'r', encoding='utf-8') as f:
    content = json.load(f)
    w_keyword = content["withdraw_list"]
    b_keyword = content["ban_list"]
    print('reading config')

withdraw_event = on_keyword(keywords=w_keyword, priority=2, block=False)
ban_event = on_keyword(keywords=b_keyword, priority=2, block=False)
add_event = on_command('添加禁言词', priority=2, block=True)
list_event = on_command('禁言词列表', priority=2, block=True)
delete_event = on_command('删除禁言词', priority=1, block=True)

@withdraw_event.handle()
async def withdraw(bot : Bot, event : MessageEvent):
    await bot.delete_msg(message_id=event.message_id)
    # await withdraw_event.send(message='撤回成功')


@ban_event.handle()
async def ban(bot : Bot, event : MessageEvent):
    sid = event.get_session_id().split('_')
    duration = 60
    uid = sid[2]
    gid = sid[1]
    await bot.delete_msg(message_id=event.message_id)
    await bot.set_group_ban(group_id=gid, user_id=uid, duration=duration)

@list_event.handle()
async def list(bot : Bot, event : MessageEvent):
    await list_event.send(str(b_keyword))


@add_event.handle()
async def add(bot : Bot, event : PrivateMessageEvent):
    new_word = event.get_plaintext().removeprefix('添加禁言词 ').split(' ')
    for word in new_word:
        if word not in b_keyword:
            b_keyword.append(word)
    content["ban_list"] = b_keyword
    global ban_event
    ban_event = on_keyword(b_keyword, priority=2,block=False)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False)

@delete_event.handle()
async def rm(bot : Bot, event : PrivateMessageEvent):
    words = event.get_plaintext().removeprefix('删除禁言词 ').split(' ')
    for word in words:
        if word in b_keyword:
            b_keyword.remove(word)
    content["ban_list"] = b_keyword
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False)
