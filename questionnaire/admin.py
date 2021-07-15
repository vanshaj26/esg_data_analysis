from django.contrib import admin
from .models import framework, category, question_model
# Register your models here.

admin.site.register(framework)
admin.site.register(category)
admin.site.register(question_model)