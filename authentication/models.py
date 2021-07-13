from esg_data_analysis.settings import AUTH_USER_MODEL
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                                        PermissionsMixin
from organisation.models import Tenant
import os
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MinLengthValidator
import random


# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, tenant, f_name = None, password=None, l_name = None):
        if self.model.objects.filter(email=email).exists():
            raise ValueError("Already Exist")
        user = self.model(email = self.normalize_email(email),
                            f_name = f_name,
                            l_name = l_name,
                            tenant = tenant
                            )
        user.set_password(password)
        user.save(using=self._db)
        
        return user


    def create_superuser(self, email, password=None ):
        # create database super_use/r         
        if self.model.objects.filter(email=email).exists():
            raise ValueError("Already Exist")
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)

        user.is_staff = True
        user.is_superuser = True
        user.user_type = 'admin'
        user.save(using=self._db)

        return user



# def get_filename_ext(filepath):
#     base_name = os.path.basename(filepath)
#     name, ext = os.path.splitext(base_name)
#     return name, ext

# def upload_image_path(instance, filename):
#     print(instance)
#     print(filename)
#     new_filename = random.randint(1,999999999)
#     name, ext = get_filename_ext(filename)
#     print(name)
#     final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
#     print("Hello Upload")
#     return "profile_pic/{new_filename}/{final_filename}".format(
#                 new_filename=new_filename,
#                 final_filename=final_filename
#                 )


class User(AbstractBaseUser, PermissionsMixin):
        
    # Custom user model for user authentication 

    user_type_choice = [

        ('admin','admin'),
        ('user','user'),

    ]


    # unique_id = models.CharField(max_length=255, null=False)

    email = models.EmailField(max_length=255, unique=True)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255, default="", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # email_verified = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, related_name='tenant_1' ,on_delete=models.CASCADE, null=True, blank=True)
    f_login = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    user_type = models.CharField(max_length=11 ,choices=user_type_choice, default = 'user' )

    
    class Meta:
        ordering = ['created_on', 'tenant']    


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []




# class email_link_expire(models.Model):

    # user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # expire_by = models.DateTimeField()
    # count = models.IntegerField(default=0)
    # date_time = models.DateTimeField(default=now)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)



