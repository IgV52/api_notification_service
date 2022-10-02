from beanie import Document, Indexed
from datetime import datetime
from pydantic import BaseModel

class MsgOut(BaseModel):
    number: Indexed(int, unique=True)
    sending_status: int
    num_dispath: int
    num_client: int
    created_in: datetime | None = None

    class Config:
         schema_extra = {
            "example": {
                "created_in": "2022-09-23 19:55:44",
                "sending_status": 200,
                "num_dispath": 1,
                "num_client": 1
            }
        }

class Msg(Document, MsgOut):

    def __repr__(self) -> str:
        return f"<Msg {self.number}>"

    def __str__(self) -> str:
        return self.number

    def __hash__(self) -> int:
        return hash(self.number)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Msg):
            return self.number == other.number
        return False

    @classmethod
    async def by_number(cls, number: int) -> "Msg":
        return await cls.find_one(cls.number == number)

    class Settings:
        name = "msg"

    class Config:
        schema_extra = {
            "example": {
                "number": 1,
                "created_in": "2022-09-23 19:55:44",
                "sending_status": 200,
                "num_dispath": 1,
                "num_client": 1
            }
        }