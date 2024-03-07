from django.shortcuts import render, HttpResponse
from datetime import datetime, date, time
from attendance.models import Register, LoginLogout
import re
from attendance.update_attendance import update_attendance

update_executed_today = False

def validate_usn(usn):
    usn_pattern = re.compile(r'^4GM\d\d[A-Z][A-Z]\d\d\d$')
    return usn_pattern.match(usn) is not None

def register_student(request):
    regusername = request.POST.get('regusername')
    regusn = request.POST.get('regusn')
    if not validate_usn(regusn):
        return HttpResponse('Invalid USN')
    regbranch = request.POST.get('regbranch')
    regphone = request.POST.get('regphone')
    regpassword = request.POST.get('regpassword')
    regdate = datetime.now()
    registration = Register(STUDENT_NAME=regusername, USN=regusn, BRANCH=regbranch, PHONE=regphone, PASSWORD=regpassword, REGISTRATION_DATE=regdate)
    registration.save()

def login_logout_student(request, action):
    logusn = request.POST.get('logusn')
    if not validate_usn(logusn):
        return HttpResponse('Invalid USN format.')
    try:
        register_instance = Register.objects.get(USN=logusn)
    except Register.DoesNotExist:
        return HttpResponse('You are not registered.')
    logpassword = request.POST.get('logpassword')
    passwords = Register.objects.values_list('USN', 'PASSWORD')
    passwords_list = list(passwords)
    usn_pass_dict = {usn: password for usn, password in passwords_list}
    if logpassword != usn_pass_dict[logusn]:
        return HttpResponse('Invalid Password')
    status = action.upper()
    curr_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    login_logout = LoginLogout(USN=register_instance, PASSWORD=logpassword, STATUS=status, LOGIN_LOGOUT_TIME=curr_time)
    login_logout.save()

def index(request):
    global update_executed_today
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'register':
                register_student(request)
            elif action == 'login':
                login_logout_student(request, action)
            elif action == 'logout':
                login_logout_student(request, action)

    current_time = datetime.now().time()
    cutoff_datetime = datetime.combine(date.today(), time(21, 0))

    if current_time > cutoff_datetime.time() and not update_executed_today:
        update_attendance()
        print('Attendance Updated')
        update_executed_today = True
        
        
        
    # update_attendance()
    # print('Attendance Updated')

    return render(request, 'index.html')