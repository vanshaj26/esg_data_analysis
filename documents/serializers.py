from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from .models import documents, private_doc_access
import re 
from datetime import datetime


class upload_doc(serializers.ModelSerializer):

    class Meta:

        model = documents

        fields = [
            'id',
            "document_name",
            'document_description',
            'document',
            'doc_type',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]


    def create(self, validated_data):

        documents_name_1 = (validated_data['document_name'].upper())
        doc_1 = re.sub(' +', ' ',documents_name_1)
        doc_name = documents.objects.filter(document_name=doc_1)
        if len(doc_name) == 0:
            validated_data['document_name'] = doc_1
            return documents.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Document name exist and Must Be unique")


    def update(self, instance, validated_data):
        doc_1 = validated_data['document_name'].upper()
        doc_1 = re.sub(' +', ' ',doc_1)
        doc_name = documents.objects.filter(document_name=doc_1)
        print(doc_name)

        if len(doc_name) == 0 :
            print("0")
            instance.document_name = doc_1
            instance.document_description = validated_data['document_description']
            if 'document' in validated_data:
                instance.document = validated_data['document']
            instance.doc_type = validated_data['doc_type']
            instance.updated_on = datetime.now()
            instance.save()
            return instance

        elif len(doc_name) == 1 :

            if doc_name[0].id == instance.id:
                print("ok")
                instance.document_name = doc_1
                instance.document_description = validated_data['document_description']
                if 'document' in validated_data:
                    instance.document = validated_data['document']
                instance.doc_type = validated_data['doc_type']
                instance.updated_on = datetime.now()
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("Document name exist and Must Be unique")



   
class access_tenant(serializers.ModelSerializer):

    class Meta:

        model = private_doc_access

        fields = [
            'id',
            'doc',
            'access_tenant',
            'created_on',
            'updated_on'
        ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]



    def create(self, validated_data):

        has_access = private_doc_access.objects.filter(doc=validated_data['doc']).filter(access_tenant=validated_data['access_tenant'])
        if len(has_access) == 0:
            return private_doc_access.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Organisation have already access to this file")
