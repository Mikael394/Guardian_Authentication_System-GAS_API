from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from .models import (
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
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token
        token['username'] = user.username  # Add username to the token payload

        return token
    

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
    # guardians = GuardianSerializer(many=True)

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "grade", "is_present", "image"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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


class HomeRoomTeacherSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = HomeRoomTeacher
        fields = ["user"]

    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.is_hrt =True
        user.save()
        hrt=HomeRoomTeacher.objects.create(user=user, **validated_data)
        return hrt



class ParentSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Parent
        fields = ["user", "user_photo"]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.is_parent =True
        user.save()
        parent=Parent.objects.create(user=user, **validated_data)
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
            "is_read_t"
        ]

class ContactBookSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = ContactBook
        fields = [
            "id",
            # "student",
            # "home_room_teacher",
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
            "is_read_t"
        ]

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'file', 'uploaded_at')

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
            "gender",
            "is_present",
            "grade_and_section",
            "guardians",
        ]


class AuthenticatorSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Authenticator
        fields = ["user", "role"]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.is_authenticator =True
        user.save()
        authenticator=Authenticator.objects.create(user=user, **validated_data)
        return authenticator


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


