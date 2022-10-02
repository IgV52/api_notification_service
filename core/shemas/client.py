from beanie import Document, Indexed
from pydantic import BaseModel

class ClientUpdate(BaseModel):
    phone: int
    code_mobile: int
    tag: str
    tzone: str

    class Config:
        schema_extra = {
            "example": {
                "phone": 79300488976,
                "code_mobile": 200,
                "tag": "gold",
                "tzone": "UTC"
            }
        }

class ClientOut(ClientUpdate):
    number: Indexed(int, unique=True)

class Client(Document, ClientOut):
    def __repr__(self) -> str:
        return f"<Client {self.number}>"

    def __str__(self) -> str:
        return self.number

    def __hash__(self) -> int:
        return hash(self.number)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Client):
            return self.number == other.number
        return False

    @classmethod
    async def by_number(cls, number: int) -> "Client":
        return await cls.find_one(cls.number == number)

    class Settings:
        name = "client"

    class Config:
        schema_extra = {
            "example": {
                "number": 1,
                "phone": 79300488976,
                "code_mobile": 200,
                "tag": "gold",
                "tzone": "UTC"
            }
        }
