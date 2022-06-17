from django.urls import path
from .views import*

app_name='wallet'

urlpatterns = [
    path('balance/', GetBalance.as_view()),
    path('top-up/', TopUp.as_view()),
    path('withdraw/', Withdraw.as_view()),
    path('last7/<str:email>/',Last7Transactions.as_view()),
    path('test_transfer/',WalletMobileTransfer.as_view()),
    path('wallet_wallet/',TestWalletTransfer.as_view())
]
