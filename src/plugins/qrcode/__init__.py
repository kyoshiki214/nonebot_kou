import re
from io import BytesIO

import pyzbar.pyzbar as pyzbar
import requests
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from PIL import Image

qrcode = on_command('qr', aliases={'qrcode'}, priority=2, block=True)

@qrcode.handle()
async def qr(bot: Bot, event: MessageEvent):
    ret = re.match(r"qr( ?)\[CQ:image,file=(.*),url=(.*)\]", str(event.get_message()))
    print(str(event.get_message()))
    print(ret)
    image = Image.open(BytesIO(get_pic(ret.group(3))))
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        await qrcode.send(message=barcodeData)
        print(barcodeData)

def get_pic(address):
    return requests.get(address,timeout=20).content
