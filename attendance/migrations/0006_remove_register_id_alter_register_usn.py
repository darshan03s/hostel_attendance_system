# Generated by Django 4.2.5 on 2024-03-01 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_rename_user_name_register_student_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='id',
        ),
        migrations.AlterField(
            model_name='register',
            name='USN',
            field=models.CharField(default=None, max_length=10, primary_key=True, serialize=False),
        ),
    ]
