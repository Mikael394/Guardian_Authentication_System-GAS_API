from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers
from .views import (
    AttendanceView,
    AttendanceViewNested,
    ContactBookView,
    ContactBookViewNested,
    GradeAndSectionView,
    HomeRoomTeacherView,
    ParentView,
    StudentView,
    GuardianView,
    AuthenticatorView,
    StudentViewReg,
    UserView,
    Verify,
    LogView,
    StudentViewNested,
    GuardianViewNested,
    LogViewNested,
    VideoListCreate,
)

router = routers.DefaultRouter()
router.register("students", StudentView, basename="students")
router.register("guardians", GuardianView, basename="guardians")
router.register("grades", GradeAndSectionView, basename="grades")
router.register("authenticator", AuthenticatorView)
router.register("attendance", AttendanceView)
router.register("student_reg", StudentViewReg)
router.register("verify", Verify)
router.register("logs", LogView)
router.register("parents", ParentView)
router.register("video", VideoListCreate)
router.register("hrts", HomeRoomTeacherView)
router.register("sections", GradeAndSectionView)
router.register("contact_book", ContactBookView)
router.register("user", UserView)
# router.register("students", StudentView)

guardian_router = routers.NestedDefaultRouter(router, "guardians", lookup="guardian")
guardian_router.register("students", StudentViewNested, basename="guardian-student")

grade_router = routers.NestedDefaultRouter(router, "grades", lookup="grade")
grade_router.register("attendances", AttendanceViewNested, basename="grade-attendance")

student_router = routers.NestedDefaultRouter(router, "students", lookup="student")
student_router.register("guardians", GuardianViewNested, basename="student-guardian")
student_router.register(
    "contactbooks", ContactBookViewNested, basename="student-contactbook"
)
# student_router.register("attendances", AttendanceViewNested, basename="student-attendance")
student_router.register("logs", LogViewNested, basename="student-log")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(student_router.urls)),
    path("", include(guardian_router.urls)),
    path("", include(grade_router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
