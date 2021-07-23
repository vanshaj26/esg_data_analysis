from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import language_view

router = DefaultRouter()
router.register(r'language', language_view),

# router.register(r'add_access',add_access)

urlpatterns = [
    path("api/", include(router.urls)),
]