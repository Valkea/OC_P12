from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import EpicMember


class EpicMember_Serializer(serializers.ModelSerializer):
    """
    This serializer returns a PARTIAL translation of the EpicMember model
    """

    class Meta(object):
        model = EpicMember
        fields = (
            "id",
            "team",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """ Make sure to add the user in the staff """

        validated_data["is_staff"] = True

        return EpicMember(**validated_data)


class EpicMember_DETAILS_Serializer(serializers.ModelSerializer):
    """
    This serializer returns a translation of the FULL EpicMember model
    """

    date_joined = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()

    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False, allow_null=True, write_only=True)

    class Meta(object):
        model = EpicMember
        fields = "__all__"
        fields = (
            "id",
            "team",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "last_login",
            "date_joined",
            "created_time",
            "updated_time",
        )
        # extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        """ Make sure to encode the password when updating the user's profile """

        instance.team = validated_data.get("team", instance.team)
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.last_login = validated_data.get("last_login", instance.last_login)
        instance.is_active = validated_data.get("is_active", instance.is_active)

        password = validated_data.get("password", instance.password)
        if password and len(password) != 78 and password != "":
            instance.password = make_password(password)

        instance.save()
        return instance
