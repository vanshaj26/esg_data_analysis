from rest_framework import generics, views
from .serializers import cates_serializer, question_serializer, cates_mapp_serializer, ques_map_serializer, related_question # framework_serializer, category_serializer, question_serializer, sub_category_serializer, mappling_Serializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response 
from rest_framework import serializers, status, mixins, viewsets
from .models import cates, question_model, cates_mapping, ques_cat_mapping   # framework, category, , sub_category, ques_cat_mapping
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404


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



class fetch_complete_paper(mixins.ListModelMixin,      # ?frame=hello&cat=hello2&sub_cat=20
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

        mapp_id = cates_mapping.objects.filter(framework=frame).filter(category=cat).filter(sub_category=sub_cat)
        if len(mapp_id)!=0:
            return mapp_id[0]
        else:
            mapp_id = cates_mapping.objects.create(framework=frame,
                                                    category=cat,
                                                    sub_category=sub_cat)
            return mapp_id



    def create(self, request, *args, **kwargs):
        frame = cat = sub_cat = None
        frame=request.GET.get('frame')
        cat=request.GET.get('cat')
        sub_cat=request.GET.get('sub_cat')
        print(frame)
        print(cat)
        print(sub_cat)

        
        print(request.data)

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




        # print(queryset)
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)



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