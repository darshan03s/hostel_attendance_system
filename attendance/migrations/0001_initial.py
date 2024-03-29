# Generated by Django 5.0.1 on 2024-03-13 10:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('STUDENT_NAME', models.CharField(max_length=100)),
                ('USN', models.CharField(default=None, max_length=10, primary_key=True, serialize=False)),
                ('BRANCH', models.CharField(max_length=5)),
                ('PHONE', models.CharField(max_length=10)),
                ('PASSWORD', models.CharField(max_length=15)),
                ('REGISTRATION_DATE', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='LoginLogout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PASSWORD', models.CharField(max_length=15)),
                ('STATUS', models.CharField(max_length=6)),
                ('LOGIN_LOGOUT_TIME', models.DateTimeField(default='2024-03-13 15:35:43')),
                ('USN', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='attendance.register')),
            ],
        ),
        migrations.CreateModel(
            name='TodaysAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('STUDENT_NAME', models.CharField(max_length=100)),
                ('BRANCH', models.CharField(max_length=5)),
                ('LAST_LOGIN', models.DateTimeField()),
                ('ATTENDANCE', models.CharField(max_length=10)),
                ('USN', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='attendance.register')),
            ],
        ),
    ]
