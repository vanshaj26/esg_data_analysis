from rest_framework import generics
from .serializers import register_user, ChangePasswordSerializer, reset_pass_serializer, resetPasswordSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response 
from rest_framework import serializers, status, mixins, viewsets

from rest_framework.permissions import IsAuthenticated
# from datetime import datetime
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from datetime import datetime, timedelta
from django.core.mail import send_mail
from esg_data_analysis.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER
from django.template import loader
# from Candidate.models import personal_detail
from django.shortcuts import get_object_or_404
from django.utils import timezone
# from datetime import datetime

# import 

# Create your views here.


class add_user (viewsets.ModelViewSet
                ):

    serializer_class = register_user
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny,]



# class resend_verify_email (generics.GenericAPIView):

#     permission_classes = [IsAuthenticated,]


#     def get(self,request):

#         token = Token.objects.get_or_create(user=request.user)
#         token = Token.objects.get(user=request.user)
#         user = get_user_model().objects.get(email=request.user.email)

#         if request.user.email_verified == True:
#             return Response ({"Value":"Already Verified", "message":"Email already verified"}, status=status.HTTP_400_BAD_REQUEST)

#         current_site = get_current_site(request)
#         relativelink = reverse('email-verify')
#         absurl = 'http://'+str(current_site)+relativelink+"?token="+str(token)

#         email_body = 'Hi '+user.f_name+" "+user.l_name+" Use this link to verify your email \n" + absurl
#         # data = {'name':user.f_name, 'url':absurl, 'email_body' : email_body, 'to_email':[user.email], 'email_subject':'Verify Your Email'  }
#         print(email_body)

# #         # Util.send_email(data)

#         send_mail(
#             subject="Verify Your Email",
#             message="Verify Email",
#             from_email = EMAIL_HOST_USER,
#             recipient_list=[user.email],
#             fail_silently = False,
#             html_message = loader.render_to_string(
#                 'Email_Verify.html',
#                 {
#                     'url':absurl,
#                     'f_name':user.f_name
#                 }
#             )

#         )
#         exp_time = datetime.now() + timedelta(hours=1)
        
#         if email_link_expire.objects.filter(user_id=user).exists():
#             e_link = email_link_expire.objects.get(user_id=user)
#             e_link.expire_by = exp_time
#             e_link.save()

#         else:
#             email_link_expire.objects.create(user_id = user, expire_by = exp_time)

#         # headers = self.get_success_headers(serializer.data)
#         return Response({"Value":"Success", "message":"Email Sent"}, status=status.HTTP_201_CREATED)








# class VerifyEmail(generics.GenericAPIView):

#     permission_classes = [AllowAny,]


#     def get(self,request):
#         token = request.GET.get('token')
        
#         try:
#             print(token)
#             print("Hello")
#             token_user = Token.objects.get(key=token)
#             print(token_user)
#             print("ok")
#             # print(token_user.user.F_name)

#             user_1 = get_user_model().objects.get(email=token_user.user)
#             print(user_1)
        
#             if email_link_expire.objects.filter(user_id = user_1).exists():
#                 email_exp_id = email_link_expire.objects.get(user_id = user_1)
#                 print("expire by")
#                 print(email_exp_id.expire_by)
#                 print("current time")
#                 print(datetime.now())
#                 if email_exp_id.expire_by > datetime.now():
                    
#                     print(email_exp_id.expire_by)
#                     print(datetime.now())
            
#                     user_1.email_verified = True
#                     user_1.save()
#                     print("ok 2")
#                     user_1.auth_token.delete()
#                     email_exp_id.delete()
#                     return Response ({"Value":"OK", "message":"Verified"}, status=status.HTTP_200_OK)


#                 else:
#                     email_exp_id.delete()
#                     return Response ({"Value":"Expired", "message":"Time Expired"}, status=status.HTTP_200_OK)



#         except:
#             return Response ({"Value":"Expired", "message":"Link Expired"}, status=status.HTTP_200_OK)



class Login(APIView):

    # {
    #     "email":"vanshaj.garg26@gmail.com",
    #     "password":"qwerty"
    # }


    permission_classes = [AllowAny,]


    def post(self, request, *args, **kwargs):
        

        email = request.data.get("email")
        password = request.data.get("password")
        print(email)
        print(password)
        
        if email is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.is_authenticated:
            return Response("You are Already Logged In", status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)

        user_mod = get_user_model()
        user_obj = user_mod.objects.get(email=user)
        print("okkkkkkkkkkk")
        print(str(timezone.now()))
        user_obj.last_login = timezone.now()
        user_obj.save()
        user_det = {}
        token, _ = Token.objects.get_or_create(user=user)

        user_det['token'] = token.key
        user_det['f_Name'] = user_obj.f_name
        user_det['l_Name'] = user_obj.l_name
        user_det['tenant'] = str(user_obj.tenant)
        user_det['f_login'] = user_obj.f_login
        user_det['user_type'] = user_obj.user_type
        print("okkkkkkk2222222")
        return Response(user_det,
                        status=status.HTTP_200_OK)




class Logout(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        # simply delete the token to force a login
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("Not Logged In" ,status=status.HTTP_400_BAD_REQUEST)




class Self_detail(APIView):

    permission_classes = [IsAuthenticated]
    # serializers_classes = []

    def get(self, request, format = None):

        user_obj = get_user_model().objects.get(email=self.request.user)

        user_dict = {"email":user_obj.email, 
                            "f_name":user_obj.f_name, 
                            "l_name":user_obj.l_name,
                            "f_login":user_obj.f_login,
                            # "email_verified":user_obj.email_verified, 
                            "user_type":user_obj.user_type
                            } 
        return Response (user_dict, status=status.HTTP_200_OK)









class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            print(serializer.data.get("old_password"))
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            print(serializer.data.get("new_password"))
            # set_password also hashes the password that the user will get
            if serializer.data.get("new_password") != serializer.data.get("confirm_password"):
                return Response({"password": ["New Password And Confirm Password Does Not Match"]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# class reset_password_email (generics.CreateAPIView):

#     serializer_class = reset_pass_serializer
#     queryset = get_user_model().objects.all()
#     permission_classes = [AllowAny,]

#     def post(self, request, *args, **kwargs):

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
        
#         # self.perform_create(serializer)
#         validated_data = serializer.validated_data
#         # validated_data.pop("confirm_password")


#         print(validated_data)
        
#         # if get_user_model().objects.filter(email=validated_data['email']).exists():
#         email_obj = get_object_or_404(get_user_model() ,email=validated_data['email'])
            
#         token = Token.objects.get_or_create(user=email_obj)
#         token = Token.objects.get(user=email_obj)
            

#         # token = Token.objects.get(user=user)

#         current_site = get_current_site(request)
#         relativelink = reverse('forget-password')
#         absurl = 'http://'+str(current_site)+relativelink+"?token="+str(token)

#         email_body = 'Hi '+email_obj.f_name+" "+email_obj.l_name+" Use this link to reset your password \n" + absurl
#         data = {'name':email_obj.f_name, 'url':absurl, 'email_body' : email_body, 'to_email':[email_obj.email], 'email_subject':'Reset Password'  }


#         # Util.send_email(data)

#         send_mail(
#             subject="Reset Password",
#             message="Reset Password",
#             from_email = EMAIL_HOST_USER,
#             recipient_list=[email_obj.email],
#             fail_silently = False,
#             html_message = loader.render_to_string(
#                 'Email_Verify.html',
#                 {
#                     'url':absurl,
#                     'f_name':email_obj.f_name
#                 }
#             )

#         )

#         exp_time = datetime.now() + timedelta(hours=1)

#         if email_link_expire.objects.filter(user_id=email_obj).exists():
#             e_link = email_link_expire.objects.get(user_id=email_obj)
#             e_link.expire_by = exp_time
#             e_link.save()

#         else:
#             email_link_expire.objects.create(user_id = email_obj, expire_by = exp_time)




#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)






# class ResetPasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = resetPasswordSerializer
#     permission_classes = [AllowAny]


#     def update(self, request, *args, **kwargs):

#         token = request.GET.get('token')

#         # print(token)
#         print("Hello")
#         token_user = Token.objects.get(key=token)
#         print(token_user)
#         print("ok")
#         # print(token_user.user.F_name)

#         user_1 = get_user_model().objects.get(email=token_user.user)
#         print(user_1)
#         try:
                
#             if email_link_expire.objects.filter(user_id = user_1).exists():
#                 email_exp_id = email_link_expire.objects.get(user_id = user_1)
#                 print("expire by")
#                 print(email_exp_id.expire_by)
#                 print("current time")
#                 print(datetime.now())

#                 if email_exp_id.expire_by > datetime.now():

#                     serializer = self.get_serializer(data=request.data)

#                     if serializer.is_valid():
                
#                         # set_password also hashes the password that the user will get
#                         if serializer.data.get("new_password") != serializer.data.get("confirm_password"):
#                             return Response({"password": ["New Password And Confirm Password Does Not Match"]}, status=status.HTTP_400_BAD_REQUEST)
#                         user_1.set_password(serializer.data.get("new_password"))
#                         user_1.save()
#                         response = {
#                             'status': 'success',
#                             'code': status.HTTP_200_OK,
#                             'message': 'Password updated successfully'
#                         }

#                         return Response(response)

#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

#         except:
#             return Response ({"Value":"Expired", "message":"Link Expired"}, status=status.HTTP_200_OK)



