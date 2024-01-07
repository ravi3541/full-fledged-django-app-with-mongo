from datetime import datetime, timezone
from rest_framework import status
from bson.objectid import (
    ObjectId,
    InvalidId
)
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response

from utilities import messages
from customuser.permissions import IsAuthenticated
from .models import (
    Client,
    Project,
    client_collection,
    project_collection
)
from utilities.utils import (
    parse_json,
    ResponseInfo,
    get_tokens_for_user
)
from .serializers import (
    ClientSerializer,
    ProjectSerializer,
)
from customuser.permissions import MongoDBAuthentication


class CreateClientAPIView(CreateAPIView):
    """
    Class to create client.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MongoDBAuthentication,)
    serializer_class = ClientSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(CreateClientAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Post method to create client.
        """
        client_serializer = self.get_serializer(data=request.data)
        if client_serializer.is_valid(raise_exception=True):
            request_data = client_serializer.data
            request_data["created_by"] = ObjectId(request.user["_id"])
            client_id = Client().create_client(request_data)

            client = Client().get_client_by_id(client_id)

            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["data"] = parse_json(client)
            self.response_format["error"] = None
            self.response_format["message"] = [messages.CREATED.format("Client")]
        return Response(self.response_format)


class GetClientAPIView(RetrieveAPIView):
    """
    Class to create client.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MongoDBAuthentication,)

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetClientAPIView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        """
        Post method to create client.
        """
        client_id = self.kwargs.get("pk")
        if client_id:
            client = Client().get_client_by_id(client_id)

            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["data"] = parse_json(client)
            self.response_format["error"] = None
            self.response_format["message"] = [messages.CREATED.format("Client")]
        return Response(self.response_format)


class GetAllClientAPIView(RetrieveAPIView):
    """
    Class to create client.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MongoDBAuthentication,)

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetAllClientAPIView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        """
        Post method to create client.
        """

        client = Client().get_all_client()

        self.response_format["status_code"] = status.HTTP_201_CREATED
        self.response_format["data"] = parse_json(client)
        self.response_format["error"] = None
        self.response_format["message"] = [messages.CREATED.format("Client")]
        return Response(self.response_format)


class UpdateClientAPIView(UpdateAPIView):
    """
    Class to create API for updating client.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MongoDBAuthentication,)
    serializer_class = ClientSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(UpdateClientAPIView, self).__init__(**kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Method to update client.
        """
        client_id = self.kwargs["pk"]

        client_serializer = self.get_serializer(data=request.data)
        if client_serializer.is_valid(raise_exception=True):

            filter_condition = {"_id": ObjectId(client_id)}
            update_fields = {
                "$set": {
                    "first_name": client_serializer.validated_data["first_name"],
                    "last_name": client_serializer.validated_data["last_name"],
                    "company_name": client_serializer.validated_data["company_name"],
                    "company_address": client_serializer.validated_data["company_address"],
                    "description": client_serializer.validated_data["description"],
                    "updated_at": datetime.now(timezone.utc),

                }
            }

            result = client_collection.update_one(filter_condition, update_fields)
            if result.matched_count == 0:
                self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
                self.response_format["data"] = None
                self.response_format["error"] = "Client"
                self.response_format["message"] = [messages.DOES_NOT_EXIST.format("Client")]

            elif result.matched_count == result.modified_count:
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["data"] = None
                self.response_format["error"] = None
                self.response_format["message"] = [messages.UPDATED.format("Client")]

            else:
                self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
                self.response_format["data"] = None
                self.response_format["error"] = "Unexpected error"
                self.response_format["message"] = [messages.UNEXPECTED_ERROR]

        return Response(self.response_format)

class DeleteClientAPIView(DestroyAPIView):
    """
    Class to create API to delete client.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MongoDBAuthentication,)

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(DeleteClientAPIView, self).__init__(**kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Method to delete client.
        """
        try:
            client_id = self.kwargs["pk"]

            # Set foreignkey to null for client to be deleted.
            # projects = project_collection.update_many(
            #     {"client_id": ObjectId(client_id)},
            #     {"$set": {"client_id": None}}
            # )

            # Delete all projects related to client
            projects = project_collection.delete_many({"client_id": ObjectId(client_id)})

            client = client_collection.delete_one({"_id": ObjectId(client_id)})
            if client.deleted_count > 0:
                self.response_format["status_code"] = status.HTTP_204_NO_CONTENT
                self.response_format["data"] = None
                self.response_format["error"] = None
                self.response_format["message"] = [messages.DELETED.format("Client")]
            else:
                self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
                self.response_format["data"] = None
                self.response_format["error"] = "Client"
                self.response_format["message"] = [messages.DOES_NOT_EXIST.format("Client")]
        except InvalidId:
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["data"] = None
            self.response_format["error"] = "Client"
            self.response_format["message"] = [messages.INVALID_ID.format("Client")]

        return Response(self.response_format)



class CreateProjectAPIView(CreateAPIView):
    """
    Class to create Project.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MongoDBAuthentication,)
    serializer_class = ProjectSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(CreateProjectAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Post method to create client.
        """
        project_serializer = self.get_serializer(data=request.data)
        if project_serializer.is_valid(raise_exception=True):
            request_data = project_serializer.data
            request_data["created_by"] = ObjectId(request.user["_id"])
            request_data["client_id"] = ObjectId(request_data["client_id"])
            project_id = Project().create_project(request_data)

            project = Project().get_project_by_id(project_id)

            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["data"] = parse_json(project)
            self.response_format["error"] = None
            self.response_format["message"] = [messages.CREATED.format("Client")]
        return Response(self.response_format)


class GetProjectAPIView(RetrieveAPIView):
    """
    Class to create API to get project.
    """

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetProjectAPIView, self).__init__(**kwargs)

    def get_project(self, project_id):
        project = project_collection.aggregate(
            [
                {
                    "$match": {"_id": ObjectId(project_id)}
                },
                {
                    "$lookup": {
                        "from": "client",
                        "localField": "client_id",
                        "foreignField": "_id",
                        "as": "client"
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "name": 1,
                        "cost": 1,
                        "description": 1,
                        "created_at": 1,
                        "updated_at": 1,
                        "client": {
                            "first_name": {"$arrayElemAt": ["$client.first_name", 0]},
                            "last_name": {"$arrayElemAt": ["$client.last_name", 0]}
                        }
                    }
                }
            ]
        )
        return next(project, None)

    def get(self, request, *arg, **kwargs):
        """
        Method to get Project details.
        """
        project_id = self.kwargs["pk"]
        project = self.get_project(project_id)

        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["data"] = parse_json(project)
        self.response_format["error"] = None
        self.response_format["message"] = [messages.SUCCESS]

        return Response(self.response_format)


class GetAllProjectAPIView(RetrieveAPIView):
    """
    Class to create API to get project.
    """
    authentication_classes = (MongoDBAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetAllProjectAPIView, self).__init__(**kwargs)

    def get_all_projects(self):
        project = project_collection.aggregate(
            [
                {
                    "$lookup": {
                        "from": "client",
                        "localField": "client_id",
                        "foreignField": "_id",
                        "as": "client"
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "name": 1,
                        "cost": 1,
                        "description": 1,
                        "created_at": 1,
                        "updated_at": 1,
                        "client": {
                            "_id": {"$arrayElemAt": ["$client._id", 0]},
                            "first_name": {"$arrayElemAt": ["$client.first_name", 0]},
                            "last_name": {"$arrayElemAt": ["$client.last_name", 0]}
                        }
                    }
                }
            ]
        )
        return project

    def get(self, request, *arg, **kwargs):
        """
        Method to get Project details.
        """
        project = self.get_all_projects()

        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["data"] = parse_json(project)
        self.response_format["error"] = None
        self.response_format["message"] = [messages.SUCCESS]

        return Response(self.response_format)



