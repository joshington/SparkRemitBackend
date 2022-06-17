from authentication.models import User 
from wallet.models import Payment, Transaction,Wallet


from .balance import balance as get_balance


def top_up(phone,amount):
    """
        Add money to users' wallet
    """
    user=User.objects.get(phone=phone)
    balance=get_balance(phone)

    payment=Payment(amount=amount,user=user,status='PENDING')
    payment.save()
    transaction = Transaction(amount=amount,payment_id=payment)
    transaction.save()

    wallet=Wallet(balance=balance+amount, owner=user, latest_transaction=transaction)
    wallet.save()
    return wallet