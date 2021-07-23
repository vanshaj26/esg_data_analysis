from django.contrib import admin
from .models import cates, cates_mapping, question_model, ques_cat_mapping # framework, category, question_model, sub_category, ques_cat_mapping
# Register your models here.

admin.site.register(cates)
admin.site.register(cates_mapping)
admin.site.register(question_model)
admin.site.register(ques_cat_mapping)
# admin.site.register(framework)
# admin.site.register(category)
# admin.site.register(sub_category)
# admin.site.register(question_model)
# admin.site.register(ques_cat_mapping)