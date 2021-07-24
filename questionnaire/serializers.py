from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from .models import cates, question_model, cates_mapping, ques_cat_mapping, stack_ques   # framework, category, question_model, sub_category, ques_cat_mapping
import re 
from django.utils import timezone



class cates_serializer(serializers.ModelSerializer):       # (cates) framework , category , sub category serializer

    class Meta:

        model = cates

        fields = [
            'id',
            'name',
            'description',
            'type',
            'language',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]

        
    def create(self, validated_data):

        nam = (validated_data['name'].upper())
        nam = re.sub(' +', ' ',nam)
        cate = (validated_data['type'])
        name_1 = cates.objects.filter(name=nam).filter(type=cate)
        if len(name_1) == 0:
            validated_data['name'] = nam
            return cates.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Framework name exist and Must Be unique")


    def update(self, instance, validated_data):
        nam = validated_data['name'].upper()
        nam = re.sub(' +', ' ',nam)
        name_1 = cates.objects.filter(name=nam)
        print(name_1)

        if len(name_1) == 0 :
            instance.name = nam
            instance.description = validated_data['description']
            instance.updated_on = timezone.now()
            instance.language = validated_data['language']
            instance.save()
            return instance

        elif len(name_1) == 1 :
            if name_1[0].id == instance.id:
                instance.name = nam
                instance.description = validated_data['description']
                instance.language = validated_data['language']
                instance.updated_on = timezone.now()
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("Exist and Must Be unique")




class cates_mapp_serializer(serializers.ModelSerializer):    # frame cat sub cat mapping

    class Meta:

        model = cates_mapping

        fields = [
            'id',
            'framework',
            'category',
            'sub_category',
            'language',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]

        
    def create(self, validated_data):

        frame = (validated_data['framework'])
        cate = (validated_data['category'])
        sub_cate = (validated_data['sub_category'])
        lang = validated_data['language']
        mapp = cates_mapping.objects.filter(framework=frame).filter(category=cate).filter(sub_category=sub_cate).filter(language=lang)
        if len(mapp) == 0:
            return cates_mapping.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Mapping exist")


    def update(self, instance, validated_data):
        frame = (validated_data['framework'])
        cate = (validated_data['category'])
        sub_cate = (validated_data['sub_category'])
        lang = validated_data['language']
        mapp = cates_mapping.objects.filter(framework=frame).filter(category=cate).filter(sub_category=sub_cate).filter(language=lang)
        
        if len(mapp) == 0 :
            instance.framework = frame
            instance.category = cate
            instance.sub_category = sub_cate
            instance.language = lang
            instance.updated_on = timezone.now()
            instance.save()
            return instance

        elif len(mapp) == 1 :
            if mapp[0].id == instance.id:
                instance.framework = frame
                instance.category = cate
                instance.sub_category = sub_cate
                instance.language = lang
                instance.updated_on = timezone.now()
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("Mapping exist")







class question_serializer(serializers.ModelSerializer): # question model serializer

    class Meta:

        model = question_model

        fields = [
            'id',
            'question',
            'description',
            'unit',
            'language',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]

        
    def create(self, validated_data):

        ques = validated_data['question']
        ques = re.sub(' +', ' ',ques)
        lang = validated_data['language']
        print(lang)
        ques_1 = question_model.objects.filter(question__iexact=ques).filter(language=lang)
        if len(ques_1) == 0:
            validated_data['question'] = ques
            print("okk")
            return question_model.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Question name exist and Must Be unique")


    def update(self, instance, validated_data):
        ques = validated_data['question']
        ques = re.sub(' +', ' ',ques)
        lang = validated_data['language']
        ques_1 = question_model.objects.filter(question__iexact=ques).filter(language=lang)
        print(ques_1)

        if len(ques_1) == 0 :
            print("0")
            instance.question = ques
            instance.description = validated_data['description']
            instance.unit = validated_data['unit']
            instance.updated_on = timezone.now()
            instance.language = validated_data['language']
            instance.save()
            return instance

        elif len(ques_1) == 1 :
            if ques_1[0].id == instance.id:
                instance.question = ques
                instance.description = validated_data['description']
                instance.unit = validated_data['unit']
                instance.updated_on = timezone.now()
                instance.language = validated_data['language']
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("Question name exist and Must Be unique")



class ques_map_serializer(serializers.ModelSerializer):    # question map sub category

    class Meta:

        model = ques_cat_mapping

        fields = [
            'id',
            'ques_map',
            'cate',
            'language',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]

        
    def create(self, validated_data):

        ques = validated_data['ques_map']
        catego = validated_data['cate']
        lang = validated_data['language']
        mapp = ques_cat_mapping.objects.filter(ques_map=ques).filter(cate=catego).filter(language=lang)
        if len(mapp) == 0:
            return ques_cat_mapping.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Question exist in this subcategory")


    def update(self, instance, validated_data):
        ques = validated_data['ques_map']
        catego = validated_data['cate']
        lang = validated_data['language']
        mapp = ques_cat_mapping.objects.filter(ques_map=ques).filter(cate=catego).filter(language=lang)        

        if len(mapp) == 0 :
            instance.ques_map = ques
            instance.cate = catego
            instance.updated_on = timezone.now()
            instance.language = lang
            instance.save()
            return instance

        elif len(mapp) == 1 :
            if mapp[0].id == instance.id:
                instance.ques_map = ques
                instance.cate = catego
                instance.updated_on = timezone.now()
                instance.language = lang
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("Question exist in this subcategory")




# class cate_list_serializer(serializers.ModelSerializer):        # get category list serializer
#     category = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='name'
#      )

#     class Meta:

#         model = cates_mapping

#         fields = [
#             'id',
#             'framework',
#             'category',
#             # 'sub_category',
#             # 'language',
#             # 'created_on',
#             # 'updated_on'
#             ]    


class ques_ser(serializers.ModelSerializer): # question model serializer

    class Meta:

        model = question_model

        fields = [
            'id',
            'question',
            'description',
            'unit'
            ]


class related_question(serializers.ModelSerializer):   # show related question values
    ques_map = ques_ser(read_only=True)

    class Meta:
        model = ques_cat_mapping
        fields = [
            'id',
            'ques_map',
            ]







class stack_question_serializer(serializers.ModelSerializer): # question model serializer

    class Meta:

        model = stack_ques

        fields = [
            'id',
            'question',
            'cate',
            'type',
            'language',
            'created_on',
            'updated_on'
            ]

        read_only_fields = [
            'created_on',
            'updated_on'
        ]

        
    def create(self, validated_data):

        ques = validated_data['question']
        ques = re.sub(' +', ' ',ques)
        cate = validated_data['cate']
        type = validated_data['type']
        lang = validated_data['language']
        print(lang)
        ques_1 = stack_ques.objects.filter(question__iexact=ques).filter(cate=cate).filter(language=lang)
        if len(ques_1) == 0:
            validated_data['question'] = ques
            print("okk")
            return stack_ques.objects.create(**validated_data)
        else:
             raise serializers.ValidationError("Question name exist and Must Be unique")


    def update(self, instance, validated_data):
        ques = validated_data['question']
        ques = re.sub(' +', ' ',ques)
        cate = validated_data['cate']
        type = validated_data['type']
        lang = validated_data['language']
        ques_1 = stack_ques.objects.filter(question__iexact=ques).filter(cate=cate).filter(language=lang)
        print(ques_1)

        if len(ques_1) == 0 :
            print("0")
            instance.question = ques
            instance.type = validated_data['type']
            instance.cate = validated_data['cate']
            instance.updated_on = timezone.now()
            instance.language = validated_data['language']
            instance.save()
            return instance

        elif len(ques_1) == 1 :
            if ques_1[0].id == instance.id:
                instance.question = ques
                instance.type = validated_data['type']
                instance.cate = validated_data['cate']
                instance.updated_on = timezone.now()
                instance.language = validated_data['language']
                instance.save()
                return instance

            else:
                raise serializers.ValidationError("Question name exist and Must Be unique")









# class framework_serializer(serializers.ModelSerializer):

#     class Meta:

#         model = framework

#         fields = [
#             'id',
#             'framework_name',
#             'framework_description',
#             'language',
#             'created_on',
#             'updated_on'
#             ]

#         read_only_fields = [
#             'created_on',
#             'updated_on'
#         ]


#     def create(self, validated_data):

#         frame = (validated_data['framework_name'].upper())
#         frame = re.sub(' +', ' ',frame)
#         frame_name = framework.objects.filter(framework_name=frame)
#         if len(frame_name) == 0:
#             validated_data['framework_name'] = frame
#             return framework.objects.create(**validated_data)
#         else:
#              raise serializers.ValidationError("Framework name exist and Must Be unique")


#     def update(self, instance, validated_data):
#         frame = validated_data['framework_name'].upper()
#         frame = re.sub(' +', ' ',frame)
#         frame_name = framework.objects.filter(framework_name=frame)
#         print(frame_name)

#         if len(frame_name) == 0 :
#             print("0")
#             instance.framework_name = frame
#             instance.framework_description = validated_data['framework_description']
#             instance.updated_on = timezone.now()
#             instance.language = validated_data['language']
#             instance.save()
#             return instance

#         elif len(frame_name) == 1 :
#             if frame_name[0].id == instance.id:
#                 instance.framework_name = frame
#                 instance.framework_description = validated_data['framework_description']
#                 instance.language = validated_data['language']
#                 instance.updated_on = timezone.now()
#                 instance.save()
#                 return instance

#             else:
#                 raise serializers.ValidationError("Framework name exist and Must Be unique")





# class category_serializer(serializers.ModelSerializer):

#     class Meta:

#         model = category

#         fields = [
#             'id',
#             "category_name",
#             'language',
#             'created_on',
#             'updated_on'
#             ]

#         read_only_fields = [
#             'created_on',
#             'updated_on'
#         ]


#     def create(self, validated_data):

#         catego = (validated_data['category_name'].upper())
#         catego = re.sub(' +', ' ',catego)
#         catego_name = category.objects.filter(category_name=catego)
#         if len(catego_name) == 0:
#             validated_data['category_name'] = catego
#             return category.objects.create(**validated_data)
#         else:
#              raise serializers.ValidationError("This category exist in this framework")


#     def update(self, instance, validated_data):
#         catego = validated_data['category_name'].upper()
#         catego = re.sub(' +', ' ',catego)
#         catego_name = category.objects.filter(category_name=catego))
#         print(catego_name)

#         if len(catego_name) == 0 :
#             print("0")
#             instance.category_name = catego
#             instance.language = validated_data['language']
#             instance.updated_on = timezone.now()
#             instance.save()
#             return instance

#         elif len(catego_name) == 1 :
#             if catego_name[0].id == instance.id:
#                 instance.category_name = catego
#                 instance.category_framework = validated_data['category_framework']
#                 instance.language = validated_data['language']
#                 instance.updated_on = timezone.now()
#                 instance.save()
#                 return instance

#             else:
#                 raise serializers.ValidationError("This category exist in this framework")







# class sub_category_serializer(serializers.ModelSerializer):

#     class Meta:

#         model = sub_category

#         fields = [
#             'id',
#             'sub_category_name',
#             'subcategory',
#             'language',
#             'created_on',
#             'updated_on'
#             ]

#         read_only_fields = [
#             'created_on',
#             'updated_on'
#         ]


#     def create(self, validated_data):

#         catego = (validated_data['sub_category_name'].upper())
#         catego = re.sub(' +', ' ',catego)
#         catego_name = sub_category.objects.filter(sub_category_name=catego).filter(subcategory=validated_data['subcategory'])
#         if len(catego_name) == 0:
#             validated_data['sub_category_name'] = catego
#             return sub_category.objects.create(**validated_data)
#         else:
#              raise serializers.ValidationError("This category exist in this framework")


#     def update(self, instance, validated_data):
#         catego = validated_data['sub_category_name'].upper()
#         catego = re.sub(' +', ' ',catego)
#         catego_name = category.objects.filter(sub_category_name=catego).filter(subcategory=validated_data['subcategory'])
#         print(catego_name)

#         if len(catego_name) == 0 :
#             print("0")
#             instance.category_name = catego
#             instance.subcategory = validated_data['subcategory']
#             instance.language = validated_data['language']
#             instance.updated_on = timezone.now()
#             instance.save()
#             return instance

#         elif len(catego_name) == 1 :
#             if catego_name[0].id == instance.id:
#                 instance.category_name = catego
#                 instance.subcategory = validated_data['subcategory']
#                 instance.language = validated_data['language']
#                 instance.updated_on = timezone.now()
#                 instance.save()
#                 return instance

#             else:
#                 raise serializers.ValidationError("This category exist in this framework")






# class question_serializer(serializers.ModelSerializer):

#     class Meta:

#         model = question_model

#         fields = [
#             'id',
#             "question",
#             "description",
#             "unit",
#             'language',
#             'created_on',
#             'updated_on'
#             ]

#         read_only_fields = [
#             'created_on',
#             'updated_on'
#         ]



# class mappling_Serializer(serializers.ModelSerializer):

#     class Meta:

#         model = ques_cat_mapping

#         fields = [
#             'id',
#             "ques_map",
#             'sub_category',
#             'language',
#             'created_on',
#             'updated_on'
#             ]

#         read_only_fields = [
#             'created_on',
#             'updated_on'
#         ]


