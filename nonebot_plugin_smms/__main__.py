from httpx import AsyncClient
from pathlib import Path
from aiofile import async_open
from config import Config
from database import ImageTable
from schema import ResponseData

root = Path(__file__).parent.absolute()


class SMMS:
    base_url = "https://sm.ms/api/v2/"

    def __init__(self, token: str) -> None:
        self.headers = {"Authorization": token}

    def UpdateDB(self, user_id:int, tag:str, parsed_json: ResponseData):
        ImageTable.create(
            user_id=user_id,
            tag=tag,
            store_name=parsed_json.data.storename,
            img_url=parsed_json.data.url,
            delete_url=parsed_json.data.delete,
        )

    async def upload_img(self, img: str, user_id: int, tag:str):
        async with async_open(img, "rb") as f:
            content = await f.read()
        async with AsyncClient(timeout=100) as client:
            resp = await client.post(
                url=self.base_url + "upload",
                headers=self.headers,
                files={"smfile": content},
            )
        parsed_json = ResponseData(**resp.json())
        if parsed_json.success:
            self.UpdateDB(user_id=user_id, tag=tag, parsed_json=parsed_json)
            return f"Uplaod Success, img_url:{parsed_json.data.url}"
        return f"Uplaod failed {parsed_json.message}"


import asyncio

smms = SMMS(token=Config.token)
img = root / "usao.png"
res = asyncio.run(smms.upload_img(img=img, user_id=1366160279, tag="USAO"))
print(res)
