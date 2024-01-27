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

    # def create(self, validated_data):
    #     student_id = self.context["student_id"]
    #     print(student_id)
    #     student = Student.objects.get(id=student_id)
    #     guardian = Guardian.objects.create(**validated_data)
    #     guardian.students.add(student)
    #     return guardian


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

    # def create(self, validated_data):
    #     guardians_data = validated_data.pop("guardians")
    #     student = Student.objects.create(**validated_data)
    #     for guardian_data in guardians_data:
    #         guardian_id = guardian_data.get("id")
    #         if guardian_id:
    #             guardian = Guardian.objects.get(id=guardian_id)
    #             student.guardians.add(guardian)
    #             return student
    #         new_guardian = Guardian.objects.create(**guardian_data)
    #         student.guardians.add(new_guardian)
    #     return student

    # def partial_update(self, validated_data):
    #     guardians_data = validated_data.pop("guardians")
    #     student = Student.objects.create(**validated_data)
    #     for guardian_data in guardians_data:
    #         Guardian.objects.create(student=student, **guardian_data)
    #     return student

    # def update(self, instance, validated_data):
    #     guardians_data = validated_data.pop("guardians", [])

    #     for guardian_data in guardians_data:
    #         if "id" in guardian_data:
    #             # Add existing guardian to student
    #             guardian_id = guardian_data["id"]
    #             guardian = Guardian.objects.get(id=guardian_id)
    #             instance.guardians.add(guardian)
    #         else:
    #             # Create and add a new guardian to student
    #             new_guardian = Guardian.objects.create(**guardian_data)
    #             instance.guardians.add(new_guardian)

    #     return instance


class StaffSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    # user = UserCreateSerializer()

    class Meta:
        model = Staff
        fields = ["user_id", "phone_number", "role"]


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
