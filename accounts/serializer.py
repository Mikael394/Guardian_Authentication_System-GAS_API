from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from .models import Student,Guardian,Staff,Log,User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "gender",
            "date_of_birth",
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
            "grade",
            "is_present",
            "image"
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "is_staff",
            "is_superuser",
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
            "gender",
            "date_of_birth",
            "address",
            "phone_number",
            "relationship",
            "students",
        ]


class GuardianSerializerNested(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "phone_number",
            "gender",
            "date_of_birth",
            "address",
            "user_photo",
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
            "phone_number"
            
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
            "gender",
           "is_present",
            "grade",
            "guardians",
        ]


class StaffSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()

    class Meta:
        model = Staff
        fields = ["user_id", "role"]


# class GuardianVerifySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Guardian
#         fields = [
#             "id",
#             "username",
#             "user_photo",
#         ]


class SimpleGuardianSerializerForLog(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = [
            "id",
            "username"  
        ]

class SimpleStaffSerializerForLog(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Staff
        fields = [
            "user_id",
            "user"  
        ]

class SimpleStudentSerializerForLog(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name"
        ]


class LogSerializer(serializers.ModelSerializer):
    guardian = SimpleGuardianSerializerForLog()
    staff = SimpleStaffSerializerForLog()
    student = SimpleStudentSerializerForLog()
    class Meta:
        model = Log
        fields = [
            "id",
            "student",
            "guardian",
            "staff",
            "date_time",
            "action",
        ]
