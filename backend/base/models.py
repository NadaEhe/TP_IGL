from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   password=None
   address = models.CharField(null=True, blank=True, max_length=50)
   email = models.EmailField(max_length=240, unique=True)
   given_name= models.CharField( max_length=50)
   family_name= models.CharField( max_length=50)
    name = models.CharField(null = True, blank = True, max_length=60,unique=True)
   username = models.CharField(null = True, blank = True, max_length=60,unique=True)
   picture = models.ImageField(upload_to="images/", null=True, blank=True , default='5032667_1.png')
    USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['username']
   def __str__(self):
        return self.email
