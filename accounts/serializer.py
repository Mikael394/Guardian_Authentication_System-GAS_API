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


class ReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAPI
        fields = ["name"]


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


class StaffSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    # user = UserCreateSerializer()

    class Meta:
        model = Staff
        fields = ["user_id", "phone_number", "role"]


class GuardianSerializer(serializers.ModelSerializer):
    # students = serializers.StringRelatedField()
    students = StudentSerializer(many=True)

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
    students = StudentSerializer(many=True)
    # students = serializers.StringRelatedField()

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


# class TestSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = TestAPI
#         fields = ["name", "ects"]
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAPI
        fields = ["id", "name", "ects"]

    # def create(self, validated_data):
    #     print(**validated_data)
    # return TestAPI.objects.create(**validated_data)
