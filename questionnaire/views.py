from rest_framework import generics, views
from .serializers import cates_serializer, question_serializer, cates_mapp_serializer, ques_map_serializer, related_question, stack_question_serializer, Upload_class # framework_serializer, category_serializer, question_serializer, sub_category_serializer, mappling_Serializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response 
from rest_framework import serializers, status, mixins, viewsets
from .models import cates, question_model, cates_mapping, ques_cat_mapping, stack_ques, upload   # framework, category, , sub_category, ques_cat_mapping
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404
import os
import re
import pandas as pd
from pandas import Series
from django.core.files.storage import FileSystemStorage


excel_pattern = re.compile(r'^.*\.xl(sx|s|tx|t|sm)$',re.IGNORECASE)
email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class cates_view (viewsets.ModelViewSet):    # view to add framework, category, subcategory

    serializer_class = cates_serializer
    queryset = cates.objects.all()
    
class question_view (viewsets.ModelViewSet):  # to add question

    serializer_class = question_serializer
    queryset = question_model.objects.all()

class cates_mapping_view (viewsets.ModelViewSet):  # framework, category , subcategory mapping

    serializer_class = cates_mapp_serializer
    queryset = cates_mapping.objects.all()

class ques_cate_map_view (viewsets.ModelViewSet):   # question sub category mapping

    serializer_class = ques_map_serializer
    queryset = ques_cat_mapping.objects.all()


class fetch_framework (mixins.ListModelMixin,    # list all framework
                        viewsets.GenericViewSet):
    serializer_class = cates_serializer
    queryset = cates.objects.filter(type='framework')


class fetch_category (mixins.ListModelMixin,         # list all category
                        viewsets.GenericViewSet):
    serializer_class = cates_serializer
    queryset = cates.objects.filter(type='category')


class fetch_sub_category (mixins.ListModelMixin,   # list all sub category
                        viewsets.GenericViewSet):
    serializer_class = cates_serializer
    queryset = cates.objects.filter(type='sub_category')


class stack_question (viewsets.ModelViewSet):
    serializer_class = stack_question_serializer
    queryset = stack_ques.objects.all()

class cates_mapping_list_view (mixins.RetrieveModelMixin,   # show framework and corrosponding sub category
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):

    serializer_class = cates_serializer
    # queryset = cates_mapping.objects.order_by().distinct('framework')
    queryset = cates.objects.filter(type='framework')

    def list(self, request, *args, **kwargs):
        # serializer = Tenant_user_serializer(request)
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        category_list = cates_mapping.objects.filter(framework=instance).order_by().distinct('category')
        # user_list = Tenant.objects.filter(tenant_1=instance)
        serializer = cates_mapp_serializer(category_list, many=True)
        print(category_list)
        return Response(serializer.data)



class fetch_complete_paper(mixins.ListModelMixin,      # ?frame=1&cat=3&sub_cat=5
                    viewsets.GenericViewSet):

    serializer_class = cates_serializer
    queryset = cates.objects.filter()

    def list(self, request, *args, **kwargs):
        frame = cat = sub_cat = None
        frame=request.GET.get('frame')
        cat=request.GET.get('cat')
        sub_cat=request.GET.get('sub_cat')
        print(frame)
        print(cat)
        print(sub_cat)

        if (frame == None and cat == None and sub_cat == None):  # return all framework
            queryset = cates.objects.filter(type = 'framework')
            print(queryset)
            serializer = cates_serializer(queryset, many=True)
            return Response(serializer.data)



        if (frame !=None and cat==None and sub_cat==None):      # return categories
            queryset = cates_mapping.objects.filter(framework=frame).order_by().values('category').distinct() #.distinct('category')
            print(queryset)
            if len(queryset)==0:
                return Response ("No Category exist", status=status.HTTP_404_NOT_FOUND)
            lis_2 = []
            for i in queryset:
                print(i)
                print(i.get("category"))
                catego = cates.objects.get(id = i.get("category"))
                print(catego)
                print(catego.name)
                print(catego.type)
                dic_2 = {}
                dic_2['id'] = catego.id
                dic_2['name'] = catego.name
                lis_2.append(dic_2)

            # serializer = cate_list_serializer(queryset, many=True)
            print(lis_2)
            return Response(lis_2, status=status.HTTP_200_OK)


        if (frame !=None and cat!=None and sub_cat==None):      # return sub categories
            queryset = cates_mapping.objects.filter(framework=frame).filter(category=cat).order_by().values('sub_category').distinct() #.distinct('category')
            print(queryset)
            lis_2 = []
            for i in queryset:
                print(i)
                print(i.get("sub_category"))
                sub_catego = cates.objects.get(id = i.get("sub_category"))
                print(sub_catego)
                print(sub_catego.name)
                print(sub_catego.type)
                dic_2 = {}
                dic_2['id'] = sub_catego.id
                dic_2['name'] = sub_catego.name
                lis_2.append(dic_2)

            # serializer = cate_list_serializer(queryset, many=True)
            print(lis_2)
            return Response(lis_2, status=status.HTTP_200_OK)

        if (frame !=None and cat!=None and sub_cat!=None):      # return question
            mapp_id = cates_mapping.objects.filter(framework=frame).filter(category=cat).filter(sub_category=sub_cat) #.distinct('category')
            # print(queryset)
            print(mapp_id)
            if len(mapp_id)==0:
                return Response ("No question exist", status=status.HTTP_404_NOT_FOUND)
            queryset = ques_cat_mapping.objects.filter(cate=mapp_id[0])
            print(queryset)
            serializer = related_question(queryset, many=True)
            return Response(serializer.data)



class map_existing_ques(mixins.CreateModelMixin,   # map existing question to sub category    # ?frame=hello&cat=hello2&sub_cat=20
                    viewsets.GenericViewSet):

    serializer_class = ques_map_serializer
    queryset = ques_cat_mapping.objects.all()

    def find_map(slef, request):
        frame=request.GET.get('frame')
        cat=request.GET.get('cat')
        sub_cat=request.GET.get('sub_cat')
        frame_id = cates.objects.get(id=frame)
        category_id = cates.objects.get(id=cat)
        sub_category_id = cates.objects.get(id=sub_cat)
        print(frame_id)
        print(category_id)
        print(sub_category_id)

        mapp_id = cates_mapping.objects.filter(framework=frame_id).filter(category=category_id).filter(sub_category=sub_category_id)
        print("mapp_id")
        print(mapp_id)
        if len(mapp_id)!=0:
            print(mapp_id)
            return mapp_id[0]
        else:

            mapp_id = cates_mapping.objects.create(framework=frame_id,
                                                    category=category_id,
                                                    sub_category=sub_category_id,
                                                    language=frame_id.language)
            print("else")
            print(mapp_id)
            return mapp_id



    def create(self, request, *args, **kwargs):
        frame = cat = sub_cat = None
        frame=request.GET.get('frame')
        cat=request.GET.get('cat')
        sub_cat=request.GET.get('sub_cat')
        print(frame)
        print(cat)
        print(sub_cat)
        if (frame == None or cat == None or sub_cat == None):
            return Response ({"Invalid Input"}, status=status.HTTP_406_NOT_ACCEPTABLE)


        mapp = self.find_map(request)
        print(request.data)
        print(mapp)
        ques_id = question_model.objects.filter(id=request.data['ques_map'])
        print(ques_id)
        check_exist = ques_cat_mapping.objects.filter(ques_map=ques_id[0]).filter(cate=mapp).filter(language=ques_id[0].language)
        if (len(check_exist)!=0):
            return Response({"Question already exist in sub category"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        mapping = ques_cat_mapping.objects.create(ques_map=ques_id[0], cate=mapp, language=ques_id[0].language)
        print(mapping)
        return Response({"Ok"}, status=status.HTTP_201_CREATED)








class map_new_ques(mixins.CreateModelMixin,   # map new question to sub category    # ?frame=hello&cat=hello2&sub_cat=20
                    viewsets.GenericViewSet):

    serializer_class = question_serializer
    queryset = question_model.objects.all()



    def find_map(slef, request):
        frame=request.GET.get('frame')
        cat=request.GET.get('cat')
        sub_cat=request.GET.get('sub_cat')
        frame_id = cates.objects.get(id=frame)
        category_id = cates.objects.get(id=cat)
        sub_category_id = cates.objects.get(id=sub_cat)
        print(frame_id)
        print(category_id)
        print(sub_category_id)

        mapp_id = cates_mapping.objects.filter(framework=frame_id).filter(category=category_id).filter(sub_category=sub_category_id)
        print("mapp_id")
        print(mapp_id)
        if len(mapp_id)!=0:
            print(mapp_id)
            return mapp_id[0]
        else:

            mapp_id = cates_mapping.objects.create(framework=frame_id,
                                                    category=category_id,
                                                    sub_category=sub_category_id,
                                                    language=frame_id.language)
            print("else")
            print(mapp_id)
            return mapp_id



    def create(self, request, *args, **kwargs):
        frame = cat = sub_cat = None
        frame=request.GET.get('frame')
        cat=request.GET.get('cat')
        sub_cat=request.GET.get('sub_cat')
        print(frame)
        print(cat)
        print(sub_cat)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        print(serializer.data)

        check_exist = question_model.objects.filter(question__iexact=serializer.data['question']).filter(language=serializer.data['language'])
        if (len(check_exist) != 0):
            ques_id = check_exist[0]
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            ques_id = serializer.save()
        print(ques_id)
        

        mapp = self.find_map(request)


        check_exist = ques_cat_mapping.objects.filter(ques_map=ques_id).filter(cate=mapp).filter(language=ques_id.language)
        if (len(check_exist)!=0):
            return Response({"Question already exist in sub category"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        mapping = ques_cat_mapping.objects.create(ques_map=ques_id, cate=mapp, language=ques_id.language)
        print(mapping)
        return Response({"Ok"}, status=status.HTTP_201_CREATED)







class Excel_upload_question(
                                mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    
    serializer_class = Upload_class
    queryset = upload.objects.all()
    # permission_classes = [IsAuthenticated, Is_admin]
    



    # def generate_random_password(self):
        
    #     N = 8
  
    #     res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
    #                                                       for i in range(N)) 

    #     print("The generated random string : " + str(res)) 

    #     return res



    # def change_pass_send_email(self, user_obj_list):

    #     # partial = kwargs.pop('partial', False)
    #     # instance = self.get_object()
    #     email_default = []
    #     for obj_user in user_obj_list:

    #         # user_mod = get_user_model()
    #         # if user_mod.objects.filter(Reg_id = instance).exists():
    #         # obj_user = user_mod.objects.get(Reg_id = instance)
    #         print(obj_user.Reg_id)
    #         print(obj_user.Email)
    #         password = self.generate_random_password()
    #         obj_user.set_password(password)
    #         obj_user.f_login = True
    #         if obj_user.Email is None:
    #             email_default.append(obj_user.Reg_id)
    #             continue
    #         message = "Your username is " + str(obj_user.Reg_id) + " And your Login 1st time password is " + str(password)
    #         send_mail('Your Account Has Been Created',
    #                      message , 'piet.epass@gmail.com', [obj_user.Email])

    #         obj_user.save()
    #         print("Mail Sent")
    #     return email_default
    #     # else:
    #     #     return Response("User Not Exist", status=status.HTTP_404_NOT_FOUND)




    def create(self, request, *args, **kwargs):
        print("Request data")
        print(request.data)
        serializer = self.get_serializer(data=request.data, many=False)

        if serializer.is_valid(raise_exception=True) :
            
            file_name = request.data['upload']
            serializer.save()
            print("Serializersssssssss data")
            print(serializer.data)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #.split('question')[0]
            print(BASE_DIR)
            address = os.path.join(BASE_DIR, 'media\\uploads', str(file_name))
            g = upload.objects.all()
            
            # check the type of file
                
            if excel_pattern.match(str(file_name)) :
                    data = pd.read_excel(address)
                    
                # try :

                    for i in range(data['framework'].size):
                        print(data.loc[i, 'framework'])
                        print("hello")
                        if (cates.objects.filter(type='framework').filter(name__iexact=data.loc[i, 'framework'])).exists():
                            print("framework exists")
                            framework_obj = cates.objects.filter(type='framework').filter(name__iexact=data.loc[i, 'framework'])
                            print(framework_obj)
                            framework_obj = framework_obj[0]
                        else:
                           framework_obj = cates.objects.create(name=data.loc[i, 'framework'], type='framework')
                        print(framework_obj)
                        if cates.objects.filter(type='category').filter(name__iexact=data.loc[i, 'category']).exists():
                            print("category exists")
                            category_obj = cates.objects.filter(type='category').filter(name__iexact=data.loc[i, 'category'])
                            category_obj = category_obj[0]
                        else:
                           category_obj = cates.objects.create(type='category', name=data.loc[i, 'category'])
                        print("category")
                        print(category_obj)

                        if cates.objects.filter(type='sub_category').filter(name__iexact=data.loc[i, 'sub_category']).exists():
                            print("sub_category exists")
                            sub_category_obj = cates.objects.filter(type='sub_category').filter(name__iexact=data.loc[i, 'sub_category'])
                            sub_category_obj = sub_category_obj[0]
                        else:
                           sub_category_obj = cates.objects.create(type='sub_category', name=data.loc[i, 'sub_category'])
                        print("sub_cat")
                        print(sub_category_obj)
                        if (cates_mapping.objects.filter(framework=framework_obj).filter(category=category_obj).filter(sub_category=sub_category_obj)).exists():
                            cates_mapping_obj = cates_mapping.objects.filter(framework=framework_obj).filter(category=category_obj).filter(sub_category=sub_category_obj)
                            cates_mapping_obj = cates_mapping_obj[0]
                        else:
                            cates_mapping_obj = cates_mapping.objects.create(framework=framework_obj, category=category_obj, sub_category=sub_category_obj)
                        print(cates_mapping_obj)

                        if question_model.objects.filter(question__iexact=data.loc[i, 'question']).exists():
                            ques_obj = question_model.objects.filter(question__iexact=data.loc[i, 'question'])
                            print("question exist")
                            print(ques_obj)
                            ques_obj = ques_obj[0]
                        else:
                            ques_obj = question_model.objects.create(question = data.loc[i, 'question'] , description = data.loc[i, 'description'] ,unit = data.loc[i, 'unit'])
                        print(ques_obj)
                        if ques_cat_mapping.objects.filter(ques_map=ques_obj).filter(cate=cates_mapping_obj).exists():
                            print("This mapping and question already exist")
                            print(i)
                        else:
                            mapping_obj = ques_cat_mapping.objects.create(ques_map=ques_obj, cate=cates_mapping_obj )

                    # deleting upload file
                    os.remove(address)
                    g.delete()
                    # email_default_user = self.change_pass_send_email(success_list_obj)
                    return Response({"OK"},status=status.HTTP_200_OK)

                # except :
                #     os.remove(address)
                #     g.delete()
                #     return Response("Attributes name should be like : Roll_no",status=status.HTTP_400_BAD_REQUEST)
                    
            else :
                # deleting upload file
                os.remove(address)
                g.delete()
                return Response("unsupported format only excel file is accepted.",status=status.HTTP_400_BAD_REQUEST)

        else :    
            return Response("not Valid data",status=status.HTTP_400_BAD_REQUEST)














































































        # if (frame == None or cat == None or sub_cat == None):
        #     return Response ({"Invalid Input"}, status=status.HTTP_406_NOT_ACCEPTABLE)


        # mapp = self.find_map(request)
        # print(request.data)
        # print(mapp)
        # ques_id = question_model.objects.filter(id=request.data['ques_map'])
        # print(ques_id)
        # check_exist = ques_cat_mapping.objects.filter(ques_map=ques_id[0]).filter(cate=mapp).filter(language=ques_id[0].language)
        # if (len(check_exist)!=0):
        #     return Response({"Question already exist in sub category"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # mapping = ques_cat_mapping.objects.create(ques_map=ques_id[0], cate=mapp, language=ques_id[0].language)
        # print(mapping)
        # return Response({"Ok"}, status=status.HTTP_201_CREATED)














# class framework_view (viewsets.ModelViewSet):

#     serializer_class = framework_serializer
#     queryset = framework.objects.all()
    


# class category_view (viewsets.ModelViewSet):

#     serializer_class = category_serializer
#     queryset = category.objects.all()


# class sub_category_view (viewsets.ModelViewSet):

#     serializer_class = sub_category_serializer
#     queryset = sub_category.objects.all()

# class question_view (viewsets.ModelViewSet):

#     serializer_class = question_serializer
#     queryset = question_model.objects.all()


# class maping_view (viewsets.ModelViewSet):

#     serializer_class = mappling_Serializer
#     queryset = ques_cat_mapping.objects.all()


# class specific_category (mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet ):
    
#     serializer_class = framework_serializer
#     queryset = framework.objects.all()


#     def list(self, request, *args, **kwargs):
#         # serializer = Tenant_user_serializer(request)
#         queryset = self.filter_queryset(self.get_queryset())
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         category_list = category.objects.filter(category_framework=instance.id)
#         # user_list = Tenant.objects.filter(tenant_1=instance)

#         serializer = category_serializer(category_list, many=True)
#         print(category_list)
#         return Response(serializer.data)



# class category_wise_view (mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet ):
    
#     serializer_class = category_serializer
#     queryset = category.objects.all()


#     def list(self, request, *args, **kwargs):
        
#         # serializer = Tenant_user_serializer(request)
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         sub_cate_list = sub_category.objects.filter(subcategory=instance.id)
#         # user_list = Tenant.objects.filter(tenant_1=instance)

#         serializer = sub_category_serializer(sub_cate_list, many=True)
#         print(sub_cate_list)
#         return Response(serializer.data)



# # class sub_category_wise_view (mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet ):
    
# #     serializer_class = sub_category_serializer
# #     queryset = sub_category.objects.all()


# #     def list(self, request, *args, **kwargs):
        
# #         # serializer = Tenant_user_serializer(request)
# #         queryset = self.filter_queryset(self.get_queryset())

# #         page = self.paginate_queryset(queryset)
# #         if page is not None:
# #             serializer = self.get_serializer(page, many=True)
# #             return self.get_paginated_response(serializer.data)

# #         serializer = self.get_serializer(queryset, many=True)
# #         return Response(serializer.data)


# #     def retrieve(self, request, *args, **kwargs):
# #         instance = self.get_object()
# #         ques_list = question_model.objects.filter(id=instance.id)
# #         # user_list = Tenant.objects.filter(tenant_1=instance)

# #         serializer = question_serializer(ques_list, many=True)
# #         print(ques_list)
# #         return Response(serializer.data)