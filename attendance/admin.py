from django.contrib import admin
from attendance.models import Register, LoginLogout, TodaysAttendance

admin.site.register(Register)
admin.site.register(LoginLogout)
admin.site.register(TodaysAttendance)
