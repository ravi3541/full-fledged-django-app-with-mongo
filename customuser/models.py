import os
from bson.objectid import ObjectId
from pymongo import MongoClient
from django.contrib.auth.hashers import make_password


client = MongoClient(os.getenv("CONNECTION_STRING"))
database = client[os.getenv("DATABASE")]
customuser_collection = database.customuser


def create_user(user_data):
    user_data['password'] = make_password(user_data['password'])
    result = customuser_collection.insert_one(user_data)
    return result.inserted_id


def get_user_by_email(email):
    return customuser_collection.find_one({'email': email})


def get_user_by_id(user_id):
    return customuser_collection.find_one({"_id": ObjectId(user_id)})
