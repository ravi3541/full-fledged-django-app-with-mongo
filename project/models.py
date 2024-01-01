from bson.objectid import ObjectId
from datetime import datetime, timezone

from utilities.utils import database

project_collection = database.project
client_collection = database["client"]


class Project:
    """
    Class to handle PROJECT operations.
    """

    def create_project(self, project_data):
        project_data["created_at"] = datetime.now(timezone.utc)
        project_data["updated_at"] = datetime.now(timezone.utc)
        result = project_collection.insert_one(project_data)
        return result.inserted_id

    def get_project_by_id(self, project_id):
        return project_collection.find_one({"_id": ObjectId(project_id)})

    def get_all_projects(self):
        return project_collection.find()


class Client:
    """
    Class to handle CLIENT operations.
    """
    def create_client(self, client_data):
        client_data["created_at"] = datetime.now(timezone.utc)
        client_data["updated_at"] = datetime.now(timezone.utc)
        result = client_collection.insert_one(client_data)
        return result.inserted_id

    def get_client_by_id(self, client_id):
        return client_collection.find_one({"_id": ObjectId(client_id)})

    def get_all_client(self):
        return client_collection.find()
