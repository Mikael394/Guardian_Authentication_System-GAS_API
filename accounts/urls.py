from django.urls import path, include
from .views import *
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

urlpatterns = [
    path("", include(router.urls)),
    path("", include(student_router.urls)),
    path("", include(guardian_router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     # path("login/<name>", login, name="login"),
#     # path("capture/", capture_data, name="capture_data"),
#     # path("authorize/", authorize, name="authorize"),
#     # path("students/", students_list, name="students"),
#     # path("courses/", include(router.urls)),
#     # path("", include(.urls)),
#     path("", include(guardian_router.urls)),
#     path("", include(router.urls)),
# ]
