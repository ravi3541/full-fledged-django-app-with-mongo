from bson.objectid import ObjectId
from rest_framework import serializers


from utilities import messages
from .models import client_collection


class ClientSerializer(serializers.Serializer):
    """
    Class to create serializer for creating client.
    """
    first_name = serializers.CharField(max_length=20, allow_null=False, allow_blank=False, required=True)
    last_name = serializers.CharField(max_length=20, allow_null=False, allow_blank=False, required=True)
    company_name = serializers.CharField(max_length=20, allow_null=False, allow_blank=False, required=True)
    company_address = serializers.CharField(max_length=100, allow_null=False, allow_blank=False, required=True)
    description = serializers.CharField(max_length=300, allow_null=True, allow_blank=False, required=True)


class ProjectSerializer(serializers.Serializer):
    """
    Class to create serializer for creating project.
    """
    name = serializers.CharField(max_length=20, allow_null=False, allow_blank=False, required=True)
    cost = serializers.FloatField(allow_null=False, required=True)
    client_id = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, required=True)
    description = serializers.CharField(max_length=300, allow_null=False, allow_blank=False, required=True)

    def validate_client_id(self, value):
        """
        Method to validate client_id.
        """
        client_exist = client_collection.find_one({"_id": ObjectId(value)})
        if not client_exist:
            raise serializers.ValidationError(messages.DOES_NOT_EXIST.format("Client"))
        return value



