import json
from bson import json_util
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView
)
from datetime import (
    datetime,
    timezone
)
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

from utilities import messages
from .permissions import (
    IsAdmin,
    IsAuthenticated
)
from .models import (
    CustomUser,
    black_list_collection
)
from utilities.utils import (
    parse_json,
    ResponseInfo,
    get_tokens_for_user
)
from .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
)
from .permissions import MongoDBAuthentication


class SignupAPIView(CreateAPIView):
    """
    Class to create register new user.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserProfileSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(SignupAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Method to create and register new user.
        """
        user_serializer = self.get_serializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_data = user_serializer.validated_data
            user_id = CustomUser().create_user(user_data)
            if user_id:
                self.response_format["status_code"] = status.HTTP_201_CREATED
                self.response_format["data"] = {"id": json.loads(json_util.dumps(user_id))["$oid"]}
                self.response_format["error"] = None
                self.response_format["message"] = [messages.CREATED.format("User")]
            else:
                self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
                self.response_format["data"] = None
                self.response_format["error"] = "User"
                self.response_format["message"] = [messages.UNEXPECTED_ERROR]

        return Response(self.response_format)


class LoginAPIView(CreateAPIView):
    """
    Class to log in user.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserLoginSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Method to login user and return jwt tokens.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = CustomUser().get_user_by_email(serializer.validated_data['username'])
            if user and check_password(serializer.validated_data['password'], user['password']):
                user = parse_json(user)

                jwt_token = get_tokens_for_user(user)

                response_data = {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email_name": user["email"],
                    "role": user["role"],
                    "token": jwt_token,

                }
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["data"] = response_data
                self.response_format["error"] = None
                self.response_format["message"] = [messages.LOGIN_SUCCESS]

            else:
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["data"] = None
                self.response_format["error"] = "User"
                self.response_format["message"] = [messages.INVALID_CREDENTIALS]

        return Response(self.response_format)


class LogoutAPIView(CreateAPIView):
    """
        Class for creating API view for user logout.
        """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MongoDBAuthentication,)

    def __init__(self, **kwargs):
        """
         Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST Method for logging out the user and blacklisting the access token used.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            key, access_token = auth_header.split(' ')
            refresh_token = request.data.get("refresh")

            black_list_collection.insert_many(
                [{"token": access_token, "timestamp": datetime.now(timezone.utc)},
                {"token": refresh_token, "timestamp": datetime.now(timezone.utc)}]
            )
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["data"] = None
            self.response_format["error"] = None
            self.response_format["message"] = [messages.LOGOUT_SUCCESS]
        return Response(self.response_format)




class GetUser(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MongoDBAuthentication,)

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetUser, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.response_format["data"] = request.user
        self.response_format["error"] = None
        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["message"] = [messages.SUCCESS]
        return Response(self.response_format)


class ListResourceAPIView(ListAPIView):
    authentication_classes = (MongoDBAuthentication,)
    permission_classes = (IsAuthenticated, IsAdmin)

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(ListResourceAPIView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        """
        Method to get list of resources.
        """
        resources = CustomUser().get_all_users()

        self.response_format["status_code"] = status.HTTP_200_OK
        self.response_format["data"] = parse_json(resources)
        self.response_format["error"] = None
        self.response_format["message"] = [messages.SUCCESS]
        return Response(self.response_format)
