from rest_framework import serializers
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from .models import (
    ContactBook,
    GradeAndSection,
    HomeRoomTeacher,
    Note,
    Parent,
    Student,
    Guardian,
    Staff,
    Log,
    User,
    Video,
)


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


# class UserSerializer(BaseUserSerializer):
#     class Meta(BaseUserSerializer.Meta):
#         fields = [
#             "id",
#             "first_name",
#             "last_name",
#             "username",
#             "is_staff",
#             "is_superuser",
#             "email",
#         ]


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
    user_id = serializers.UUIDField()

    class Meta:
        model = HomeRoomTeacher
        fields = ["user_id"]


class ParentSerializer(serializers.ModelSerializer):
    # user_id = serializers.UUIDField()
    user = UserCreateSerializer()

    class Meta:
        model = Parent
        fields = ["user", "user_photo"]

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        Parent.objects.create(user=user, **validated_data)
        return user

# class ParentSerializer(serializers.ModelSerializer):
#     parent = ParentSerializerUser()

#     class Meta:
#         model = User  # Assuming User is your parent model
#         fields = ('id', 'username', 'email', 'password', 'parent')

#     def create(self, validated_data):
#         guardian_data = validated_data.pop('guardian')
#         user = User.objects.create(**validated_data)
#         Guardian.objects.create(user=user, **guardian_data)
#         return user

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
            "is_read"
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
            "is_read"
        ]

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'file', 'uploaded_at')

class GradeAndSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradeAndSection
        fields = ["id", "grade", "section"]


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
        fields = ["id", "username"]


class SimpleStaffSerializerForLog(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = ["user_id", "user"]


class SimpleStudentSerializerForLog(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name"]


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



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
