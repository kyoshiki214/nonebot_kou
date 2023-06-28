from socket import MSG_CONFIRM
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot import on_command
from jmcomic import *
from jmcomic.jm_option import *

jm = on_command("jm", aliases={"JM"}, priority=2, block=True)
search = on_command("search", priority=2, block=True)
jm_option = create_option('/root/tmp/option.yml')


@jm.handle()
async def jm_sender(bot: Bot, event: MessageEvent):
    plain_msg = str(event.get_message())
    uid = plain_msg.split(' ')[1]
    try:
        await jm.send(message='bot加载中')
        msg = search_jm_album(uid)
        print(msg)
        # await pixiv.send(message=msg)
        gid = event.get_session_id()
        gid = int(gid[6:15])
        print(gid)
        # for i in range(len(msg)):
        await bot.send_group_forward_msg(group_id=gid, messages=msg)
    except Exception as e:
        print(e)
        await jm.send(message=str(e))
        await jm.send(message='发送失败')


@search.handle()
async def jm_search(bot: Bot, event: MessageEvent):
    plain_msg = str(event.get_message())
    keyword = plain_msg.split(' ')[1]
    try:
        await jm.send(message='bot搜索中')
        msg = search_jm_album_by_keyword(keyword)
        print(msg)
        gid = event.get_session_id()
        gid = int(gid[6:15])
        print(gid)
        await bot.send_group_forward_msg(group_id=gid, messages=msg)
    except Exception as e:
        print(e)
        await jm.send(message=str(e))
        await jm.send(message='发送失败')


def search_jm_album_by_keyword(keyword):
    uin = 425831926
    name = '雪豹'
    client = jm_option.build_jm_client()
    search_page: JmSearchPage = client.search_album(
        search_query=keyword, page=1)
    forward_msg = []
    for album_id, title in search_page:
        msg = {
            "type": "node",
            "data": {
                    "name": name,
                    "uin": uin,
                    "content": f'[{album_id}]: {title}'
            }
        }
        forward_msg.append(msg)
    return forward_msg


def search_jm_album(id):
    uin = 425831926
    name = '雪豹'

    client = jm_option.build_jm_client()
    search_page = client.search_album(search_query=id)
    album: JmAlbumDetail = search_page.single_album

    title = album.title
    author = album.author
    tags = album.keywords
    page_count = album.page_count
    msg = f'title: {title}\nauthor: {author}, page:{page_count}\ntags: {tags}\n'
    print(msg)
    forward_msg = [
        {
            "type": "node",
            "data": {
                    "name": name,
                    "uin": uin,
                    "content": msg
            }
        }
    ]

    def download(p):
        p: JmPhotoDetail = client.get_photo_detail(p.photo_id, False)
        client.ensure_photo_can_use(p)
        decode_image = jm_option.download_image_decode
        img_save_path = "/root/jm/download/tmp.jpg"
        client.download_by_image_detail(p[0], img_save_path, decode_image)
        msg = {
            "type": "node",
            "data": {
                "name": name,
                "uin": uin,
                "content": MessageSegment.image("file:///root/jm/download/tmp.jpg")
            }
        }
        forward_msg.append(msg)

    multi_thread_launcher(
        iter_objs=album,
        apply_each_obj_func=download
    )
    return forward_msg
