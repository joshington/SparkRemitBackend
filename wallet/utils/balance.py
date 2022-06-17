from authentication.models import User
from wallet.models import Wallet


def balance(phone,user):
    """
        get the wallet balance of a particular user
    """
    print("now picking user of the phone")
    
    print("have gotten the user")
    print(user)
    print(user.id)
    try:
        print("testiing the wallet for now")
        wallet_owner =Wallet.objects.get(owner=user)
        wallet_balance=wallet_owner.balance
        print(wallet_balance)
        return wallet_balance
    except Exception as e:
        print("cant find owner of the wallet")