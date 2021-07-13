from django.db import models
import os
import random
from django.utils.timezone import now

# Create your models here.


class framework(models.Model):

    framework_name = models.CharField(max_length=100, unique=True)
    framework_description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.framework_name)


class category(models.Model):

    category_name = models.CharField(max_length=100)
    category_framework = models.ForeignKey(framework, related_name='frame' , on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.category_name)


class question_model(models.Model):

    question = models.TextField()
    category = models.ForeignKey(category, related_name='cate' , on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.id)