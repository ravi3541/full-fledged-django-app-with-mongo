import os
import json
import jwt
from jwt import (
    InvalidSignatureError,
    ExpiredSignatureError
)
from bson import json_util
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

from utilities import messages
from .models import (
    create_user,
    get_user_by_id,
    get_user_by_email,
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
            user_id = create_user(user_data)
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
            user = get_user_by_email(serializer.validated_data['username'])
            if user and check_password(serializer.validated_data['password'], user['password']):
                user = parse_json(user)

                jwt_token = get_tokens_for_user(user)

                response_data = {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email_name": user["email"],
                    "token": jwt_token

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


class GetUserProfileAPIView(RetrieveAPIView):
    """
    Class to create API for getting logged in users profile data.
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserLoginSerializer

    def __init__(self, **kwargs):
        """
        Constructor function for formatting the web response to return.
        """
        self.response_format = ResponseInfo().response
        super(GetUserProfileAPIView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        """
        Method to get logged user profile.
        """
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header:
                key, old_token = auth_header.split(' ')

                if key == 'Bearer':
                    user_id = jwt.decode(old_token, os.getenv("JWT_PUBLIC_KEY"), algorithms=["RS256"])
                    if user_id:
                        if user_id["token_type"] == "access":
                            user_obj = get_user_by_id(user_id["id"])
                            user_obj.pop("password")

                            user = parse_json(user_obj)
                            self.response_format["data"] = user
                            self.response_format["error"] = None
                            self.response_format["status_code"] = status.HTTP_200_OK
                            self.response_format["message"] = [messages.SUCCESS]
                        else:
                            self.response_format["data"] = None
                            self.response_format["error"] = "Token type"
                            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
                            self.response_format["message"] = [messages.INVALID_TOKEN_TYPE]

                    else:
                        self.response_format["data"] = None
                        self.response_format["error"] = "User Error"
                        self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
                        self.response_format["message"] = [messages.JWT_DECODE_ERROR]
            else:
                self.response_format["data"] = None
                self.response_format["error"] = "Bearer Error"
                self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = [messages.TOKEN_NOT_FOUND]
        except InvalidSignatureError:
            self.response_format["data"] = None
            self.response_format["error"] = "Token Error"
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = [messages.INVALID_TOKEN]
        except ExpiredSignatureError:
            self.response_format["data"] = None
            self.response_format["error"] = "Token Error"
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = [messages.TOKEN_EXPIRED]
        return Response(self.response_format)
