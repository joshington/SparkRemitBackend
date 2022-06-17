from uuid import uuid4
import datetime
from authentication.models import User

from wallet.models import Payment, Transaction, Wallet

from .balance import balance as get_balance
from .exceptions import WalletException
from .rave import  transfer_money_to_phone

def withdraw(phone, amount,user):
    """
        move money from a users wallet to phone number
    """
    print("testing balance")
    balance = get_balance(phone,user)
    print(balance)
    print(amount)

    transaction_ref=str(uuid4())
    print(transaction_ref)
    print("transaction model")
    print("in payments model now...")
    print(user)
    #got the error the user is supposed to be an instance
    user_instance=User.objects.get(email=user)
    print(user_instance)
    payment=Payment.objects.create(
        status='PENDING',
        transaction_ref=transaction_ref,
        amount=amount,
        user=user_instance,
        category='WITHDRAW', 
    )
    print("created----")
    payment.save()
    print("testing payment now")
    print(payment.amount)
    transaction = Transaction(
        amount=amount,
        payment_id=payment
    )
    transaction.save()
    print("finished transaction")
    wallet=Wallet(
        balance=balance,owner=user_instance,latest_transaction=transaction)
    wallet.save()
    print("finished wallet")
    res=transfer_money_to_phone(phone,amount,user.name)
    print("=====after transfer=====")
    print(res)
    return res

