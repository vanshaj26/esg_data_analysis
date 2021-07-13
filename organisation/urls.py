from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import tenant_view, tenant_user_view


router = DefaultRouter()
router.register(r'tenant', tenant_view),
router.register(r'user', tenant_user_view),
# router.register(r'add_access',add_access)

urlpatterns = [
    path("api/", include(router.urls)),
]