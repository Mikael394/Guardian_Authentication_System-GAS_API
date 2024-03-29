from django.urls import path, include
from .views import StudentView,GuardianView,StaffView,Verify,LogView,StudentViewNested,GuardianViewNested,LogViewNested
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register("students", StudentView, basename="students")
router.register("guardians", GuardianView, basename="guardians")
router.register("staff", StaffView)
router.register("verify", Verify)
router.register("logs", LogView)
# router.register("students", StudentView)

guardian_router = routers.NestedDefaultRouter(router, "guardians", lookup="guardian")
guardian_router.register("students", StudentViewNested, basename="guardian-student")

student_router = routers.NestedDefaultRouter(router, "students", lookup="student")
student_router.register("guardians", GuardianViewNested, basename="student-guardian")

student_router.register("logs", LogViewNested, basename="student-log")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(student_router.urls)),
    path("", include(guardian_router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
