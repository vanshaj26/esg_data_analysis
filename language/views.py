from rest_framework import generics, views
from .serializers import language_serializer
# from django.contrib.auth import get_user_model
from rest_framework.response import Response 
from rest_framework import serializers, status, mixins, viewsets
from .models import language
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404


class language_view (viewsets.ModelViewSet):

    serializer_class = language_serializer
    queryset = language.objects.all()