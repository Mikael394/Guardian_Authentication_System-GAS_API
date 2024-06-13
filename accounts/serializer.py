from django.contrib.auth import get_user_model
from django.forms import ValidationError
from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from .models import (
    Attendance,
    ContactBook,
    GradeAndSection,
    HomeRoomTeacher,
    Parent,
    Student,
    Guardian,
    Authenticator,
    Log,
    Video,
)
User = get_user_model()


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
            "is_active",
            "is_parent",
            "is_hrt",
            "is_staff",
            "is_first_login",
            "is_authenticator",
            "date_of_birth",
            "password",
        ]
        read_only_fields = [
            "is_active",
            "is_parent",
            "is_hrt",
            "is_authenticator",
            "is_first_login",
            "is_staff",
        ]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "gender",
            "date_of_birth",
            "is_active",
            "is_first_login",
            "is_parent",
            "is_hrt",
            "is_staff",
            "is_authenticator",
        ]
        read_only_fields = [
            "is_active",
            "is_parent",
            "is_hrt",
            "is_authenticator",
            "is_first_login",
        ]
class GradeAndSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradeAndSection
        fields = ["id", "grade", "home_room_teacher"]

class SimpleStudentSerializer(serializers.ModelSerializer):
    grade = GradeAndSectionSerializer()
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "grade", "image","is_present"]


class GuardianSerializer(serializers.ModelSerializer):
    students = SimpleStudentSerializer(many=True, required=False)

    class Meta:
        model = Guardian
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "address",
            "phone_number",
            "relationship",
            "students",
            "user_photo_1",
            "user_photo_2",
            "user_photo_3",
        ]


class HomeRoomTeacherSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = HomeRoomTeacher
        fields = ["user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.is_hrt = True
        user.save()
        hrt = HomeRoomTeacher.objects.create(user=user, **validated_data)
        return hrt


class ParentSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Parent
        fields = ["user", "user_photo_1", "user_photo_2", "user_photo_3"]

        read_only_fields = ["user_photo_1", "user_photo_2", "user_photo_3"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.is_parent = True
        user.save()
        parent = Parent.objects.create(user=user)
        return parent



class ContactBookSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = ContactBook
        fields = [
            "id",
            "date_time",
            "home_room_teacher",
            "parents_follow_up",
            "hand_writing",
            "reading_skill",
            "material_handling",
            "happy",
            "wear_uniform",
            "has_good_time_while_eating",
            "active_participation",
            "teacher_comment",
            "parent_comment",
            "is_read_p",
            "is_read_t",
        ]
        read_only_fields = ['home_room_teacher']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("id", "file", "uploaded_at")





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
            "user_photo_1",
            "user_photo_2",
            "user_photo_3",
            "relationship",
        ]


class SimpleGuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = [
            "id",
            "username",
            "user_photo_1",
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
            "user_photo_1",
            "user_photo_2",
            "user_photo_3",
        ]


class StudentSerializer(serializers.ModelSerializer):
    guardians = SimpleGuardianSerializer(many=True, required=False)
    grade = GradeAndSectionSerializer()
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "image",
            "last_name",
            "date_of_birth",
            "gender",
            "grade",
            "guardians",
            "parents",
            "is_present",
        ]
        
class ContactBookSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = ContactBook
        fields = [
            "id",
            "student",
            "home_room_teacher",
            "date_time",
            "parents_follow_up",
            "hand_writing",
            "reading_skill",
            "material_handling",
            "happy",
            "wear_uniform",
            "has_good_time_while_eating",
            "active_participation",
            "teacher_comment",
            "parent_comment",
            "is_read_p",
            "is_read_t",
        ]
        read_only_fields = ['home_room_teacher']


class AuthenticatorSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Authenticator
        fields = ["user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.is_authenticator = True
        user.save()
        authenticator = Authenticator.objects.create(user=user, **validated_data)
        return authenticator


class SimpleGuardianSerializerForLog(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = ["id", "username"]


class SimpleAuthenticatorSerializerForLog(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Authenticator
        fields = ["user_id", "user"]


class SimpleStudentSerializerForLog(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name"]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["students","grade", "date"]


class AttendanceSerializerNested(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["students", "date"]


class LogSerializer(serializers.ModelSerializer):
    guardian = SimpleGuardianSerializerForLog()
    authenticator = SimpleAuthenticatorSerializerForLog()
    student = SimpleStudentSerializerForLog()

    class Meta:
        model = Log
        fields = [
            "id",
            "student",
            "guardian",
            "authenticator",
            "date_time",
            "action",
        ]
