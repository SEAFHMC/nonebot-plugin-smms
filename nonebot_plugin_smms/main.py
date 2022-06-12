from httpx import AsyncClient
from pathlib import Path
from .database import ImageTable
from .schema import ResponseData

root = Path(__file__).parent.absolute()


async def open_img_from_url(url: str):
    async with AsyncClient() as client:
        resp = await client.get(url=url)
    return resp.content


class SMMS:
    base_url = "https://sm.ms/api/v2/"

    def __init__(self, token: str) -> None:
        self.headers = {"Authorization": token}

    def UpdateDB(self, user_id: int, tag: str, parsed_json: ResponseData):
        ImageTable.create(
            user_id=user_id,
            tag=tag,
            store_name=parsed_json.data.storename,
            img_url=parsed_json.data.url,
            hash=parsed_json.data.hash,
        )

    async def upload_img(self, img: bytes, user_id: int, tag: str):
        async with AsyncClient(timeout=100) as client:
            resp = await client.post(
                url=self.base_url + "upload",
                headers=self.headers,
                files={"smfile": img},
            )
        parsed_json = ResponseData(**resp.json())
        if parsed_json.success:
            self.UpdateDB(user_id=user_id, tag=tag, parsed_json=parsed_json)
        return parsed_json
