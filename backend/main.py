from fastapi import FastAPI, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
import redis.asyncio as redis



app = FastAPI()

# redis_pool = redis.ConnectionPool(host="localhost", port=6379, db=0, decode_responses=True) #vs code redis pool
redis_pool = redis.ConnectionPool(host="redis", port=6379, db=0, decode_responses=True) # docker container redis pool

async def get_redis_data():
    try:
        client =redis.Redis(connection_pool=redis_pool)
        yield client
    finally:
        await client.close()


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

@app.get("/getdetails")
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
    

@app.get('/user/details')
def user_details():

    return users

@app.get('/user/details/{user_id}')
def user_details_id(user_id : int):
    for user in users:
        if user["id"] == user_id:
            return user
        
    return {"message": f"{user_id} doesn't exist"}

@app.get('/search')
def search_user(name : str):
    for user in users:
        if user["first_name"].lower() == name.lower():
            return user
    return {"message" : f"{name.capitalize()} has not found on database"} 
    
@app.delete('/user/delete/{user_id}')
def delete_user(user_id : int):
    for user in users:
        if user_id == user["id"]:
            users["users"].remove(user)
            return {"message": "user has deleted"}
           
    return {"message": f"{user_id} doesn't exist"}
            
        


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)