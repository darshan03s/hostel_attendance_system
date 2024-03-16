from django.shortcuts import redirect
# from datetime import datetime, date, time
import datetime 
from attendance.models import Register, LoginLogout
import re
from .update_attendance import update_attendance
from django.contrib import messages

""" Function to check if usn is valid"""
def validate_usn(usn):
    usn_pattern = re.compile(r'^4GM\d\d[A-Z][A-Z]\d\d\d$')
    return usn_pattern.match(usn) is not None


"""Function to create record of student registration
Details stored - Name, USN, Branch, Phone , Date of Registration. Password"""
def register_student(request):
    """Get data from the html form"""
    
    regusername = request.POST.get('regusername')
    regusn = request.POST.get('regusn')
    if not validate_usn(regusn):
        messages.error(request, 'Invalid USN')            
        return redirect('/')               
    regbranch = request.POST.get('regbranch')
    regphone = request.POST.get('regphone')
    regpassword = request.POST.get('regpassword')
    regdate = datetime.date.today()                                            #get date 
    
    """Create register object and save the details"""
    registration = Register(STUDENT_NAME=regusername, USN=regusn, BRANCH=regbranch, PHONE=regphone, PASSWORD=regpassword, REGISTRATION_DATE=regdate)
    registration.save()
    messages.success(request, f'Successfully registered {regusername} {regusn} {regbranch}')
    
    
""" Function to create records of login and logout activity of students
Details stored - USN, Login date-time"""
def login_logout_student(request, action):
    """Get data from the html form"""
    
    logusn = request.POST.get('logusn')
    if not validate_usn(logusn):                                        #validate usn
        messages.error(request, 'Invalid USN')            
        return redirect('/')
    try:
        register_instance = Register.objects.get(USN=logusn)            #check if student has registered
    except Register.DoesNotExist:
        messages.error(request, 'You are not registered.')            
        return redirect('/')
    logpassword = request.POST.get('logpassword')
    passwords = Register.objects.values_list('USN', 'PASSWORD')
    passwords_list = list(passwords)
    usn_pass_dict = {usn: password for usn, password in passwords_list}
    if logpassword != usn_pass_dict[logusn]:                            #check if usn matches with students created password
        messages.error(request, 'Invalid Password')            
        return redirect('/')
    status = action.upper()                                             #convert string to uppercase
    curr_time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")          #store login date-time
    login_logout = LoginLogout(USN=register_instance, PASSWORD=logpassword, STATUS=status, LOGIN_LOGOUT_TIME=curr_time)
    login_logout.save()
    messages.success(request, f'{logusn} {status}')
    
# def run_update(request, test=False):
#     current_time = datetime.datetime.now().time()                                
#     cutoff_datetime = datetime.datetime.combine(datetime.date.today(), datetime.time(21, 0))     
#     update_executed_today = False
#     if not update_executed_today:
#         if current_time > cutoff_datetime.time():    
#             update_attendance()                         
#             messages.success(request, f'Attendance updated at {datetime.now().strftime("%H:%M:%S")}')
#             update_executed_today = True
#     if test==True:
#         update_attendance()                         
#         messages.success(request, f'Attendance updated at {datetime.now().strftime("%H:%M:%S")}')


def run_update(request, test=False):
    current_time = datetime.datetime.now().time()
    cutoff_time = datetime.time(21, 0)  # 9:00 PM
    today_date = datetime.date.today()
    cutoff_datetime = datetime.datetime.combine(today_date, cutoff_time)
    attendance_updated_today = False
    if not test:
        if current_time > cutoff_datetime and not attendance_updated_today:
            update_attendance()
            attendance_updated_today = True
            messages.success(request, f'Attendance updated at {datetime.datetime.now().strftime("%H:%M:%S")}')
    else:
        update_attendance()
        messages.success(request, f'Attendance updated at {datetime.datetime.now().strftime("%H:%M:%S")}')