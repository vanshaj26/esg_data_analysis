from django.db import models
from django.utils import timezone
import random
import os
# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1,999999999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    print("Hello Upload")
    return "org_logo/{new_filename}/{final_filename}".format(
                new_filename=new_filename,
                final_filename=final_filename
                )


class Tenant(models.Model):
    organisation_name = models.CharField(max_length=100)
    website_url = models.CharField(max_length=100, null=True, blank=True)
    org_logo = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.organisation_name)


class TenantClass(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True