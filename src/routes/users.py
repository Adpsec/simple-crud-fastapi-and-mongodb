from pickle import PUT
from fastapi import APIRouter, Response, status
from config.db import conn
from models.user_model import User
from schemas.user_schema import userEntity, usersEntity
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT


router = APIRouter()

# Definición de rutas

@router.get("/")
def index():
    return {"message": "Here is MongoDB"}


@router.get("/users", response_model=list[User], tags=["users"])
def find_all_users():
    return usersEntity(conn.local.user.find())


@router.post("/users", response_model=User, tags=["users"])
def create_one_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]

    id = conn.local.user.insert_one(new_user).inserted_id

    user = conn.local.user.find_one({"_id": id})

    return {"message": "User created", "User": userEntity(user)}


@router.get("/users/{id}", response_model=User, tags=["users"])
def find_user(id: str):
    return usersEntity(conn.local.users.find_one({"_id": ObjectId(id)}))


@router.put("/users/{id}", response_model=User, tags=["users"])
def update_user(id: str, user: User):
    conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    userEntity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))

    return Response(status_code=HTTP_204_NO_CONTENT)
