import urllib.request
import urllib.parse
import jsonpath
import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

vtb = on_command('查成分', priority=2, block=True)

@vtb.handle()
async def vtb_sender(bot: Bot, event: MessageEvent):
    keyword = str(event.get_message()).split(' ')[1]
    print(keyword)
    result = query(keyword)
    await vtb.finish(result)

def query(content):
    # 请求地址
    url = 'https://api.asoulfan.com/cfj/?name=' + urllib.parse.quote(content)
    # 请求头部
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' 
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 发送请求，获得响应
    response = urllib.request.urlopen(req)
    # 读取响应，获得文本
    text = json.loads(response.read().decode('utf-8'))
    res = jsonpath.jsonpath(text, '$..uname')
    try:
        return ','.join(res)
    except Exception:
        return ''.join(jsonpath.jsonpath(text, '$..message'))