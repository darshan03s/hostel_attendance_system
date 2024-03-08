from django.db import models
from datetime import datetime

# Register Table
class Register(models.Model):
    STUDENT_NAME = models.CharField(max_length=100)
    USN = models.CharField(max_length=10, primary_key=True, default=None)
    BRANCH = models.CharField(max_length=5)
    PHONE = models.CharField(max_length=10)
    PASSWORD = models.CharField(max_length=15)
    REGISTRATION_DATE = models.DateField()
    
# LoginLogout
class LoginLogout(models.Model):
    USN = models.ForeignKey(Register, on_delete=models.CASCADE, default=None)
    PASSWORD = models.CharField(max_length=15)
    STATUS = models.CharField(max_length=6)
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOGIN_LOGOUT_TIME = models.DateTimeField(default=time)
    
# TodaysAttendance
class TodaysAttendance(models.Model):
    STUDENT_NAME = models.CharField(max_length=100)
    USN = models.ForeignKey(Register, on_delete=models.CASCADE, default=None)
    BRANCH = models.CharField(max_length=5)
    LAST_LOGIN = models.DateTimeField()
    ATTENDANCE = models.CharField(max_length=10)
    
    