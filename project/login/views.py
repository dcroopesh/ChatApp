from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationSerializer,LoginSerializer,ResetSerializer
from .models import Registration
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
#from rest_framework. import IsAuthenticate
from django.contrib.auth.models import User
import json
import rest_framework_jwt as jwt
from urlshortening.models import get_short_url, invalidate_url, get_full_url
#from django_short_url.views import get_surl
#from django.contrib.auth import set_password
#django.contrib.auth.models.User 
from django.core.validators import validate_email
#from django.contrib.auth import authenticate
from project.settings import EMAIL_HOST_USER , BASE_URL
from .token import generate_token,decode_token  

class RegistrationApiView(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RegistrationSerializer

    def get(self,request):
        return render(request,'login/register.html',{'title' : "Register"})

    def post(self, request):
        
        username = request.data['username']
        email = request.data['email']
        password = request.data['password1']
        password2 = request.data['password2']
        #url = "http://localhost:8000/activate/"
        valid_data = RegistrationSerializer(data = {'username':username,'email':email,'password':password,'password2':password2})
        
        if valid_data.is_valid():
            # print(valid_data['email'])
            add_user = User.objects.create_user(username=username, email=email, password=password,is_active=False)
            add_user.save()
            data = {'username': username ,'password' : password}
            token = generate_token(data)
            short_url = get_short_url(token)
            url = BASE_URL + "activate/" + short_url.short_id
            send_mail('Account activation',url,EMAIL_HOST_USER,[email],fail_silently=False)
        else:
            return Response(valid_data.errors,status = 400)
        
        return redirect('user_login')

class LoginAPIview(APIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = LoginSerializer


    def get(self, request):
        # print(request.data)
        return render(request, 'login/login.html',{'title' : "Login"})

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        # print(request.data)
        user = authenticate(username=username, password= password)
        if user != None:
            return Response({user.username : "Successfully logged in"},status = 200)    
        else:
            return Response({"Invalid credentials !!"},status = 400) 
                    
class Activate(APIView):
    def get(self,request,url):
        full_url = get_full_url(url)
        data = decode_token(full_url.url)
        user = User.objects.get(username = data['username'])
        if not user.is_active:
            user.is_active = True
            user.save()
        else:
            return Response({data['username'] : "User is already Activated"},status = 200)
        return Response({data['username'] : "Activated"},status = 200)

class ResetLinkView(APIView):
    
    def get(self,request):
        return render(request,'login/link.html')

    def post(self,request):
        email = request.data['email']
        url = "http://localhost:8000/reset/password/"
        user = User.objects.get(email = email)
        data = {'username': user.username ,'email' : email }
        token = generate_token(data)
        short_url = get_short_url(token)
        url += short_url.short_id
        send_mail('Reset passowrd link',url,EMAIL_HOST_USER,[email],fail_silently=False)
        
        return Response({email : "Check your email "},status = 200)

class ResetPasswordView(APIView):
    
    def get(self,request,url):
        full_url = get_full_url(url)
        data = decode_token(full_url.url)
        #print(data)
        user = User.objects.get(username = data['username'],email = data['email'])
        if user:
            return render(request,'login/reset_password.html',{'title' : "Password Reset","user_email" : user.email})
        else:
            return Response({"Invalid email " : "USer doesn't exists"} , status = 400)
    
    def post(self,request,url):
        
        email = request.data['email']
        password = request.data['password1']
        password2 = request.data['password2']
        user = User.objects.get(email = email)
        valid_data = ResetSerializer(data = {'password':password , 'password2':password2})
       
        if valid_data.is_valid():
            user.set_password(password)
            user.save()
            return Response({'password' : "Updated"},status = 200)
        else:       
            return Response(valid_data.errors,status = 400)