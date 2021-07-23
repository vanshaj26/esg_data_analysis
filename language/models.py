from django.db import models
from django.utils.timezone import now

# Create your models here.

class language(models.Model):

    language_name = models.CharField(max_length=50, unique=True)
    language_code = models.CharField(max_length=5, unique=True)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.language_name)