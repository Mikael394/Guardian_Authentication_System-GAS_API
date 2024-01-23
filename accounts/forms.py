from django import forms
from .models import *


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "user_photo"]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "date_of_birth", "class_name"]


class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = "__all__"
