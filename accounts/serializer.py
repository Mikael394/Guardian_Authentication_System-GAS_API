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
    User,
    Video,
)


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
            "password",
        ]


class SimpleStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "grade", "is_present", "image"]


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
        fields = [
            "user",
            "user_photo_1",
            "user_photo_2",
            "user_photo_3",
            "students"
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.is_parent = True
        user.save()
        parent = Parent.objects.create(user=user, **validated_data)
        return parent


class ContactBookSerializer(serializers.ModelSerializer):

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


class ContactBookSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = ContactBook
        fields = [
            "id",
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


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("id", "title", "file", "uploaded_at")


class GradeAndSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradeAndSection
        fields = ["id", "grade"]


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

    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "image",
            "last_name",
            "date_of_birth",
            "gender",
            "grade_and_section",
            "guardians",
            "parents"
        ]


class AuthenticatorSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Authenticator
        fields = ["user", "role"]

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
        fields = ["students", "grade", "date"]


class AttendanceSerializerNested(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["students", "date"]


class LogSerializer(serializers.ModelSerializer):
    guardian = SimpleGuardianSerializerForLog()
    Authenticator = SimpleAuthenticatorSerializerForLog()
    student = SimpleStudentSerializerForLog()

    class Meta:
        model = Log
        fields = [
            "id",
            "student",
            "guardian",
            "Authenticator",
            "date_time",
            "action",
        ]
