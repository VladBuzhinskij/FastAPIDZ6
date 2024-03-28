from pydantic import BaseModel,Field
from datetime import date

class UserIn(BaseModel):
    name: str = Field(..., max_length=32)
    surname: str = Field(..., max_length=32)
    dat: date = Field(...)
    mail: str = Field(..., max_length=128,pattern=r'[\w\.-]+@[\w\.-]+(\.[\w]+)+')
    address: str = Field(..., max_length=128)


class User(BaseModel):
    id: int
    name: str = Field(..., max_length=32)
    surname: str = Field(..., max_length=32)
    dat: date = Field(...)
    mail: str = Field(..., max_length=128,pattern=r'[\w\.-]+@[\w\.-]+(\.[\w]+)+')
    address: str = Field(..., max_length=128)
