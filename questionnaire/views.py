from rest_framework import generics, views
from .serializers import framework_serializer, category_serializer, question_serializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response 
from rest_framework import serializers, status, mixins, viewsets
from .models import framework, category, question_model
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404


class framework_view (viewsets.ModelViewSet):

    serializer_class = framework_serializer
    queryset = framework.objects.all()
    


class category_view (viewsets.ModelViewSet):

    serializer_class = category_serializer
    queryset = category.objects.all()


class question_view (viewsets.ModelViewSet):

    serializer_class = question_serializer
    queryset = question_model.objects.all()




class specific_category (mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet ):
    
    serializer_class = framework_serializer
    queryset = framework.objects.all()


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
        category_list = category.objects.filter(category_framework=instance.id)
        # user_list = Tenant.objects.filter(tenant_1=instance)

        serializer = category_serializer(category_list, many=True)
        print(category_list)
        return Response(serializer.data)



class category_wise_view (mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet ):
    
    serializer_class = category_serializer
    queryset = category.objects.all()


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
        ques_list = question_model.objects.filter(category=instance.id)
        # user_list = Tenant.objects.filter(tenant_1=instance)

        serializer = question_serializer(ques_list, many=True)
        print(ques_list)
        return Response(serializer.data)
