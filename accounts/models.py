from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .utils import extract_face_haar_cascade, resize_image
from PIL import Image


class User(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)

    def __str__(self):
        return self.username


class Guardian(models.Model):
    username = models.CharField(max_length=50, unique=True)
    user_photo = models.ImageField(upload_to="guardian_faces")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=50)
    students = models.ManyToManyField("Student", related_name="guardians")
    # user_encoding_photo = models.BinaryField(null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        processed_img = extract_face_haar_cascade(self.user_photo.path)
        processed_img = resize_image(processed_img, 0.5)
        pil_image = Image.fromarray(processed_img)
        pil_image.save(self.user_photo.path)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    class_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Staff(models.Model):
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Log(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=50, default="Picked Up")

    def __str__(self):
        return self.action


class Person(models.Model):
    name = models.CharField(max_length=100)
    user_photo = models.ImageField(upload_to="")
    # user_encoding_photo = models.BinaryField(null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        processed_img = extract_face_haar_cascade(self.user_photo.path)
        processed_img = resize_image(processed_img, 0.5)
        pil_image = Image.fromarray(processed_img)
        pil_image.save(self.user_photo.path)

    def __str__(self):
        return self.name


class TestAPI(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    # photo = models.ImageField(upload_to="guardian/")
    ects = models.IntegerField()
    # student = models.ForeignKey

    def __str__(self):
        return self.name


# class PickUp(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
