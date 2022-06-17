
from typing import Type
from django.db import models,IntegrityError,transaction
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from django.conf import settings


from django.utils import timezone

import jwt
from datetime import datetime,timedelta,timezone

from wallet.models import Transaction,Wallet, Transfer 


#am going to use this as my custom model

class UserManager(BaseUserManager):
    use_in_migrations: True
    def create_user(self, username,phone,email,password=None):
        if not email:
            raise ValueError(_('You must provide an email address'))
        if username is None:
            raise  TypeError('Users must have a username.')
        email = self.normalize_email(email)
        user = self.model(username,email=self.normalize_email(email),phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,phone,email,password):
        if password is None:
            raise TypeError('superusers must have a password.')
        user=self.create_user(username,email,phone,password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

       



#===now the actual user model
class User(AbstractBaseUser,PermissionsMixin):
    COUNTRIES = (
        ('UGA','Uganda'),
        ('KEN', 'Kenya'),
        ('NIG', 'Nigeria'),
    )
    username= models.CharField(max_length=10, default='Bbosa')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format \
        +256706626855. Up to 10 digits allowed.")
    phone = models.CharField('Phone', validators=[phone_regex], max_length=17,null=False,unique=True,db_index=True)
    email =  models.EmailField(max_length=32,unique=True,db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.utcnow())
    updated_at = models.DateTimeField(default=datetime.utcnow())
    country = models.CharField(max_length=10,choices=COUNTRIES,default="UGA")
    password = models.CharField(max_length=8)
    

    objects=UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','username']
    #idont think i need the password

   

    def __str__(self):
        return self.email

    class Meta:
        unique_together = ("phone","email")
    
    @property 
    def token(self):
        """
            allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()


    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id':self.pk,
            'exp':int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorith='HS256')
        return token.decode('utf-8')

    
    def has_perm(self,perm,obj=None):
        """Does the user have aspecific permission"""
        return True 

    def has_module_perms(self, app_label: str) -> bool:
        """Does the user have permissions to view the app `app_label`"""
        return True



#===just  use a function to automate adding country code to the phone=====
def add_code_phone(country,phone):
    return {
        'UGA':'+256'+phone[1:],
        'KEN':'+254'+phone[1:],
        'NIG':'+234'+phone[1:]
    }[country]
#task is at hand is to handle the issue of country code when user selects country 
#i shud concatenate the country at the start



def phone_number(sender,instance,*args,**kwargs):
    if instance.country:
        instance.phone = add_code_phone(instance.country,instance.phone)
        #finally saving it to the database
        # return {
        #     'UGA':'256'+instance.phone,
        #     'KEN':'254'+instance.phone,
        #     'NIG':'234'+instance.phone
        # }[instance.country]


@transaction.atomic 
@receiver(post_save, sender=User)
def create_wallet(sender, instance,created, **kwargs):
    """
        create awallet for every new user
    """
    if created:
        print("testing creating the wallet")
        try:
            transfer = Transfer(
                transferred_to=instance, transferred_from=instance,transfer_reason='Initial Transfer',amount=0
            )
            transfer.save()
            print("saving transfer")
            transaction = Transaction(amount=transfer.amount)
            transfer.save()
            print("saving transaction")
            wallet=Wallet(balance=0, owner=instance, latest_transaction=transaction)
            print("saving wallet..")
            wallet.save()
        except IntegrityError as e:
            raise e



        