from rest_framework import generics
from .serializers import upload_doc, access_tenant
from django.contrib.auth import get_user_model
from rest_framework.response import Response 
from rest_framework import serializers, status, mixins, viewsets
from .models import documents, private_doc_access
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404


class upload_doc (viewsets.ModelViewSet):

    serializer_class = upload_doc
    queryset = documents.objects.all()

class add_access (mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    serializer_class = access_tenant
    queryset = private_doc_access.objects.all()
