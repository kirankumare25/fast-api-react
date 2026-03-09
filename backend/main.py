from fastapi import FastAPI, Depends, Response, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
from database import SessionLocal, engine, Base
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
import uvicorn
import json
import os



app = FastAPI()

# redis_pool = redis.ConnectionPool(host="localhost", port=6379, db=0, decode_responses=True) #vs code redis pool
redis_pool = redis.ConnectionPool(host="redis", port=6379, db=0, decode_responses=True) # docker container redis pool

async def get_redis_data():
    try:
        client = redis.Redis(connection_pool=redis_pool)
        yield client
    finally:
        await client.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependancy = Annotated[Session , Depends(get_db)]


class MockData(Base):
    __tablename__ = "customers"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True) 
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    job_title = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    ip_address = Column(String(50), nullable=False)


async def custom_rate(
    request: Request,
    rlocal: redis.Redis = Depends(get_redis_data),
):
    client_ip = request.client.host
    key = f"rate:{client_ip}"
    current = await rlocal.get(key)

    if current and int(current) >= 2:
        raise HTTPException(status_code=429, detail="Too many requests")

    pipe = rlocal.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, 5)
    await pipe.execute()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

users = []

WORKDIR = os.getcwd()
FILE = os.path.join(WORKDIR + "/database.json") #docker file path
# FILE = os.path.join(WORKDIR + "/backend/database.json") #vs code file path

with open(FILE, "r") as file:
    data = json.load(file)
    users = data


@app.get('/')
def home():
    return {"message": "Hellow from Fast API"}

@app.get('/getdb')
def get_db_data(db : db_dependancy):

    data = db.query(MockData).all()

    return data

@app.get("/rate", dependencies=[Depends(custom_rate)])
async def rate_limite_check():
    return {"message": "ok"}

@app.get("/getdetails",dependencies=[Depends(custom_rate)])
async def get_from_redis(id : int, cache : redis.Redis = Depends(get_redis_data)):
    cache_data = await cache.get(f"{id}")
    if cache_data:
        data = json.loads(cache_data)

        data["source"] = "from redis"
        jdata = json.dumps(data, indent=4)
        return Response(content=jdata, media_type="application/json")
    else:
        for user in users:
            if user["id"] == id:
                await cache.set(f"{id}", json.dumps(user), ex=60)
                user["source"] = "from database"
                jdata = json.dumps(user, indent=4)
                return Response(content=jdata, media_type="application/json")
    

@app.get('/user/details',dependencies=[Depends(custom_rate)])
def user_details():
    return Response(content=json.dumps(users, indent=4), media_type="application/json")

@app.get('/user/details/{user_id}',dependencies=[Depends(custom_rate)])
def user_details_id(user_id : int):
    for user in users:
        if user["id"] == user_id:
            return Response(content=json.dumps(user, indent=4), media_type="application/json")
        
    return {"message": f"{user_id} doesn't exist"}

@app.get('/search',dependencies=[Depends(custom_rate)])
def search_user(name : str):
    for user in users:
        if user["first_name"].lower() == name.lower():
             return Response(content=json.dumps(user, indent=4), media_type="application/json")
    return {"message" : f"{name.capitalize()} has not found on database"} 
    
@app.delete('/user/delete/{user_id}',dependencies=[Depends(custom_rate)])
def delete_user(user_id : int):
    for user in users:
        if user_id == user["id"]:
            users["users"].remove(user)
            return {"message": "user has deleted"}
           
    return {"message": f"{user_id} doesn't exist"}
            
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)