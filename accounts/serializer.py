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


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
        ]


class StudentSerializer(serializers.ModelSerializer):
    # guardians = GuardianSerializer(many=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "class_name",
            "guardians",
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


class StaffSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    # user = UserCreateSerializer()

    class Meta:
        model = Staff
        fields = ["user_id", "phone_number", "role"]


class GuardianSerializer(serializers.ModelSerializer):
    # students = serializers.StringRelatedField()
    students = SimpleStudentSerializer(many=True)

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


class GuardianVerifySerializer(serializers.ModelSerializer):
    # students = StudentSerializer(many=True)
    # students = serializers.StringRelatedField()

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
