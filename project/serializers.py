from rest_framework import serializers


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


