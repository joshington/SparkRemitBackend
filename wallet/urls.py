from django.urls import  re_path
from .views import*

app_name='wallet'

urlpatterns = [
    re_path('balance/', GetBalance.as_view()),
    re_path('top-up/', TopUp.as_view()),
    re_path('withdraw/', Withdraw.as_view()),
    re_path('last7/<str:email>/',Last7Transactions.as_view()),
    re_path('test_transfer/',WalletMobileTransfer.as_view()),
    re_path('wallet_wallet/',TestWalletTransfer.as_view()),
    re_path('wallet_details/',UserWalletDetails.as_view()),
]
