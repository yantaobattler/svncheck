# Generated by Django 2.1.5 on 2019-03-14 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0003_auto_20190313_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='logintime',
            field=models.DateTimeField(),
        ),
    ]