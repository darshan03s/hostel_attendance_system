# Generated by Django 4.2.5 on 2024-03-02 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_todaysattendance_alter_loginlogout_login_logout_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginlogout',
            name='LOGIN_LOGOUT_TIME',
            field=models.DateTimeField(default='2024-03-02 12:52:21'),
        ),
    ]
