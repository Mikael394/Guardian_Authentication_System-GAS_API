
from django.urls import path, include
from .views import ContactBookView, ContactBookViewNested, GradeAndSectionView, HomeRoomTeacherView, ParentView, StudentView,GuardianView,StaffView,Verify,LogView,StudentViewNested,GuardianViewNested,LogViewNested, VideoListCreate, getNotes
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = routers.DefaultRouter()

router.register("students", StudentView, basename="students")
router.register("guardians", GuardianView, basename="guardians")
router.register("staff", StaffView)
router.register("verify", Verify)
router.register("logs", LogView)
router.register("parents", ParentView)
router.register("video", VideoListCreate)
router.register("hrts", HomeRoomTeacherView)
router.register("sections", GradeAndSectionView)
router.register("contact_book", ContactBookView)
# router.register("students", StudentView)

guardian_router = routers.NestedDefaultRouter(router, "guardians", lookup="guardian")
guardian_router.register("students", StudentViewNested, basename="guardian-student")

student_router = routers.NestedDefaultRouter(router, "students", lookup="student")
student_router.register("guardians", GuardianViewNested, basename="student-guardian")
student_router.register("contactbooks", ContactBookViewNested, basename="student-contactbook")

student_router.register("logs", LogViewNested, basename="student-log")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(student_router.urls)),
    path("", include(guardian_router.urls)),
    path('notes', getNotes),
    # path('api/', getRoutes),
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
