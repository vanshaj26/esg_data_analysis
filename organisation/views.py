from rest_framework import generics
from .serializers import Tenant_serializer, Tenant_user_serializer, tenant_user
from django.contrib.auth import get_user_model
from rest_framework.response import Response 
from rest_framework import serializers, status, mixins, viewsets
from .models import Tenant
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404


class tenant_view (viewsets.ModelViewSet):

    serializer_class = Tenant_serializer
    queryset = Tenant.objects.all()



class tenant_user_view (mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = Tenant_user_serializer
    queryset = Tenant.objects.all()

    def list(self, request, *args, **kwargs):
        
        # serializer = Tenant_user_serializer(request)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_list = get_user_model().objects.filter(tenant=instance.id)
        # user_list = Tenant.objects.filter(tenant_1=instance)

        serializer = tenant_user(user_list, many=True)
        print(user_list)
        return Response(serializer.data)
