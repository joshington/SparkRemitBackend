import re
import socket

from uuid import uuid4

from rave_python import Rave
from wallet.models import Payment, Transaction

# RAVE_SECRET_KEY = "FLWSECK-9d454c7836b407aa3a4585c0eb9103c5-X"
# RAVE_PUBLIC_KEY = 'FLWPUBK-cb38d8ffef2a9521711f24187beb95aa-X'


secret_key="FLWSECK_TEST-e0cbc06d58428b734f5caa144be6cbb7-X"
public_key="FLWPUBK_TEST-0848d18635e3b1ef8e9a17c0473b1801-X"
DEFAULT_PAYMENT_EMAIL = 'bbosalj@gmail.com'
from dotenv import load_dotenv
import os

load_dotenv()

# RAVE_SECRET_KEY = os.environ["secret_key"]
# RAVE_PUBLIC_KEY = os.environ["public_key"]
# DEFAULT_PAYMENT_EMAIL = os.environ["default_email"]


rave = Rave(public_key,secret_key, usingEnv = False)


#getting the ip address currently
def get_ip_addess():
    host_name =socket.gethostname()
    IP_Addr = socket.gethostbyname(host_name)
    return IP_Addr


def make_momo_payment(amount,phonenumber,user,email=DEFAULT_PAYMENT_EMAIL):
    IP=get_ip_addess()
    txRef = str(uuid4())
    payment=Payment(transaction_ref=txRef,amount=amount,user=user)
    payment.save()
    transaction = Transaction(amount=amount,payment_id=payment)
    transaction.save()

    payload = {
        'amount':amount,
        'email':email,
        'phonenumber':phonenumber,
        "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
        'IP':IP
    }
    return rave.UGMobile.charge(payload)

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
