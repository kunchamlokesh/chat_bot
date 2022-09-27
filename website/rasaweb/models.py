from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=6,
        choices=[('MALE','MALE'),('FEMALE','FEMALE')]
    )
    Domain = models.CharField(
        max_length=25,
        choices=[('Business Finance','Business Finance'),('Graphic Design','Graphic Design'),('Musical Instruments','Musical Instruments'),('Web Development','Web Development')],
        default = 'Business Finance'
    )
    Area_of_Interest = models.CharField(max_length=30,default='Python')


    def __str__(self):
        return self.user.username