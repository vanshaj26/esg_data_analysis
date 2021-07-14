from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from .models import framework, category, question_model
import re 
from django.utils import timezone



class framework_serializer(serializers.ModelSerializer):

    class Meta:

        model = framework

        fields = [
            'id',
            "framework_name",
            'framework_description',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]


    def create(self, validated_data):

        frame = (validated_data['framework_name'].upper())
        frame = re.sub(' +', ' ',frame)
        frame_name = framework.objects.filter(framework_name=frame)
        if len(frame_name) == 0:
            validated_data['framework_name'] = frame
            return framework.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Framework name exist and Must Be unique")


    def update(self, instance, validated_data):
        frame = validated_data['framework_name'].upper()
        frame = re.sub(' +', ' ',frame)
        frame_name = framework.objects.filter(framework_name=frame)
        print(frame_name)

        if len(frame_name) == 0 :
            print("0")
            instance.framework_name = frame
            instance.framework_description = validated_data['framework_description']
            instance.updated_on = timezone.now()
            instance.save()
            return instance

        elif len(frame_name) == 1 :
            if frame_name[0].id == instance.id:
                instance.framework_name = frame
                instance.framework_description = validated_data['framework_description']
                instance.updated_on = timezone.now()
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("Framework name exist and Must Be unique")





class category_serializer(serializers.ModelSerializer):

    class Meta:

        model = category

        fields = [
            'id',
            "category_name",
            'category_framework',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]


    def create(self, validated_data):

        catego = (validated_data['category_name'].upper())
        catego = re.sub(' +', ' ',catego)
        catego_name = category.objects.filter(category_name=catego).filter(category_framework=validated_data['category_framework'])
        if len(catego_name) == 0:
            validated_data['category_name'] = catego
            return category.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("This category exist in this framework")


    def update(self, instance, validated_data):
        catego = validated_data['category_name'].upper()
        catego = re.sub(' +', ' ',catego)
        catego_name = category.objects.filter(category_name=catego).filter(category_framework=validated_data['category_framework'])
        print(catego_name)

        if len(catego_name) == 0 :
            print("0")
            instance.category_name = catego
            instance.category_framework = validated_data['category_framework']
            instance.updated_on = timezone.now()
            instance.save()
            return instance

        elif len(catego_name) == 1 :
            if catego_name[0].id == instance.id:
                instance.category_name = catego
                instance.category_framework = validated_data['category_framework']
                instance.updated_on = timezone.now()
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("This category exist in this framework")



class question_serializer(serializers.ModelSerializer):

    class Meta:

        model = question_model

        fields = [
            'id',
            "question",
            "description",
            "unit",
            'category',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]





