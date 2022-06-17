from django.shortcuts import render
from rest_framework import generics, status,views
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .serializers import*
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .renderers import UserJSONRenderer

from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework_simplejwt.tokens import RefreshToken

import jwt, datetime
from .models import User


# Create your views here.
from .utils import Util

from django.contrib.auth import login

from django.contrib.auth import authenticate

#registering the user
class RegisterView(generics.GenericAPIView):
    serializer_class= RegisterSerializer
    def post(self, request, *args, **kwargs):
        user = request.data 
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user=User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        #the one above gets the access token
        email_body = 'Registration successful'
        data = {
            'email_body':email_body,
            'to_email':user.email,
            'email_subject':'Spark Remit Registration'
        }
        Util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)

        


#====login view coming from the tutorial
class LoginView(APIView):
    permission_classes=(AllowAny,)
    serializer_class=LoginSerializer

    def post(self, request,format=None):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email)
        #print(user)
        if user is None:
            #raise AuthenticationFailed('User not Found')
            return Response({
                'status':False,
                'detail':'Account doesnot exist'
            })
        if not user.check_password(password):
            #AuthenticationFailed('Incorrect password')
            return Response({
                'status':False,
                'detail':'Password is Incorrect'
            })

        authenticate(email=email,password=password)
        #print(user.email)

        # serializer.is_valid(raise_exception=True)
        #suser = serializer.validated_data['user']
        
        email_body = 'You are successfully logged in,\n Enjoy your experience '
        data = {
            'email_body':email_body,
            'to_email':user.email,
            'email_subject':'Spark Remit Registration'
        }
        Util.send_email(data)
        return Response({'status':True,'message':'Login successful'},status=status.HTTP_202_ACCEPTED)
        # email = request.data['email']
        # password = request.data['password']

        # user = User.objects.filter(email=email).first()
        # if user is None:
        #     raise AuthenticationFailed('User not Found')
        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect password')

        # authenticate(username=email,password=password)
        # #now jwt comes in======
        # payload = {
        #     'id':user.id,
        #     'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),#signifying keeping token for 60 minutes
        #     'iat':datetime.datetime.utcnow()
        # }
        # token =jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        # response = Response() 
        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {
        #     'jwt':token
        # }
        #thus have to allow credentials for the frontend
        
        
       

class UserView(APIView):
    def get(self,request):
        #using cookies to get the user token
        token = request.COOKIES.get('jwt')
        #gives us the cookie we want
        #and then decode it to get the user
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithm='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.get(id=payload['id']).first()
        serializer=RegisterSerializer(user)
        return Response(token)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response
