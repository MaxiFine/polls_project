from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):

    username = models.CharField('Username', max_length=20, unique=True)
    email = models.EmailField('Email Address', unique=True)

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email']  

    def __str__(self):
        return self.username
    
