from django.db import models

# Create your models here.


# 用户表
class useraccount(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=20)
    logintime = models.DateTimeField(auto_now_add=True)
    lastlogintime = models.DateTimeField(auto_now_add=True)
    loginip = models.CharField(max_length=20, default='0.0.0.0')
    lastloginip = models.CharField(max_length=20, default='0.0.0.0')

