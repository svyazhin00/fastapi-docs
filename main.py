from datetime import datetime
from enum import Enum
from typing import List

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from fastapi.exceptions import ValidationException
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI(title='Test API')


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )

fake_trades = [
    {'id': 1, "user_id": 1, "coin": "BTC", "price": 123},
    {'id': 2, "user_id": 2, "coin": "ETH", "price": 4321}
]

users = [
    {'id': 1, "role": 1, "name": ["dsadfdsfsdf"]},
    {'id': 2, "role": 3, "name": "Asdasdasdad", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "master"}
    ]}
]

class Trade(BaseModel):
    id: int
    user_id: int
    coin: str = Field(max_length=5)
    price: float = Field(ge=0)


class DegreeType(Enum):
    master = "master"
    newbie = "newbie"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType

class User(BaseModel):
    id: int
    role: int
    name: str
    degree: List[Degree] | None = []

@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [i for i in users if i.get('id') == user_id]
