from django.db import models
from django.conf import settings
from persiantools.jdatetime import JalaliDate

# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255,null=True,blank=True)
    last_name=models.CharField(max_length=255,null=True,blank=True)
    job=models.CharField(max_length=255,null=True,blank=True)
    avatar=models.ImageField(upload_to='profile/',null=True,blank=True)
    phone_number=models.CharField(max_length=11,null=True,blank=True)
    email=models.CharField(max_length=255,null=True,blank=True)
    birth_date=models.DateField(null=True,blank=True)
    credit_card=models.CharField(max_length=16,null=True,blank=True)

    def __str__(self):
        return self.first_name

    def jalali_date(self):
        return JalaliDate(self.birth_date).strftime("%Y/%m/%d")