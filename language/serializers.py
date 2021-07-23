from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from .models import language
import re 
from django.utils import timezone



class language_serializer(serializers.ModelSerializer):

    class Meta:

        model = language

        fields = [
            'id',
           'language_name',
           'language_code',
           'created_on',
           'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]