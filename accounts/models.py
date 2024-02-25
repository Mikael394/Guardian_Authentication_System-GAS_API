from django.db import models
import uuid
from datetime import date
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=15)
    
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

    

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     processed_img = extract_face_haar_cascade(self.user_photo.path)
    #     pil_image = Image.fromarray(processed_img)
    #     pil_image.save(self.user_photo.path)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    GENDER_FIELDS = [("Male", "Male"), ("Female", "Female")]
    gender = models.CharField(max_length=6, choices=GENDER_FIELDS)
    grade = models.CharField(max_length=50)
    image = models.ImageField(upload_to="students/", null=True)
    guardians = models.ManyToManyField("Guardian", related_name="students", blank=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=50, default="Picked Up")

    def __str__(self):
        return self.action
