from rest_framework import serializers

from utilities import constants


class UserProfileSerializer(serializers.Serializer):
    """
    Class to create serializer class to validate request data.
    """
    first_name = serializers.CharField(max_length=20, allow_null=False, allow_blank=False, required=True)
    last_name = serializers.CharField(max_length=20, allow_null=False, allow_blank=False, required=True)
    email = serializers.CharField(max_length=255, allow_null=False, allow_blank=False, required=True)
    role = serializers.ChoiceField(allow_null=False, allow_blank=False, required=True, choices=constants.role_options)
    password = serializers.CharField(max_length=16, allow_null=False, allow_blank=False, required=True, write_only=True)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)