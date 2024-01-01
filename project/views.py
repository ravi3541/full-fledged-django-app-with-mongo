from rest_framework import status
from bson.objectid import ObjectId
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response

from utilities import messages
from customuser.permissions import IsAuthenticated
from .models import (
    Client,
    Project
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
