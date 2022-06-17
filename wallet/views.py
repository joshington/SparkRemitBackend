from django.shortcuts import render
from rest_framework import generics, status,views
from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response

from rest_framework import authentication,permissions

from django.db import models
import requests
import json,base64 #we want to decode the token


import json ,re
from uuid import UUID
from django.db import transaction


from .serializers import*
from .models import Payment
from .utils.balance import balance as get_balance
from .utils.rave import make_momo_payment
from .utils.top_up import top_up
from .utils.withdraw import withdraw

from authentication.models import User

from rave_python import Rave


#importing ent variables
import environ
# Initialise environment variables
from dotenv import load_dotenv
import os

load_dotenv()


RAVE_SECRET_KEY = os.environ["secret_key"]
RAVE_PUBLIC_KEY = os.environ["public_key"]
DEFAULT_PAYMENT_EMAIL = os.environ["default_email"]

secret_key="FLWSECK_TEST-e0cbc06d58428b734f5caa144be6cbb7-X"
public_key="FLWPUBK_TEST-0848d18635e3b1ef8e9a17c0473b1801-X"
MerchantID=5799821


rave = Rave(public_key, secret_key, usingEnv=False)

# rave = Rave(RAVE_PUBLIC_KEY, RAVE_SECRET_KEY, usingEnv = False)


#====flutterwave part only============
def handle_successful_payment(data):
    transaction_ref = data['txRef']
    payment=Payment.objects.get(transaction_ref=transaction_ref)

    if payment.category == Payment.Categories.TOP_UP:
        top_up(payment.user.phone,payment.amount)
    payment.status = Payment.Statuses.COMPLETE
    payment.save()

def key_exists(key,dict,label):
    if not key in dict:
        raise Exception("'{}' must exist in '{}'".format(key,label))


def required_fields(dict, required, label):
    [key_exists(i,dict,label) for i in required]



class GetBalance(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class=GetBalanceSerializer

    @transaction.atomic
    def get(self, request):
        phone=request.data.get('phone',False)

        user_target = User.objects.filter(phone__iexact=phone).first()
        if user_target:
            try:
                balance = get_balance(user_target.phone,user_target)
                print("passed this step")
                return Response({'status':True,'balance':balance}, status=status.HTTP_200_OK)
            except Exception as e:
                string_exception = str(e)
                return Response({'error':string_exception}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status':False,'detail':'Balance not returned'},status=status.HTTP_400_BAD_REQUEST)

        


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,UUID):
            #if obj is uuid we simpley return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self,obj)

#====view to handle choice of apackage


class TopUp(APIView):
    """
        essence is to topup on the wallet
    """
    serializer_class = TopUpSerializer

    @transaction.atomic
    def post(self,request,*args, **kwargs):
        phone=request.data.get('phone',False)
        amount=request.data.get('amount',False)
        user = User.objects.filter(phone__iexact=phone).first()
        if user:
            try:
                make_momo_payment(amount=amount,phonenumber=phone,user=user)
                return Response({
                    'status':True,
                    'detail':'Top up initiated'
                })
            except Exception as e:
                print(e)
                return Response({
                    'status':False,
                    'detail':'Top up Failed'
                })
        else:
            return Response({'status':False,'detail':'User not authenticated'})
        
#finding======all the required the transactions from the wallet 
class Last7Transactions(APIView):
    def get(self, request):
        #===have to fist check that user is authenticated
        # request = self.context.get("request")
        # if request and hasattr(request, "user"):
        user=self.request.user
        print(user.id)   
        all_payments = Payment.objects.filter(category='TOP_UP')
        #===since its a list its time to iterate
        #use enumerate to return 
        days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        payment_array = [(days_of_week[payment.paid_at.weekday()],payment.amount) for payment in all_payments]

        #now after getting the payment array
        return Response({'status':True,'last7transactions':payment_array},status=status.HTTP_200_OK)




#=====this is for the 
class TransPerMonth(APIView):
    def get(self,request):
        """
            target of endpoint is to return transactions per month 
        """
        #all_payments=
        pass

class Withdraw(APIView):
    serializer_class = WithdrawSerializer
    
    def post(self, request):
        phone = request.data.get('phone_number',False)
        amount=request.data.get('amount',False)
        user=User.objects.filter(phone=phone)
        
        print(user)
        if user is not None:
            try:
                print("now have enetered the loop")
                print("next is to trigger the withdraw")
                print(user)
                print(user.phone)
                #getting phone first
                withdraw(user.phone, amount,user)
                print("what next after the withdraw=====")
                return Response({
                    'status':True,
                    'detail':'Amount withdrawn successfully from wallet'
                })
            except Exception as e:
                string_exception = str(e)
                return Response({
                    'status':False,
                    'detail':'Error during withdraw from wallet'
                })
        else:
            return Response({
                'status':False,
                'detail':'Phone number not registered on the platform'
            })








class WebHook(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            required_fields(request.headers, ['verify-hash'],'request headers')
            required_fields(request.data, ['txRef'], 'request body')

            hash =request.headers['verify-hash']
            pass
        except:
            pass


def format_phone_number(phone_number):
    if re.search(r"\A\+2567\d{8}\Z",phone_number):
        return phone_number[1:]
    elif re.search(r"\A07\d{8}\Z",phone_number):
        return "256" + phone_number[1:]


def transfer_money_to_phone(phone, amount,username="Unknown User"):
    details =  {
        "account_bank":"MPS",
		"account_number":format_phone_number(phone),
		"amount":amount,
        "currency":"UGX",
        "beneficiary_name":username,
        "meta":{
            "sender": "Flutterwave Developers",
            "sender_country": "UGA",
            "mobile_number": "256760810134"
        }
    }
    res = rave.Transfer.initiate(details)


#===account_number => mobile number on account with code like 233
#beneficiary name => just make this default

#===i want to test this transfer cz man its not working properly=======
#==but actually ask them to first confirm the phone number
#so ask for it
class WalletMobileTransfer(APIView):
    def post(self, request, *args, **kwargs):
        """
            task is to test the transfer endpoint on flutterwave
            256704372213
        """
       
        details = {
            "account_bank":"MPS",
            "account_number":"256706626855",
            "amount":100,
            "currency":"UGX",
            "beneficiary_name":"Bbosa",
            "meta":{
                "sender":"Flutterwave developer",
                "sender_country":"UG",
                "mobile_number":"256706626855"
            }
        }
        res=rave.Transfer.initiate(details)
        return Response(res, status=status.HTTP_200_OK)




#==testing aswell the wallet to wallet transfer,case wen user wants to send other user directly to their wallet
class TestWalletTransfer(APIView):
    def post(self,request, *args, **kwargs):
        details ={
            "account_bank": "flutterwave",
            "account_number": MerchantID,
            "amount": 500,
            "currency": "UGX",
            "debit_currency": "UGX",
            "beneficiary_name":"Bbosa",
        }
        res=rave.Transfer.initiate(details)
        return Response(res, status=status.HTTP_200_OK)


    