from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import add_user, Login, Logout, Self_detail


router = DefaultRouter()
router.register(r'register', add_user)

urlpatterns = [
    path("api/", include(router.urls)),
    path("login/", Login.as_view(), name='login'),
    path("logout/", Logout.as_view(), name='logout'),
    # path('email-verify/',VerifyEmail.as_view(), name='email-verify'),
    # path('reset-password/',VerifyEmail.as_view(), name='reset-password'),
    # path('forget-password-email/',reset_password_email.as_view(), name='reset_password-email'),
    # path('forget-password/',ResetPasswordView.as_view(), name='forget-password'),
    path('self-detail/',Self_detail.as_view(), name='self-detail'),
    # path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('api/resend_verify_email/', resend_verify_email.as_view(), name='resend_verify_email'),
]