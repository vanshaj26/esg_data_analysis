from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from .models import Tenant , TenantClass
import re
# from datetime import datetime, timezone
from django.utils import timezone



class Tenant_serializer(serializers.ModelSerializer):

    class Meta:

        model = Tenant

        fields = [
            'id',
            "organisation_name",
            'org_logo',
            'website_url',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]



    def create(self, validated_data):

        org_1 = (validated_data['organisation_name'].upper())
        org_1 = re.sub(' +', ' ',org_1)
        org_name = Tenant.objects.filter(organisation_name=org_1)
        if len(org_name) == 0:
            validated_data['organisation_name'] = org_1
            return Tenant.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Organisation name exist and Must Be unique")


    def update(self, instance, validated_data):
        org_1 = validated_data['organisation_name'].upper()
        org_1 = re.sub(' +', ' ',org_1)
        org_name = Tenant.objects.filter(organisation_name=org_1)
        print(org_name)

        if len(org_name) == 0 :
            print("0")
            instance.organisation_name = org_1
            instance.website_url = validated_data['website_url']
            if 'org_logo' in validated_data:
                instance.org_logo = validated_data['org_logo']
            instance.updated_on = timezone.now()
            instance.save()
            return instance

        elif len(org_name) == 1 :
            if org_name[0].id == instance.id:
                instance.organisation_name = org_1
                instance.website_url = validated_data['website_url']
                if 'org_logo' in validated_data:
                    instance.org_logo = validated_data['org_logo']
                instance.updated_on = timezone.now()
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("Organisation name exist and Must Be unique")



class Tenant_user_serializer(serializers.ModelSerializer):

    class Meta:

        model = Tenant

        fields = [
            'id',
            "organisation_name",
            "organisation_name",
            'org_logo'
            ]



class tenant_user(serializers.ModelSerializer):

    class Meta:

        model = get_user_model()

        fields = [
            "email",
            'f_name',
            'l_name',
            'tenant'
            ]
