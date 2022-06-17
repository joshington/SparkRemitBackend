from rest_framework import serializers
from authentication .models import User
from django.core.validators import RegexValidator


class WalletSerializer(serializers.Serializer):
	balance = serializers.IntegerField()
	owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	latest_transaction = serializers.UUIDField()


class TopUpSerializer(serializers.Serializer):
	phone = serializers.CharField(max_length=15)
	amount = serializers.IntegerField() 


class VerifyPinSerializer(serializers.ModelSerializer):
	class Meta:
		model = User 
		fields = ('pin_code')

class WithdrawSerializer(serializers.Serializer):
	phone_number =  serializers.IntegerField()
	amount = serializers.IntegerField()

class GetBalanceSerializer(serializers.Serializer):
	phone = serializers.CharField(max_length=15)


class CheckoutSerializer(serializers.Serializer):
    request_amount = serializers.IntegerField()

class GeneralSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields = ('email')

class WalletDetailSerializer(serializers.Serializer):
	email = serializers.EmailField()

#=====wallet==

	





