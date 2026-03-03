from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

users = {
  "users": [
    {
      "id": 1,
      "username": "emilys",
      "email": "emilys@example.com",
      "first_name": "Emily",
      "last_name": "Smith",
      "age": 25,
      "active": True
    },
    {
      "id": 2,
      "username": "michaelj",
      "email": "michaelj@example.com",
      "first_name": "Michael",
      "last_name": "Johnson",
      "age": 30,
      "active": True
    },
    {
      "id": 3,
      "username": "sarah_c",
      "email": "sarah_c@example.com",
      "first_name": "Sarah",
      "last_name": "Connor",
      "age": 40,
      "active": False
    }
  ]
}


@app.get('/')
def home():
    return {"message": "Hellow from Fast API"}

@app.get('/user/details')
def user_details():

    return users

@app.get('/user/details/{user_id}')
def user_details_id(user_id : int):
    for user in users["users"]:
        if user_id == user["id"]:
            return user
    
    return {"message": f"{user_id} doesn't exist"}
    
@app.delete('/user/delete/{user_id}')
def delete_user(user_id : int):
    for user in users["users"]:
        if user_id == user["id"]:
            users["users"].remove(user)
            return {"message": "user has deleted"}
           
    return {"message": f"{user_id} doesn't exist"}
            
        


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)