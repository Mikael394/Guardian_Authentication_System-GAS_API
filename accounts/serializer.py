from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from .models import *


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]


class SimpleStudentSerializer(serializers.ModelSerializer):
    # guardians = GuardianSerializer(many=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "class_name",
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
        ]


class GuardianSerializer(serializers.ModelSerializer):
    # students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    students = SimpleStudentSerializer(many=True, required=False)

    class Meta:
        model = Guardian
        fields = [
            "id",
            "username",
            "user_photo",
            "first_name",
            "last_name",
            "phone_number",
            "relationship",
            "students",
        ]


class GuardianSerializerNested(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = [
            "id",
            "username",
            "user_photo",
            "first_name",
            "last_name",
            "phone_number",
            "relationship",
        ]


class SimpleGuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = [
            "id",
            "username",
            "user_photo",
            "first_name",
            "last_name",
            "phone_number",
        ]


class GuardianVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = [
            "id",
            "username",
            "user_photo",
        ]


class StudentSerializer(serializers.ModelSerializer):
    # guardians = serializers.ListField(child=serializers.JSONField(), required=False)
    guardians = SimpleGuardianSerializer(many=True, required=False)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "image",
            "last_name",
            "date_of_birth",
            "class_name",
            "guardians",
        ]


class StaffSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()
    # user = UserCreateSerializer()

    class Meta:
        model = Staff
        fields = ["user_id", "phone_number", "role"]


class GuardianVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = [
            "id",
            "username",
            "user_photo",
        ]


class LogSerializer(serializers.ModelSerializer):
    # guardians = GuardianSerializer(many=True)

    class Meta:
        model = Log
        fields = [
            # "id",
            "student",
            "guardian",
            "staff",
            "date_time",
            "action",
        ]
