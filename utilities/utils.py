import os
import jwt
import json
from bson import json_util
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import exception_handler


class ResponseInfo(object):
    """
    Class for setting how API should send response.
    """

    def __init__(self, **args):
        self.response = {
            "status_code": args.get("status", 200),
            "error": args.get("error", None),
            "data": args.get("data", []),
            "message": [args.get("message", "Success")],
        }


# class CustomPermissionException(APIException):
#     status_code = status.HTTP_400_BAD_REQUEST
#     default_detail = "You do not have permission to perform this action."
#
#     def __init__(self, detail=None):
#         """
#         Method to display custom exception message
#         """
#         if detail is not None:
#             self.detail = detail
#         else:
#             self.detail = self.default_detail


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = dict()
        customized_response["error"] = []

        for key, value in response.data.items():
            error = key
            customized_response["status_code"] = response.status_code
            customized_response["error"] = error
            customized_response["data"] = None
            if response.status_code == 401:
                if type(value[0]) is dict:
                    customized_response["message"] = [value[0]["message"]]
                else:
                    customized_response["message"] = [value]
            else:
                if type(value) is list:
                    customized_response["message"] = [value[0]]
                else:
                    customized_response["message"] = [value]

        response.data = customized_response

    return response


def parse_json(data):
    parsed_data = json.loads(json_util.dumps(data))
    parsed_data["id"] = parsed_data["_id"]["$oid"] if parsed_data["_id"]["$oid"] else None
    parsed_data.pop("_id")

    return parsed_data


def get_tokens_for_user(user_obj):
    """
    function to create and returns JWT token in response
    """
    user_obj.pop("password")

    payload = {
        "id": user_obj["id"],
        "exp": timezone.now() + timedelta(minutes=10),
        "iat": timezone.now(),
        "token_type": "access"
    }

    access_token = jwt.encode(
        payload=payload,
        key=os.getenv("JWT_PRIVATE_KEY"),
        algorithm='RS256'
    )

    payload["exp"] = timezone.now() + timedelta(days=5)
    payload["token_type"] = "refresh"

    refresh_token = jwt.encode(
        payload=payload,
        key=os.getenv("JWT_PRIVATE_KEY"),
        algorithm='RS256'
    )
    return {
        'refresh': refresh_token,
        'access': access_token,
    }
