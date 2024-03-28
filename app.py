from fastapi import FastAPI
import databases
import sqlalchemy
from model import User, UserIn
from typing import List
DATABASE_URL="sqlite:///my_database.db"

database=databases.Database(DATABASE_URL)
metadata=sqlalchemy.MetaData()

users=sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("name",sqlalchemy.String(32)),
    sqlalchemy.Column("surname",sqlalchemy.String(32)),
    sqlalchemy.Column("dat",sqlalchemy.Date()),
    sqlalchemy.Column("mail",sqlalchemy.String(128)),
    sqlalchemy.Column("address",sqlalchemy.String(128)),
)


engine=sqlalchemy.create_engine(
    DATABASE_URL,connect_args={"check_same_thread":False})
metadata.create_all(engine)



app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.post("/users/",response_model=User)
async def create_user(user:UserIn):
    query=users.insert().values(name=user.name, surname=user.surname,dat=user.dat,mail=user.mail,address=user.address)
    query=users.insert().values(**user.dict())
    last_record_id=await database.execute(query)

    return {**user.dict(),"id":last_record_id}

@app.get("/users/",response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}",response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id ==user_id)
    return await database.fetch_one(query)

@app.put("/users/{user_id}",response_model=User)
async def update_user(user_id: int,new_user: UserIn):
    query = users.update().where(users.c.id ==user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(),"id":user_id}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id ==user_id)
    await database.execute(query)
    return {"message":"user deleted"}