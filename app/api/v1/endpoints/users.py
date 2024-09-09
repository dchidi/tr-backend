from fastapi import APIRouter, Depends
from bson import ObjectId
from app.schemas.user import User, UserCreate
from app.db.mongodb import get_mongo_db

router = APIRouter()


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, mongo_db=Depends(get_mongo_db)):
    user_dict = user.dict()
    result = await mongo_db["users"].insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str, mongo_db=Depends(get_mongo_db)):
    user = await mongo_db["users"].find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])  # Convert ObjectId to string
        return user
    return {"error": "User not found"}
