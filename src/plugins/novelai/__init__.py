from random import randint
from nonebot import Bot, on_command, get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, PrivateMessageEvent, MessageSegment
import requests
import json
import base64

ai = on_command('novelai', aliases={'ai生成', 'ai画图'}, priority=2, block=True)
help = on_command('aihelp', priority=2, block=True)

@help.handle()
async def send_help(bot: Bot, event: MessageEvent):
    msg = "写着玩的ai画图插件\n使用示例:\n.ai画图:white hair,red eyes\n.novelai:blue eyes white dragon\n使用须知:该项目为基于 https://ai.nya.la/ 的懒人摸鱼插件，由于api调用量较高，可能(经常)出现超时，请稍后再试\n如需更高的自定义度(如生成NSFW图片)，请自行访问上述网站或考虑自行搭建环境"
    await ai.send(message=msg)
@ai.handle()
async def aidrawer(bot : Bot, event : MessageEvent):
    tags = event.get_plaintext().split(':')[1]
    url = "https://api.nya.la/ai/generate-image"
    seed = randint(1, 2000000000)
    headers = {
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ing0djVwQ3dLZmR3WjdvTVNTTTd0NiIsIm5jIjoibnd5Rm9JR1ZLeldZT1RDd3BDTEVxIiwiaWF0IjoxNjY1Mjk5ODA0LCJleHAiOjE2Njc4OTE4MDR9.L419_1_jSM_aTzByGTHe0QByZIw3inwuIFhoaZHnjiQ',
        'authority': 'api.nya.la',
        'origin': 'https://ai.nya.la',
        'referer': 'https://ai.nya.la/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "input": tags + ", masterpiece, best quality",
        "model": "safe-diffusion",
        "parameters": {
        "width": 512,
        "height": 768,
        "scale": 12,
        "sampler": "k_euler_ancestral",
        "steps": 28,
        "seed": seed,
        "n_samples": 1,
        "ucPreset": 0,
        "uc": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry"
        } 
    })
    await ai.send(message="ai绘画中(发送 .aihelp 可查看帮助(也许是)")
    response = requests.request("POST", url, headers=headers, data=payload).text
    list = response.split(':')
    cnt = 0
    while response[0] == '{':
        if cnt >= 4:
            await ai.finish(message="Too many requests currently processing, please try again later")
            
        cnt += 1
        # await ai.send(message=response + "\n重试中")
        response = requests.request("POST", url, headers=headers, data=payload).text
        list = response.split(':')
    if response[0] == 'e':
        data =list[3]
        img = base64.b64decode(data)
        with open("sample.png", "wb") as f:
            f.write(img)
        await ai.finish(message=MessageSegment.image(img))
    else:
        await ai.finish(message=response)
        
