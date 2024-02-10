from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ["username","phone_number","user_photo"]
    # list_editable = ["is_active"]
    # ordering = []
    # list_per_page = 10
    search_fields = ["username__istartswith"]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name","last_name","present"]
    # list_editable = ["present"]
    # ordering = []
    # list_per_page = 10
    search_fields = ["first_name__istartswith","last_name__istartswith"]
    @admin.display(ordering="is_present")
    def present(self,student):
        if student.is_present:
            return "Present"
        else:
            return "Absent"
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["student","guardian","staff","date_time","action"]
    # list_editable = ["present"]
    # ordering = []
    # list_per_page = 10
    search_fields = ["student__istartswith","guardian__istartswith","staff__istartswith","date_time"]

admin.site.register(User)
admin.site.register(Staff)
