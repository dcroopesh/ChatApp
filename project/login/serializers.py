from rest_framework import serializers
from rest_framework.serializers import  ValidationError
from login.models import Registration
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.validators import validate_email
import json
import re

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        model = Registration
        fields = ['username','email','password','password2']

    def validate(self,data):
       
        username_pattern = re.compile('^[a-zA-Z]+[0-9]*[a-zA-Z]*$')
        password_pattern = re.compile('^[a-zA-Z0-9@$#%]*[@$#%]+[a-zA-Z0-9@$#%]*$')
        
        if data['username'] == "" or data['email'] == "" or data['password'] == "" or data['password2'] == "":
            raise serializers.ValidationError("Some fields are missing !!!")
        
        elif username_pattern.match(data['username']) is None:
            raise serializers.ValidationError({'Username':'UserName should begin with character ,Not interger !!!'})
       
        elif data['password'] != data['password2']:
            raise serializers.ValidationError('Both passwords are not matched !!!')

        elif password_pattern.match(data['password']) is None or len(data['password']) < 8: 
            raise serializers.ValidationError('password should have atleast one digit and one special character and length should be minimum 8')
 
        elif User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email is already Registered !!!")
        
        elif User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError("UserName is already Registered !!!")
        
        return data

        
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class ResetSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        model = Registration
        fields = ['password','password2']

    def validate(self,data):

        password_pattern = re.compile('^[a-zA-Z0-9@$#%]*[@$#%]+[a-zA-Z0-9@$#%]*$')

        if data['password'] != data['password2']:
            raise serializers.ValidationError('Both passwords are not matched !!!')

        elif password_pattern.match(data['password']) is None or len(data['password']) < 8 :
            raise serializers.ValidationError('password should have atleast one digit and one special character and length should be minimum 8')

        return data