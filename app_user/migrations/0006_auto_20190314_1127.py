# Generated by Django 2.1.5 on 2019-03-14 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0005_auto_20190314_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='lastloginip',
            field=models.CharField(default='0.0.0.0', max_length=20),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='loginip',
            field=models.CharField(default='0.0.0.0', max_length=20),
        ),
    ]
