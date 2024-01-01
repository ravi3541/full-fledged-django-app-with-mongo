import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone

from utilities.utils import CustomException


client = MongoClient(os.getenv("CONNECTION_STRING"))
database = client[os.getenv("DATABASE")]
customuser_collection = database.customuser


def create_user(user_data):
    try:
        # customuser_collection.create_index([('first_name', 1)], unique=True)
        customuser_collection.create_index([('email', 1)], unique=True)

        user_data['password'] = make_password(user_data['password'])
        user_data["created_at"] = datetime.now(timezone.utc)
        user_data["updated_at"] = datetime.now(timezone.utc)
        result = customuser_collection.insert_one(user_data)
        return result.inserted_id
    except DuplicateKeyError as e:
        # duplicate_key = e.details.get("keyPattern", {}).keys()
        # print("key = ", duplicate_key)
        # if "email" in duplicate_key:
        #     print("Error - User with this email already exists.")
        # if "first_name" in duplicate_key:
        #     print("Error - User with this first_name already exists.")

        raise CustomException("User already exists.")


def get_user_by_email(email):
    return customuser_collection.find_one({'email': email})


def get_user_by_id(user_id):
    return customuser_collection.find_one({"_id": ObjectId(user_id)})
