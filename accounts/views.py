from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from .permission import IsAdminOrReadOnly
from .serializer import StaffSerializer,GuardianSerializer,GuardianSerializerNested,StudentSerializer,LogSerializer
from .utils import compare, save_up, extract_face_haar_cascade3,image_to_numpy
from .models import Student,Guardian,Staff,Log
from PIL import Image
from io import BytesIO
from rest_framework.exceptions import ValidationError
from django.core.files.base import ContentFile




class StaffView(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    # permission_classes = [IsAdminUser]

    


class GuardianView(ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer

class GuardianViewNested(ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializerNested

    # # permission_classes = [IsAdminOrReadOnly]
    def get_serializer_context(self):
        return {"student_id": self.kwargs["student_pk"]}

    def get_queryset(self):
        return Guardian.objects.filter(students__id=self.kwargs["student_pk"])

    def perform_create(self, serializer):
        student_id = self.kwargs["student_pk"]
        user_photo = self.request.data["user_photo"].read()
        user_photo = image_to_numpy(user_photo)
        processed_img = extract_face_haar_cascade3(user_photo)

        if processed_img is None:
             raise ValidationError({"detail":"No face found in the image"})
        pil_image = Image.fromarray(processed_img)

        # Convert PIL Image to a file-like object
        image_io = BytesIO()
        pil_image.save(image_io, format='JPEG')  # Adjust format based on your image format
        image_file = ContentFile(image_io.getvalue(), name='user_photo.jpg')  # Adjust the name as needed

        # Validate and set the student_id and user_photo before saving the instance
        serializer.validated_data["students"] = [student_id]
        serializer.validated_data["user_photo"] = image_file
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
        guardian = Guardian.objects.get(username=username)
        serializer = self.get_serializer(guardian)
        temp_path = save_up(user_photo)
        if temp_path is None:
            return Response(
                {"error": "No face found in the image"}, status=status.HTTP_400_BAD_REQUEST
            )
        result = compare(guardian.user_photo.path, temp_path)

        if result:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "You are no Authorized"}, status=status.HTTP_400_BAD_REQUEST
            )


    @action(detail=False, methods=["post"])
    def create_log(self, request, *args, **kwargs):
        student_id = request.data.get("student_id")
        guardian_id = request.data.get("guardian_id")
        student = Student.objects.get(id=student_id)
        guardian = Guardian.objects.get(id=guardian_id)
        staff = Staff.objects.get(user=request.user)

        try:
            log = Log.objects.create(student=student, guardian=guardian, staff=staff)
            student.is_present = False
            return Response(
                {"message": "Log object created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(f"An error occurred while creating the Log object: {e}")
            return Response(
                {"error": "Error creating Log object"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogView(ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAdminUser]
