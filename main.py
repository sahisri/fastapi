# -*- coding: utf-8 -*-

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional
from pydantic import BaseModel, Field
import MySQLdb

# Database configuration
db_config = {
    "host": "mysql",
    "user": "fastapi",
    "passwd": "fastapi",
    "db": "testdb",
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)

# aplication instance
app = FastAPI()
# request body pydantic model

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://medium.com/@Danie_l/getting-started-with-fast-api-and-docker-8ff2fd784399
# https://www.youtube.com/watch?v=aHv7-6WIxNM
# https://medium.com/@nutanbhogendrasharma/step-by-step-consume-rest-api-in-react-application-48388f6c4d9c
# https://medium.com/@harshvardhan.singh/mysql-on-docker-9c7adec88b13
# https://medium.com/@miladev95/fastapi-crud-with-mysql-b06d33601a38
# https://dassum.medium.com/building-rest-apis-using-fastapi-sqlalchemy-uvicorn-8a163ccf3aa1


class User(BaseModel):
    name: str
    username: str
    email: str
    phone: str
    website: Optional[str] = None
    vaccinated: bool = True
    age: int = Field(gt=0, lt=100)


# get endpoint to get all posts
@app.get("/users")
def get_users():
    cursor = conn.cursor()
    users = []
    query = "SELECT * FROM users"
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    if items is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There are no users")
    for item in items:
        user = {
            "id": item[0],
            "name": item[1],
            "username": item[2],
            "email": item[3],
            "phone": item[4],
            "website": item[5],
        }
        users.append(user)
    return users


# post endpoint to add a post
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_users(user: User):
    cursor = conn.cursor()
    query = (
        "INSERT INTO users (name, username, email, phone, website, vaccinated, age) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(query, (user.name, user.username, user.email, user.phone, user.website, user.vaccinated, user.age))
    conn.commit()
    # user.id = cursor.lastrowid
    cursor.close()
    return user


@app.get("/users/{user_id}")
def get_user(user_id: int):
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id=%s"
    cursor.execute(query, (user_id,))
    item = cursor.fetchone()
    cursor.close()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {user_id} was not found")
    user = {"id": item[0], "name": item[1], "username": item[2], "email": item[3], "phone": item[4], "website": item[5]}
    return user
