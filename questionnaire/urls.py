from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import cates_view, question_view, cates_mapping_view, ques_cate_map_view, cates_mapping_list_view, fetch_framework, fetch_category, fetch_sub_category, fetch_complete_paper, map_existing_ques, map_new_ques, stack_question, Excel_upload_question  #framework_view, category_view, sub_category_view, question_view, specific_category, category_wise_view, maping_view


router = DefaultRouter()
router.register(r'cate', cates_view),  # add framework, category , sub category
router.register(r'framework', fetch_framework),  # fetch only framewok
router.register(r'category', fetch_category),    # fetch only category
router.register(r'sub_category', fetch_sub_category),  # fetch only sub category
router.register(r'ques', question_view), # fetch all qestion
router.register(r'cate_map', cates_mapping_view),   # frame category sub cat mapping
router.register(r'ques_cat_map', ques_cate_map_view),  # ques cat mapping
router.register(r'fetch_paper', fetch_complete_paper), # fetch depandent cat, sub cat and questions
router.register(r'map_ques', map_existing_ques),
router.register(r'map_new_ques', map_new_ques),
router.register(r'stack_ques', stack_question),
router.register(r'upload_question', Excel_upload_question),


urlpatterns = [
    path("api/", include(router.urls)),
]