from email.policy import default
from django.db import models
import uuid
from datetime import date
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=15)
    is_parent = models.BooleanField(default=False)
    is_hrt = models.BooleanField(default=False)
    is_authenticator = models.BooleanField(default=False)
    GENDER_FIELDS = [("Male", "Male"), ("Female", "Female")]
    gender = models.CharField(max_length=6, choices=GENDER_FIELDS)
    date_of_birth = models.DateField(default=date.today)
    address = models.CharField(max_length=30)

    @property
    def age(self):
        today = date.today()
        age = (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
        return age

    def __str__(self):
        return self.username

class Guardian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    user_photo = models.ImageField(upload_to="guardian_faces")
    user_photo_2 = models.ImageField(upload_to="guardian_faces", null=True)
    user_photo_3 = models.ImageField(upload_to="guardian_faces", null=True)
    phone_number = models.CharField(max_length=15, null=True)
    GENDER_FIELDS = [("Male", "Male"), ("Female", "Female")]
    gender = models.CharField(max_length=6, choices=GENDER_FIELDS, null=True)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=30,null=True)
    relationship = models.CharField(max_length=50)

    @property
    def age(self):
        today = date.today()
        age = (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
        return age
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class HomeRoomTeacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    user_photo = models.ImageField(upload_to="parents photo")
    RELATION = [("Father","Father"),("Mother","Mother")]
    relation = models.CharField(max_length=7,choices=RELATION)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class GradeAndSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grade = models.CharField(max_length=20)
    home_room_teacher = models.OneToOneField(HomeRoomTeacher,on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return f"{self.grade}"

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    grade_and_section = models.ForeignKey(GradeAndSection, on_delete = models.CASCADE)
    GENDER_FIELDS = [("Male", "Male"), ("Female", "Female")]
    gender = models.CharField(max_length=6, choices=GENDER_FIELDS)
    image = models.ImageField(upload_to="students/", null=True)
    guardians = models.ManyToManyField("Guardian", related_name="students", blank=True)
    parent = models.ForeignKey(Parent, on_delete = models.CASCADE, null =True,blank=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Authenticator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class ContactBook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    home_room_teacher = models.ForeignKey(HomeRoomTeacher, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    LEVEL = [("Very Good","Very Good"),("Good","Good"),("Fair","Fair"),("Need Improvement","Need Improvement")]
    yes_no = [("Yes","Yes"),("No","No")]
    parents_follow_up = models.CharField(max_length=20, choices=LEVEL)
    hand_writing = models.CharField(max_length=20, choices=LEVEL)
    reading_skill = models.CharField(max_length=20, choices=LEVEL)
    material_handling = models.CharField(max_length=20, choices=LEVEL)

    happy = models.CharField(max_length=20, choices=yes_no)
    wear_uniform = models.CharField(max_length=20, choices=yes_no)
    has_good_time_while_eating = models.CharField(max_length=20, choices=yes_no)
    active_participation = models.CharField(max_length=20, choices=yes_no)

    
    teacher_comment = models.TextField()
    parent_comment = models.TextField()

    is_read_p = models.BooleanField(default=False)
    is_read_t = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.student} - {self.date_time}"

class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    authenticator = models.ForeignKey(Authenticator, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=50, default="Picked Up")

    def __str__(self):
        return self.action
    
class Video(models.Model):
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
