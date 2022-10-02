from beanie import Document, Indexed
from datetime import datetime
from pydantic import BaseModel
from typing import TypedDict

class Filter(TypedDict):
    tag: str
    code_mobile: int

class DispathUpdate(BaseModel):
    start_sending: datetime
    text: str
    filter: Filter
    end_sending: datetime

    class Config:
        schema_extra = {
            "example": {
                "start_sending": "2022-09-23 19:55:44.583089",
                "text": "Первая рассылка",
                "filter": {"tag": "gold", "code_mobile": 200},
                "end_sending": "2022-09-23 19:55:44.583089"
            }
        }

class DispathOut(DispathUpdate):
    number: Indexed(int, unique=True)

class Dispath(Document, DispathOut):

    def __repr__(self) -> str:
        return f"<Dispath {self.number}>"

    def __str__(self) -> str:
        return self.number

    def __hash__(self) -> int:
        return hash(self.number)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Dispath):
            return self.number == other.number
        return False

    @classmethod
    async def by_number(cls, number: int) -> "Dispath":
        return await cls.find_one(cls.number == number)

    class Settings:
        name = "dispath"

    class Config:
        schema_extra = {
            "example": {
                "number": 1,
                "start_sending": "2022-09-23 19:55:44.583089",
                "text": "Первая рассылка",
                "filter": {"tag": "gold", "code_mobile": 200},
                "end_sending": "2022-09-23 19:55:44.583089"
            }
        }
