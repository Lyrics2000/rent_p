from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.gis.db import models as md

# Create your models here.


class Agent(md.Model):
    agent_id = models.AutoField(primary_key=True,help_text="agent primary id")
    agent_name = models.CharField(max_length=30,help_text="agent name")
    mobile_number = models.CharField(max_length=10,help_text="agent phone number")
    email = models.EmailField(max_length=50,help_text="agent email")
    approved = models.BooleanField(default=False,help_text="approved")
    address = md.PointField(srid=4326,help_text="agent address")
    account_number = models.CharField(max_length=30, help_text="bank account")

    def __str__(self):
        return self.agent_name

    class Meta:
        verbose_name_plural = 'Agents'


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractUser):

    first_name =  None
    last_name = None
    username = None
    email = models.EmailField(verbose_name='email',max_length=255,unique=True)
    # phone = models.CharField(null=True,max_length=255)
    # account_type = models.CharField(max_length=255,blank=True,null=True)
    # approved =  models.BooleanField(default=False)
    # address_name = models.CharField(max_length=255,blank=True,null=True)
    # latitude =  models.CharField(max_length=100,blank=True,null=True)
    # longitude =  models.CharField(max_length=100,blank=True,null=True)
    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.email