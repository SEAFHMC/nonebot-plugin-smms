from pydantic import BaseModel
from typing import Optional

"""
{
    "success": true,
    "code": "success",
    "message": "Upload success.",
    "data": {
        "file_id": 0,
        "width": 4677,
        "height": 3307,
        "filename": "luo.jpg",
        "storename": "D5VpWCKFElUsPcR.jpg",
        "size": 801933,
        "path": "/2019/12/16/D5VpWCKFElUsPcR.jpg",
        "hash": "Q6vLIbCGZojrMhO2e7BmgFuXRV",
        "url": "https://vip1.loli.net/2019/12/16/D5VpWCKFElUsPcR.jpg",
        "delete": "https://sm.ms/delete/Q6vLIbCGZojrMhO2e7BmgFuXRV",
        "page": "https://sm.ms/image/D5VpWCKFElUsPcR"
    },
    "RequestId": "8A84DDCA-96B3-4363-B5DF-524E95A5201A"
}
"""


class Base(BaseModel):
    class Config:
        extra = "ignore"


class Data(Base):
    file_id: int
    width: int
    height: int
    filename: str
    storename: str
    size: int
    path: str
    hash: str
    url: str
    delete: str
    page: str


class ResponseData(Base):
    success: bool
    code: str
    message: str
    data: Optional[Data]
    images: Optional[str]
    RequestId: str
