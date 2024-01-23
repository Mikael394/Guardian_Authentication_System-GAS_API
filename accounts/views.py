from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from .serializer import *
from .utils import compare, save_up
from .forms import *
from .models import *


class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


# class StaffViewSet(
#     CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
# ):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer


class TestView(ModelViewSet):
    queryset = TestAPI.objects.all()
    serializer_class = TestSerializer


class GuardianView(ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer


class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class Verify(ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticated]

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticated()]

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
        result = compare(guardian.user_photo.path, temp_path)
        staff = Staff.objects.get(user=request.user)

        def create_log(self, student_id, guardian):
            student = Student.objects.get(pk=student_id)
            Log.objects.create(
                student=student,
                staff=staff,
                guardian=guardian,
            )

        if result:
            for student in serializer.data.get("students"):
                create_log(self, student.get("id"), guardian)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "You are no Authorized"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogView(ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


# def login(request, name):
#     if request.method == "POST":
#         user_face = request.FILES["face_image"]
#         temp_path = save_up(user_face)
#         # print(user_face.path)
#         people = Person.objects.get(name=name)
#         status = compare(people.user_photo.path, temp_path)
#         if status:
#             verified_person = people
#             return render(request, "success.html", {"person": verified_person})
#         else:
#             return render(request, "failed.html")
#     return render(request, "login.html")


# def capture_data(request):
#     if request.method == "POST":
#         form = PersonForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("authorize")
#     else:
#         form = PersonForm()
#     return render(request, "capture_data.html", {"form": form})


# def authorize(request):
#     people = Person.objects.all()
# return render(request, "authorize.html", {"people": people})
