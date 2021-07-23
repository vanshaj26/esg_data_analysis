from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import cates_view, question_view, cates_mapping_view, ques_cate_map_view, cates_mapping_list_view, fetch_framework, fetch_category, fetch_sub_category, fetch_complete_paper, map_existing_ques  #framework_view, category_view, sub_category_view, question_view, specific_category, category_wise_view, maping_view


router = DefaultRouter()
router.register(r'cate', cates_view),  # add framework, category , sub category
router.register(r'framework', fetch_framework),  # fetch only framewok
router.register(r'category', fetch_category),    # fetch only category
router.register(r'sub_category', fetch_sub_category),  # fetch only sub category
router.register(r'ques', question_view),
router.register(r'cate_map', cates_mapping_view),
router.register(r'ques_cat_map', ques_cate_map_view),
router.register(r'show_cate_map', cates_mapping_list_view),
router.register(r'fetch_paper', fetch_complete_paper),
router.register(r'map_ques', map_existing_ques),
# router.register(r'framework', framework_view),
# router.register(r'category', category_view),
# router.register(r'sub_category', sub_category_view),
# router.register(r'question', question_view),
# router.register(r'spec_cate', specific_category),
# # router.register(r'spec_sub_cate', sub_category_wise_view),
# router.register(r'cate_ques', category_wise_view),
# router.register(r'mapping', maping_view),

# router.register(r'add_access',add_access)

urlpatterns = [
    path("api/", include(router.urls)),
]