from django.contrib import admin
from .models import Attendance, ContactBook, GradeAndSection, Guardian, HomeRoomTeacher,Student,Log,User,Authenticator,Parent, Video
# Register your models here.
@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ["username","phone_number","user_photo_1"]
    # list_editable = ["is_active"]
    # ordering = []
    # list_per_page = 10
    search_fields = ["username__istartswith"]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name","last_name"]
    # list_editable = ["present"]
    # ordering = []
    # list_per_page = 10
    search_fields = ["first_name__istartswith","last_name__istartswith"]
    
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["student","guardian","authenticator","date_time","action"]
    # list_editable = ["present"]
    # ordering = []
    # list_per_page = 10
    search_fields = ["student__istartswith","guardian__istartswith","authenticator__istartswith","date_time"]

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["students","date","grade","status"]
    # list_editable = ["present"]
    # ordering = []
    # list_per_page = 10
    search_fields = ["students__first_name__istartswith","date__istartswith","grade__grade__istartswith"]


admin.site.register(User)
admin.site.register(Authenticator)
admin.site.register(Parent)
admin.site.register(GradeAndSection)
admin.site.register(HomeRoomTeacher)
admin.site.register(ContactBook)
admin.site.register(Video)

