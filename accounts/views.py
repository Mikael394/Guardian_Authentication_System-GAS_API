from io import BytesIO
from django.http import JsonResponse
from django.core.files.base import ContentFile
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from PIL import Image

from .permission import IsAdminOrReadOnly
from .serializer import AttendanceSerializer, ContactBookSerializer, ParentSerializer2, UserSerializer, ContactBookSerializerNested, GradeAndSectionSerializer, HomeRoomTeacherSerializer, ParentSerializer, AuthenticatorSerializer,GuardianSerializer,GuardianSerializerNested,StudentSerializer,LogSerializer, VideoSerializer
from .utils import compare, save_up, extract_face_haar_cascade3,image_to_numpy,process_image
from .models import Attendance, ContactBook, GradeAndSection, HomeRoomTeacher, Parent, Student,Guardian,Authenticator,Log, Video

class AuthenticatorView(ModelViewSet):
    queryset = Authenticator.objects.all()
    serializer_class = AuthenticatorSerializer
    # permission_classes = [IsAdminUser]
def are_the_same(processed_img):
    c1 = compare(processed_img[0],processed_img[1])
    c2 = compare(processed_img[0],processed_img[2])
    c3 = compare(processed_img[1],processed_img[2])

    return (c1 and c2 and c3)

def transform_data(data):
    transformed_data = {
        "user": {
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
            "username": data.get("username", ""),
            "email": data.get("email", ""),
            "phone_number": data.get("phone_number", ""),
            "gender": data.get("gender", None),
            "date_of_birth": data.get("date_of_birth", None),
            "password": data.get("password", ""),
        },
        "user_photo_1": data.get("user_photo_1", None),
        "user_photo_2": data.get("user_photo_2", None),
        "user_photo_3": data.get("user_photo_3", None),
    }
    return transformed_data

def create_user(data):
    transformed_data = {
        "first_name": data.get("first_name", ""),
        "last_name": data.get("last_name", ""),
        "username": data.get("username", ""),
        "email": data.get("email", ""),
        "phone_number": data.get("phone_number", ""),
        "gender": data.get("gender", None),
        "date_of_birth": data.get("date_of_birth", None),
        "password": data.get("password", "")
    }
    return transformed_data

# class ParentView(ModelViewSet):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer

    # def perform_create(self, serializer):
    #     user_data = create_user(self.request.data)
    #     user_photos = [self.request.data["user_photo_1"].read(),self.request.data["user_photo_2"].read(),self.request.data["user_photo_3"].read()]
    #     processed_img = []

    #     for index, photo in enumerate(user_photos):
    #         pr_image = process_image(photo)
    #         if pr_image is None:
    #             raise ValidationError({"detail":f"No face found in the image_{index+1}"})
    #         processed_img.append(pr_image)
    #     # if are_the_same(processed_img):
    #         # Validate and set the student_id and user_photo before saving the instance
    #     serializer.validated_data["user_photo_1"] = processed_img[0]
    #     serializer.validated_data["user_photo_2"] = processed_img[1]
    #     serializer.validated_data["user_photo_3"] = processed_img[2]
    #     serializer.validated_data["user"] = user_data
    #     serializer.save()

    #     # else:
    #     #     raise ValidationError({"detail":"Not the same person!"})

    
    
class ParentView(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    @action(detail=True, methods=["get", "post"])
    def activate(self, request, *args, **kwargs):
        parent_id = self.kwargs["pk"]

        if request.method == "GET":
            # Return guardians that are not associated with the student
            parents_list = Parent.objects.filter(user__is_active=False)
            serializer = ParentSerializer(parents_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            user_photos = [request.data["user_photo_1"].read(),request.data["user_photo_2"].read(),request.data["user_photo_3"].read()]
            processed_img = []
            try:
                parent = Parent.objects.get(user_id=parent_id)
            except Parent.DoesNotExist:
                return Response(
                    {"detail": "Parent not found"}, status=status.HTTP_404_NOT_FOUND
                )

            for index, photo in enumerate(user_photos):
                pr_image = process_image(photo)
                if pr_image is None:
                    raise ValidationError({"detail":f"No face found in the image_{index+1}"})
                processed_img.append(pr_image)
            parent.user_photo_1 = processed_img[0]
            parent.user_photo_2 = processed_img[1]
            parent.user_photo_3 = processed_img[2]
            parent.save()
            
            return Response(
                {"detail": "Activated successfully"},
                status=status.HTTP_200_OK,
            )



      

class HomeRoomTeacherView(ModelViewSet):
    queryset = HomeRoomTeacher.objects.all()
    serializer_class = HomeRoomTeacherSerializer

class GradeAndSectionView(ModelViewSet):
    queryset = GradeAndSection.objects.all()
    serializer_class = GradeAndSectionSerializer

class ContactBookView(ModelViewSet):
    queryset = ContactBook.objects.all()
    serializer_class = ContactBookSerializer

class VideoListCreate(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class ContactBookViewNested(ModelViewSet):
    queryset = ContactBook.objects.all()
    serializer_class = ContactBookSerializerNested

    def get_serializer_context(self):
        return {"student_id": self.kwargs["student_pk"]}

    def get_queryset(self):
        return ContactBook.objects.filter(student__id=self.kwargs["student_pk"])

    def perform_create(self, serializer):
        student = Student.objects.get(id = self.kwargs["student_pk"])
        hrt = HomeRoomTeacher.objects.get(user__id="fdc3d8ff-6a60-43d7-bfa1-9787b05be344")
        print(hrt)
        
        # Validate and set the student_id and user_photo before saving the instance
        serializer.validated_data["student"] = student
        serializer.validated_data["home_room_teacher"] = hrt
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GuardianView(ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer

class LogViewNested(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    #permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        print(self.kwargs)
        return {"student_id": self.kwargs["student_pk"]}

    def get_queryset(self):
        print(self.kwargs)
        return Log.objects.filter(student__id=self.kwargs["student_pk"])


class GuardianViewNested(ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializerNested
    # permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {"student_id": self.kwargs["student_pk"]}

    def get_queryset(self):
        return Guardian.objects.filter(students__id=self.kwargs["student_pk"])

    def perform_create(self, serializer):
        student_id = self.kwargs["student_pk"]
        user_photos = [self.request.data["user_photo_1"].read(),self.request.data["user_photo_2"].read(),self.request.data["user_photo_3"].read()]
        processed_img = []

        for index, photo in enumerate(user_photos):
            pr_image = process_image(photo)
            if pr_image is None:
                raise ValidationError({"detail":f"No face found in the image_{index+1}"})
            processed_img.append(pr_image)

        # Validate and set the student_id and user_photo before saving the instance
        serializer.validated_data["students"] = [student_id]
        serializer.validated_data["user_photo_1"] = processed_img[0]
        serializer.validated_data["user_photo_2"] = processed_img[1]
        serializer.validated_data["user_photo_3"] = processed_img[2]
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def perform_destroy(self, instance):
        student_id = self.kwargs["student_pk"]

        # Remove the association between the guardian and the student
        instance.students.remove(student_id)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get", "post"])
    def add_guardian(self, request, *args, **kwargs):
        student_id = self.kwargs["student_pk"]
        guardian_id = request.data.get("guardian_id")

        if request.method == "GET":
            # Return guardians that are not associated with the student
            unassociated_guardians = Guardian.objects.exclude(students__id=student_id)
            serializer = GuardianSerializerNested(unassociated_guardians, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            try:
                guardian = Guardian.objects.get(id=guardian_id)
            except Guardian.DoesNotExist:
                return Response(
                    {"detail": "Guardian not found"}, status=status.HTTP_404_NOT_FOUND
                )
            if guardian.students.filter(id=student_id).exists():
                return Response(
                    {"detail": "Guardian is already associated with the student"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Add the guardian to the student
            guardian.students.add(student_id)

            # You can return a success response or the updated data as needed
            return Response(
                {"detail": "Guardian added to student successfully"},
                status=status.HTTP_200_OK,
            )


class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=["get", "post"])
    def assign_parent(self, request, *args, **kwargs):
        student_id = self.kwargs["pk"]
        parent_id = request.data.get("parent_id")

        if request.method == "GET":
            # Return guardians that are not associated with the student
            parents_list = Parent.objects.all()
            serializer = ParentSerializer(parents_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            try:
                parent = Parent.objects.get(user_id=parent_id)
            except Parent.DoesNotExist:
                return Response(
                    {"detail": "Parent not found"}, status=status.HTTP_404_NOT_FOUND
                )
            if parent.students.filter(id=student_id).exists():
                return Response(
                    {"detail": "Parent is already associated with the student"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Add the guardian to the student
            parent.students.add(student_id)

            # You can return a success response or the updated data as needed
            return Response(
                {"detail": "Parent added to student successfully"},
                status=status.HTTP_200_OK,
            )

class StudentViewNested(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # permission_classes = [IsAdminOrReadOnly]
    # def get_serializer_context(self):
    #     return {"student_id": self.kwargs["student_pk"]}

    def get_queryset(self):
        return Student.objects.filter(guardians__id=self.kwargs["guardian_pk"])

    def perform_destroy(self, instance):
        guardian_id = self.kwargs["guardian_pk"]

        # Remove the association between the guardian and the student
        instance.guardians.remove(guardian_id)

        return Response(status=status.HTTP_204_NO_CONTENT)

class Verify(ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        user_photo = request.data.get("user_photo", None)
        if not username or not user_photo:
            return Response(
                {"error": "username and face is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            guardian = Guardian.objects.get(username=username)
        except Guardian.DoesNotExist:
                return Response(
                    {"detail": "Guardian not found with this"}, status=status.HTTP_404_NOT_FOUND
                )
        serializer = self.get_serializer(guardian)
        temp_path = save_up(user_photo)
        if temp_path is None:
            return Response(
                {"error": "No face found in the image"}, status=status.HTTP_400_BAD_REQUEST
            )
        result = compare(guardian.user_photo_1.path, temp_path)

        if result:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("not authorized...")
            return Response(
                {"error": "You are not Authorized"}, status=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=False, methods=["post"])
    def create_log(self, request, *args, **kwargs):
        student_id = request.data.get("student_id")
        guardian_id = request.data.get("guardian_id")
        # Authenticator_id = request.data.get("guardian_id")
        student = Student.objects.get(id=student_id)
        guardian = Guardian.objects.get(id=guardian_id)
        authenticator = request.user

        try:
            log = Log.objects.create(student=student, guardian=guardian, authenticator=authenticator)
            serializer = LogSerializer(log)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"An error occurred while creating the Log object: {e}")
            return Response(
                {"error": "Error creating Log object"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class AttendanceView(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
class AttendanceViewNested(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    def get_serializer_context(self):
        
        return {"grade_id": self.kwargs["grade_pk"]}
    
    def get_queryset(self):
        return Attendance.objects.filter(grade__id=self.kwargs["grade_pk"])

    
    

class LogView(ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    # permission_classes = [IsAdminUser]
