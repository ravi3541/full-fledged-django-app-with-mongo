import os
import jwt
from jwt import (
    InvalidSignatureError,
    ExpiredSignatureError,
)
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

from utilities.utils import parse_json
from customuser.models import CustomUser


class MongoDBAuthentication(BaseAuthentication):
    """
    Class to authenticate incoming request.
    """

    def authenticate_user(self, token):
        try:
            user_id = jwt.decode(token, os.getenv("JWT_PUBLIC_KEY"), algorithms=["RS256"])
            if user_id and user_id["token_type"] == "access":
                user_obj = CustomUser().get_user_by_id(user_id["id"])
                user_obj.pop("password")

                return user_obj
            else:
                raise AuthenticationFailed(
                    _("Given token not valid for any token type."),
                )
        except InvalidSignatureError:
            raise AuthenticationFailed(
                _("Given token not valid for any token type."),
            )

        except ExpiredSignatureError:
            raise AuthenticationFailed(
                _("Token is invalid or expired."),
            )

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            key, token = auth_header.split(' ')

            if key == 'Bearer':
                user_data = self.authenticate_user(token)
                if user_data:
                    user_data["is_authenticated"] = True
                    return parse_json(user_data), None
                else:
                    return None
        else:
            raise AuthenticationFailed(
                _("Authorization header must contain two space-delimited values."),
            )

        return None


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user["is_authenticated"])
