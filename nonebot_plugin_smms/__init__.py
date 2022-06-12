from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11.helpers import extract_image_urls
from nonebot.params import EventMessage, CommandArg
from random import choice
from .database import ImageTable
from .main import SMMS, open_img_from_url
from .config import Config

plugin_config = Config.parse_obj(get_driver().config)
upload = on_command("upload")
smms = SMMS(token=plugin_config.smms_token)


@upload.handle()
async def _(
    event: MessageEvent, message: Message = EventMessage(), arg: Message = CommandArg()
):
    tag = arg.extract_plain_text().strip()
    img_list = extract_image_urls(message=message)
    for i in img_list:
        img = await open_img_from_url(i)
        result = await smms.upload_img(img=img, user_id=event.user_id, tag="aw")
        if result.success:
            msg = f"上传成功!\n标签: {tag}\n文件名: {result.data.storename}"
            await upload.finish(message=msg)
        await upload.finish(f"上传失败!\n{result.message}")


img = on_command("img")


@img.handle()
async def _(arg: Message = CommandArg()):
    tag = arg.extract_plain_text().strip()
    result_list = ImageTable.select().where(ImageTable.tag == tag)
    try:
        img_url = choice([i.img_url for i in result_list])
        await img.finish(MessageSegment.image(img_url))
    except IndexError as e:
        await img.finish(f"没有找到标签为<{tag}>的图片\n{e}")
