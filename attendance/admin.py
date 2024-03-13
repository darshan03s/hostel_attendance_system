from django.contrib import admin
from attendance.models import Register, LoginLogout, TodaysAttendance

class RegisterAdmin(admin.ModelAdmin):
  list_display = ('STUDENT_NAME', 'USN', 'BRANCH', 'PHONE', 'PASSWORD', 'REGISTRATION_DATE')
  list_display_links = ('STUDENT_NAME', 'USN')
  list_filter = ('BRANCH','REGISTRATION_DATE')
  show_facets = admin.ShowFacets.ALWAYS
  search_fields = ('STUDENT_NAME', 'USN', 'BRANCH', 'PHONE',)
admin.site.register(Register, RegisterAdmin)

class LoginLogoutAdmin(admin.ModelAdmin):
  list_display = ('USN', 'STATUS', 'LOGIN_LOGOUT_TIME')
  list_display_links = ('USN',)
  list_filter = ('STATUS',)
  show_facets = admin.ShowFacets.ALWAYS
  search_fields = ('USN', 'STATUS')
admin.site.register(LoginLogout, LoginLogoutAdmin)

class TodaysAttendanceAdmin(admin.ModelAdmin):
  list_display = ('STUDENT_NAME', 'USN', 'BRANCH', 'LAST_LOGIN', 'ATTENDANCE')
  list_display_links = ('STUDENT_NAME', 'USN',)
  list_filter = ('BRANCH',)
  show_facets = admin.ShowFacets.ALWAYS
  search_fields = ('STUDENT_NAME', 'USN', 'BRANCH')
admin.site.register(TodaysAttendance, TodaysAttendanceAdmin)
