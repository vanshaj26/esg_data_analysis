from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import upload_doc, add_access


router = DefaultRouter()
router.register(r'upload_doc', upload_doc),
router.register(r'add_access',add_access)

urlpatterns = [
    path("api/", include(router.urls)),
]