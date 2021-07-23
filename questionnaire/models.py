from django.db import models
import os
import random
from django.utils.timezone import now
from language.models import language

# Create your models here.



class cates(models.Model):

    type_choice = [

        ('framework','framework'),
        ('category','category'),
        ('sub_category', 'sub_category')

    ]


    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=12 ,choices=type_choice, default = 'category' )
    language = models.ForeignKey(language, related_name='lang_cate', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.name)


# GRI ---> Social , Env
# social --> sub 1, sub 2
# Env -- sub 1, sub 2

# GRI --> Social --> Sub 1
# GRI --> Social --> Sub 2
# GRI --> Env --> Sub 1 
# GRI --> Env --> Sub 2 

# GRI --> Social , Env
# GRI - social --> Sub 1, Sub 2

# cates_mapping ( tab name)
# framework, category, subcategory

# select distinct framework from cates_mapping
# select distinct category from cates_mapping where framwork = selected framework
# select distinct sub categoty from cates_mapping where framework = selected framework and category = selected category

class cates_mapping(models.Model):

    framework = models.ForeignKey(cates, related_name='frame1' , on_delete=models.CASCADE) # 1 GRI  2 GRI 3 Sasb
    category = models.ForeignKey(cates, related_name='catego1' , on_delete=models.CASCADE) # social Social Envi
    sub_category = models.ForeignKey(cates, related_name='sub_cate1' , on_delete=models.CASCADE) # subcat 1 Subcate-2 Subcat 1
    language = models.ForeignKey(language, related_name='lang_map1' ,on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.id)

    

class question_model(models.Model):

    question = models.TextField(unique=True) # 1 what is your name
    description = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    language = models.ForeignKey(language, related_name='lang_ques' ,on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.id)





class ques_cat_mapping(models.Model):

    ques_map =  models.ForeignKey(question_model, related_name='mapped_ques' , on_delete=models.CASCADE) # 1    3
    cate = models.ForeignKey(cates_mapping, related_name='sub_cate' , on_delete=models.CASCADE) #          1    1
    language = models.ForeignKey(language, related_name='lang_map' ,on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now)
    updated_on = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.id)







# class ques_cat_mapping(models.Model):

#     ques_map =  models.ForeignKey(question_model, related_name='mapped_ques' , on_delete=models.CASCADE)
#     framework = models.ForeignKey(cates, related_name='frame' , on_delete=models.CASCADE)
#     category = models.ForeignKey(cates, related_name='catego' , on_delete=models.CASCADE)
#     sub_category = models.ForeignKey(cates, related_name='sub_cate' , on_delete=models.CASCADE)
#     language = models.ForeignKey(language, related_name='lang_map' ,on_delete=models.CASCADE)
#     created_on = models.DateTimeField(default=now)
#     updated_on = models.DateTimeField(default=now)

#     def __str__(self):
#         return str(self.id)




# class framework(models.Model):

#     framework_name = models.CharField(max_length=100, unique=True)
#     framework_description = models.TextField(null=True, blank=True)
#     language = models.ForeignKey(language, related_name='lang_frame' ,on_delete=models.CASCADE)
#     created_on = models.DateTimeField(default=now)
#     updated_on = models.DateTimeField(default=now)

#     def __str__(self):
#         return str(self.framework_name)


# class category(models.Model):

#     category_name = models.CharField(max_length=100)
#     # category_framework = models.ForeignKey(framework, related_name='frame' , on_delete=models.CASCADE, null=True, blank=True)
#     language = models.ForeignKey(language, related_name='lang_cate' ,on_delete=models.CASCADE)
#     created_on = models.DateTimeField(default=now)
#     updated_on = models.DateTimeField(default=now)

#     def __str__(self):
#         return str(self.category_name)


# class sub_category(models.Model):

#     sub_category_name = models.CharField(max_length=100)
#     # subcategory = models.ForeignKey(category, related_name='sub_category' , on_delete=models.CASCADE, null=True, blank=True)
#     language = models.ForeignKey(language, related_name='lang_sub' ,on_delete=models.CASCADE)
#     created_on = models.DateTimeField(default=now)
#     updated_on = models.DateTimeField(default=now)

#     def __str__(self):
#         return str(self.sub_category_name)



# class question_model(models.Model):

#     question = models.TextField(unique=True)
#     description = models.TextField(null=True, blank=True)
#     unit = models.CharField(max_length=100, null=True, blank=True)
#     language = models.ForeignKey(language, related_name='lang_ques' ,on_delete=models.CASCADE)
#     created_on = models.DateTimeField(default=now)
#     updated_on = models.DateTimeField(default=now)

#     def __str__(self):
#         return str(self.id)


# class ques_cat_mapping(models.Model):

#     ques_map =  models.ForeignKey(question_model, related_name='mapped_ques' , on_delete=models.CASCADE)
#     framework = models.ForeignKey(framework, related_name='frame' , on_delete=models.CASCADE)
#     category = models.ForeignKey(category, related_name='catego' , on_delete=models.CASCADE)
#     sub_category = models.ForeignKey(sub_category, related_name='sub_cate' , on_delete=models.CASCADE)
#     language = models.ForeignKey(language, related_name='lang_map' ,on_delete=models.CASCADE)
#     created_on = models.DateTimeField(default=now)
#     updated_on = models.DateTimeField(default=now)

#     def __str__(self):
#         return str(self.id)
