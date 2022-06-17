#from dataclasses import fields
from rest_framework import serializers
from .models import User

from django.contrib.auth import authenticate

#registering the new user
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    class Meta:
        model = User 
        fields=['email','username','phone','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    #hashing the password
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ['email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    # def validate(self,attrs):
    #     #take username and password requet
    #     email = attrs.get('email')
    #     password = attrs.get('password')

    #     if email and password:
    #         user = authenticate(request=self.context.get('request'),
    #                             email=email, password=password)
    #         if not user:
    #             # If we don't have a regular user, raise a ValidationError
    #             msg = 'Access denied: wrong username or password.'
    #             raise serializers.ValidationError(msg, code='authorization')
    #     else:
    #         msg = 'Both "username" and "password" are required.'
    #         raise serializers.ValidationError(msg, code='authorization')
    #     attrs['user'] = user
    #     return attrs