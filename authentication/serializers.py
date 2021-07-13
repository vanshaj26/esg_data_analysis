from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

import random
import string

from django.core.mail import send_mail
from esg_data_analysis.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER
from django.template import loader

# from rest_framework.serializers import Serializer



class ChangePasswordSerializer(serializers.Serializer):
    
    model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(style={'input_type':'password'}, required=True)
    new_password = serializers.CharField(style={'input_type':'password'}, required=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, required=True)



class reset_pass_serializer(serializers.Serializer):
    
    model = get_user_model()

    """
    Serializer for reset password endpoint.
    """
    email = serializers.EmailField(required=True)



class resetPasswordSerializer(serializers.Serializer):
    
    model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    
    new_password = serializers.CharField(style={'input_type':'password'}, required=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, required=True)





class register_user(serializers.ModelSerializer):

    # confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True, required = True)


    # def validate(self, data):

    #     email = data.get('email')   
        # if email
        # password = data.get('password')
        # confirm_password = data.get('confirm_password')
        # if password != confirm_password:
            # raise serializers.ValidationError ("Password Not Match")
        # print("matched")

        # return super(register_user, self).validate(data)



    class Meta:

        model = get_user_model()

        fields = [
            "id",
            "email",
            # 'password',
            # 'confirm_password',
            'f_name',
            'l_name',
            'tenant'
            ]

        # extra_kwargs = {'password': {'write_only': True, 'min_length': 6 , 'required':True}}

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        print("Random string of length", length, "is:", result_str)
        return result_str
   

   
    def create(self, validated_data):
        
        if get_user_model().objects.filter(email=(validated_data['email'])):
            raise serializers.ValidationError("Email exists")

        user_email = validated_data['email']
        user_data = get_user_model()(
            email=validated_data['email'],
            f_name=validated_data['f_name'],
            l_name=validated_data['l_name'],
            tenant = validated_data['tenant'],
            # email_verified = True
        )

        passw = self.get_random_string(8)
        user_data.set_password(passw)
        user_data.save()

        # send_mail(
        #     subject="Welcome TO BM Hiring",
        #     message="Your Username "+str(user_email)+"\n"+"Your first time password is "+str(passw),
        #     from_email = EMAIL_HOST_USER,
        #     recipient_list=[user_email],
        #     fail_silently = False,
        #     # html_message = loader.render_to_string(
        #     #     'Email_Verify.html',
        #     #     {
        #     #         'url':absurl,
        #     #         'f_name':user.f_name
        #     #     }
        #     # )

        # )

        return user_data



class UpdateFirstPasswordSerializer(serializers.Serializer):
    
    model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    
    new_password = serializers.CharField(style={'input_type':'password'}, required=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, required=True)