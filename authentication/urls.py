from django.urls import path,include
from .views import*

app_name='authentication'

urlpatterns = [
    path('register',RegisterView.as_view(), name='register'),
    path('login',LoginView.as_view(), name='login'),
]
