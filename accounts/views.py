from io import BytesIO
from datetime import datetime
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from PIL import Image

from .permission import IsAdminOrReadOnly
from .serializer import AttendanceSerializer, ContactBookSerializer, StudentSerializerReg, UserSerializer, ContactBookSerializerNested, GradeAndSectionSerializer, HomeRoomTeacherSerializer, ParentSerializer, AuthenticatorSerializer,GuardianSerializer,GuardianSerializerNested,StudentSerializer,LogSerializer, VideoSerializer
from .utils import compare, save_up, extract_face_haar_cascade3,image_to_numpy,process_image
from .models import Attendance, ContactBook, GradeAndSection, HomeRoomTeacher, Parent, Student,Guardian,Authenticator,Log, User, Video


class AuthenticatorView(ModelViewSet):
    queryset = Authenticator.objects.all()
    serializer_class = AuthenticatorSerializer
    # permission_classes = [IsAdminUser]
def are_the_same(processed_img):
    c1 = compare(processed_img[0],processed_img[1])
    c2 = compare(processed_img[0],processed_img[2])
    c3 = compare(processed_img[1],processed_img[2])

    return (c1 and c2 and c3)

class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    

    
class ParentView(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    

    @action(detail=False, methods=["get", "post"])
    def activate(self, request, *args, **kwargs):
        
        if request.method == "GET":
            # Return guardians that are not associated with the student
            parents_list = Parent.objects.filter(user__is_active=False)
            serializer = ParentSerializer(parents_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            parent_id = request.data["parent_id"]
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
            if not parent.user.is_active:
                parent.user_photo_1 = processed_img[0]
                parent.user_photo_2 = processed_img[1]
                parent.user_photo_3 = processed_img[2]
                parent.user.is_active = True
                parent.user.save()
                parent.save()
                return Response(
                    {"detail": "Activated successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": "Already activated!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    @action(detail=False, methods=["get","post"])
    def remove_first_login(self, request, *args, **kwargs):
        if request.method == "GET":
            # Return guardians that are not associated with the student
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            user_id = request.data["id"]
            user = User.objects.get(id = user_id)
            user.is_first_login = False
            user.save()

            return Response(
                {"detail": "First Login status changed successfully..."},
                status=status.HTTP_200_OK,
            )
    
     
class HomeRoomTeacherView(ModelViewSet):
    queryset = HomeRoomTeacher.objects.all()
    serializer_class = HomeRoomTeacherSerializer


    @action(detail=False, methods=["get", "post"])
    def activate(self, request, *args, **kwargs):
        # hrt_id = self.kwargs["pk"]

        if request.method == "GET":
            # Return guardians that are not associated with the student
            hrt_list = HomeRoomTeacher.objects.filter(user__is_active=False)
            serializer = HomeRoomTeacherSerializer(hrt_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            hrt_id = request.data["hrt_id"]            
            try:
                hrt = HomeRoomTeacher.objects.get(user_id=hrt_id)
            except Parent.DoesNotExist:
                return Response(
                    {"detail": "Home room teacher not found"}, status=status.HTTP_404_NOT_FOUND
                )

            if not hrt.user.is_active:
                hrt.user.is_active = True
                hrt.user.save()
                hrt.save()
                return Response(
                    {"detail": "Activated successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": "Already activated!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["get", "post"])
    def take_attendance(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            hrt = HomeRoomTeacher.objects.get(user=user)
            section = GradeAndSection.objects.get(home_room_teacher=hrt)
        except HomeRoomTeacher.DoesNotExist:
            return Response(
                {"detail": "Home room teacher not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "GET":
            students = Student.objects.filter(grade=section)
            serializer = StudentSerializer(students,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "POST":
            pre_students = request.data
            students_id = []
            print(pre_students)
            attendance = Attendance.objects.create(grade=section)
            for student_id in pre_students.values():
                attendance.students.add(student_id)
                students_id.append(student_id)
                # student = Student.objects.get(id = self.kwargs["student_pk"])
                
            attendance.save()
            present_students = Student.objects.filter(id__in=students_id)
            present_students.update(is_present = True)

            return Response(
                {"detail": "Attendance taken successfully"},
                status=status.HTTP_200_OK,
            )

    @action(detail=False, methods=["get", "post","patch",])
    def manage_grade(self, request, *args, **kwargs):

        if request.method == "GET":
            # Return guardians that are not associated with the student
            section_list = GradeAndSection.objects.all()
            serializer = GradeAndSectionSerializer(section_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            hrt_id = request.data["hrt_id"]
            grade_id = request.data["grade_id"]

            try:
                hrt = HomeRoomTeacher.objects.get(user_id=hrt_id)
                section = GradeAndSection.objects.get(id=grade_id)
                
            except Parent.DoesNotExist:
                return Response(
                    {"detail": "Home room teacher not found"}, status=status.HTTP_404_NOT_FOUND
                )
            print(section.home_room_teacher and hrt.section)
            if (section.home_room_teacher is None) and (hrt.section is None):
                section.home_room_teacher = hrt
                section.save()
            elif section.home_room_teacher == hrt :
                return Response( 
                {"detail": "Home Room Teacher is already assigned to this Section."},
                status=status.HTTP_200_OK,
            )
            else:
                
                return Response( 
                {"detail": "Home Room Teacher is already assigned to other section please remove first."},
                status=status.HTTP_200_OK,
            )

                

        elif request.method == "PATCH":
            hrt_id = request.data["hrt_id"]

            try:
                hrt = HomeRoomTeacher.objects.get(user_id=hrt_id)
                section = GradeAndSection.objects.get(home_room_teacher=hrt)
            except Parent.DoesNotExist:
                return Response(
                    {"detail": "Home room teacher not found"}, status=status.HTTP_404_NOT_FOUND
                )
            
            section.home_room_teacher = None
            section.save()

            return Response(
                {"detail": "Section removed successfully"},
                status=status.HTTP_200_OK,
            )
            





class GradeAndSectionView(ModelViewSet):
    queryset = GradeAndSection.objects.all()
    serializer_class = GradeAndSectionSerializer



class ContactBookView(ModelViewSet):
    queryset = ContactBook.objects.all()
    serializer_class = ContactBookSerializer
    
    @action(detail=False,methods=['get','poost','patch'])
    def contact_book_parent(self,request,*args,**kwargs):
        if request.method == "GET":
            user = request.user
            if isinstance(user, AnonymousUser):
                return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                parent = Parent.objects.get(user=user)
                students = parent.students.all()
            except HomeRoomTeacher.DoesNotExist:
                return Response(
                    {"detail": "parent does not found"}, status=status.HTTP_404_NOT_FOUND
                )
        
            contact_books = ContactBook.objects.filter(student__in=students)
            serializer = ContactBookSerializer(contact_books,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method =="PATCH":
            contact_book_id = request.data["cb_id"]
            p_comment = request.data["p_comment"]
            contact_book = ContactBook.objects.get(id=contact_book_id)
            
            contact_book.parent_comment=p_comment
            contact_book.is_read_p = True
            contact_book.save()
            serializer = ContactBookSerializer(contact_book)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
    @action(detail=False,methods=['get','post','patch'])
    def contact_book_hrt(self,request,*args,**kwargs):
        if request.method == "GET":
            user = request.user
            if isinstance(user, AnonymousUser):
                return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                hrt = HomeRoomTeacher.objects.get(user=user)
            except HomeRoomTeacher.DoesNotExist:
                return Response(
                    {"detail": "Home room teacher does not found"}, status=status.HTTP_404_NOT_FOUND
                )
        
            contact_books = ContactBook.objects.filter(home_room_teacher=hrt)
            serializer = ContactBookSerializer(contact_books,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            info_type = request.data["info_type"]
            if info_type == "student":
                student_id = request.data["student_id"]
                
                contact_books = ContactBook.objects.filter(student__id=student_id)
                serializer = ContactBookSerializer(contact_books,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                contact_book_id = request.data["cb_id"]
                contact_book = ContactBook.objects.get(id=contact_book_id)
                serializer = ContactBookSerializer(contact_book)
                return Response(serializer.data, status=status.HTTP_200_OK)
               
        elif request.method == "PATCH":
            contact_book_id = request.data["cb_id"]
            contact_book = ContactBook.objects.get(id=contact_book_id)
            
            

            contact_book.is_read_t = True
            contact_book.save()
            serializer = ContactBookSerializer(contact_book)
            return Response(serializer.data, status=status.HTTP_200_OK)
            

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
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        student = Student.objects.get(id = self.kwargs["student_pk"])
        hrt = HomeRoomTeacher.objects.get(user=user)
        
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
class StudentViewReg(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializerReg


class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=True, methods=["get"])
    def view_parent(self, request, *args, **kwargs):
        student_id = self.kwargs["pk"]
        parents_list = Parent.objects.filter(students__id=student_id)
        serializer = ParentSerializer(parents_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get", "post"])
    def assign_parent(self, request, *args, **kwargs):
        student_id = self.kwargs["pk"]
        parent_id = request.data.get("parent_id")

        if request.method == "GET":
            # Return guardians that are not associated with the student
            parents_list = Parent.objects.exclude(students__id=student_id)
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

            return Response(
                {"detail": "Parent added to student successfully"},
                status=status.HTTP_200_OK,
            )
    
    @action(detail=True, methods=["get", "post"])
    def remove_parent(self, request, *args, **kwargs):
        student_id = self.kwargs["pk"]
        parent_id = request.data.get("parent_id")

        if request.method == "GET":
            parents_list = Parent.objects.filter(students__id=student_id)
            serializer = ParentSerializer(parents_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            try:
                parent = Parent.objects.get(user_id=parent_id)
            except Parent.DoesNotExist:
                return Response(
                    {"detail": "Parent not found"}, status=status.HTTP_404_NOT_FOUND
                )

            parent.students.remove(student_id)
            parent.save()

            return Response(
                {"detail": "Parent removed successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )


class StudentViewNested(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

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
        person = request.data.get("person", None)
        username = request.data.get("username", None)
        user_photo = request.data.get("user_photo", None)
        if not username or not user_photo:
            return Response(
                {"error": "username and face is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if person == "parent":
            try:
                parent = Parent.objects.get(user__username=username)
            except Parent.DoesNotExist:
                    return Response(
                        {"detail": "Parent not found with this user name"}, status=status.HTTP_404_NOT_FOUND
                    )
            serializer = ParentSerializer(parent)
            temp_path = save_up(user_photo)
            if temp_path is None:
                return Response(
                    {"error": "No face found in the image"}, status=status.HTTP_400_BAD_REQUEST
                )
            result = compare(parent.user_photo_1.path, temp_path)

            if result:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "You are not Authorized"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
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
        authenticator = Authenticator.objects.get(user=request.user)
        print(authenticator)

        try:
            log = Log.objects.create(student=student, guardian=guardian, authenticator=authenticator)
            student.is_present = False
            student.save()
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

    @action(detail=False, methods=["get"])
    def todays_attendance(self, request, *args, **kwargs):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y-%m-%d")
        attendance = Attendance.objects.get(date=formatted_date)
        serializers = AttendanceSerializer(attendance)
        return Response(serializers.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=["get","post"])
    def get_attendance(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, AnonymousUser):
        # Handle the case where request.user is AnonymousUser
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            hrt = HomeRoomTeacher.objects.get(user=user)
            section = GradeAndSection.objects.get(home_room_teacher=hrt)
        except HomeRoomTeacher.DoesNotExist:
            return Response(
                {"detail": "Home room teacher not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "GET":
            attendance = Attendance.objects.filter(grade=section)
            serializer = AttendanceSerializer(attendance,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            r_date = request.data["date"]

            try:
                attendance = Attendance.objects.get(grade=section,date=r_date)
            except Attendance.DoesNotExist:
                return Response(
                    {"detail": "No attendance registered on this date"}, status=status.HTTP_404_NOT_FOUND
                )
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_200_OK)       

    
class AttendanceViewNested(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
    
class LogView(ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
