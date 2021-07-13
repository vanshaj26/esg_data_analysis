from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import framework_view, category_view, question_view, specific_category, category_wise_view


router = DefaultRouter()
router.register(r'framework', framework_view),
router.register(r'category', category_view),
router.register(r'question', question_view),
router.register(r'spec_cate', specific_category),
router.register(r'cate_ques', category_wise_view),

# router.register(r'add_access',add_access)

urlpatterns = [
    path("api/", include(router.urls)),
]