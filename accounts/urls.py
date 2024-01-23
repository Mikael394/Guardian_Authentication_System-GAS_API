from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers

# router = routers.DefaultRouter()
# router.register("guardian", ReactView)
router = routers.DefaultRouter()
router.register("guardians", GuardianView)
router.register("staff", StaffViewSet)
router.register("verify", Verify)
router.register("courses/", TestView)
router.register("logs", LogView)
guardian_router = routers.NestedDefaultRouter(router, "guardians", lookup="guardian")
guardian_router.register("logs", LogView, basename="guardian-log")

urlpatterns = [
    # path("login/<name>", login, name="login"),
    # path("capture/", capture_data, name="capture_data"),
    # path("authorize/", authorize, name="authorize"),
    # path("students/", students_list, name="students"),
    # path("courses/", include(router.urls)),
    # path("", include(.urls)),
    path("", include(guardian_router.urls)),
    path("", include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
