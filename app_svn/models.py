from django.db import models


# Create your models here.
# python36 manage.py makemigrations
# python36 manage.py migrate


# svn检查主表
class check_main(models.Model):
    id = models.AutoField(primary_key=True)
    check_no = models.CharField(max_length=20, default='')
    sys_name = models.CharField(max_length=10, default='')
    sub_req_code = models.CharField(max_length=20, default='')
    sub_req_name = models.CharField(max_length=200, default='')
    UD_FD_code = models.CharField(max_length=20, default='')
    qm = models.CharField(max_length=30, default='')
    upload_user = models.CharField(max_length=50, default='')
    path = models.CharField(max_length=100, default='')
    excel_name = models.CharField(max_length=100, default='')
    upload_time = models.DateTimeField(auto_now_add=True)


# svn检查明细
class check_detail(models.Model):
    id = models.AutoField(primary_key=True)
    check_no = models.CharField(max_length=20)
    excel_line = models.CharField(max_length=10)
    line_name = models.CharField(max_length=200)
    problem = models.CharField(max_length=3)
    check_time = models.DateTimeField(auto_now_add=True)


# tag log
class tag_log(models.Model):
    id = models.AutoField(primary_key=True)
    sys_name = models.CharField(max_length=10)
    svn_version = models.CharField(max_length=10)
    v_version = models.CharField(max_length=20)
    UD_FD_code = models.CharField(max_length=20)
    trunk_url = models.CharField(max_length=100)
    tag_url = models.CharField(max_length=100)
    sub_req_code = models.CharField(max_length=20)
    sub_req_name = models.CharField(max_length=200)
    user = models.CharField(max_length=50)
    stat = models.CharField(max_length=2, default='')
    msg = models.CharField(max_length=100, default='')
    check_time = models.DateTimeField(auto_now_add=True)
