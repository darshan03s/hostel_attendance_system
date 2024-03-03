from django.shortcuts import render, HttpResponse
from datetime import datetime, date, time
from attendance.models import Register, LoginLogout
import re
from attendance.update_attendance import update_attendance

update_executed_today = False

def index(request):
    global update_executed_today
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'register':
                regusername = request.POST.get('regusername')
                
                usn_pattern = re.compile(r'^4GM\d\d[A-Z][A-Z]\d\d\d$')
                if usn_pattern.match(request.POST.get('regusn')) is not None:
                    regusn = request.POST.get('regusn')
                else :
                    regusn = None
                    return HttpResponse('Invalid USN')
                regbranch = request.POST.get('regbranch')
                regphone = request.POST.get('regphone')
                regpassword = request.POST.get('regpassword')
                regdate = datetime.now()
                registration = Register(STUDENT_NAME=regusername, USN=regusn, BRANCH=regbranch, PHONE=regphone, PASSWORD=regpassword, REGISTRATION_DATE=regdate)
                registration.save()
                
                
                
            elif action == 'login':
                passwords = Register.objects.values_list('USN','PASSWORD')
                passwords_list = list(passwords)
                usn_pass_dict = {usn: password for usn, password in passwords_list}
                usn_pattern = re.compile(r'^4GM\d\d[A-Z][A-Z]\d\d\d$')
                if usn_pattern.match(request.POST.get('logusn')) is not None:
                    logusn = request.POST.get('logusn')
                    try:
                        register_instance = Register.objects.get(USN=logusn)
                    except Register.DoesNotExist:
                        return HttpResponse('You are not registered.')
                    
                    logpassword = request.POST.get('logpassword')
                    logusn = request.POST.get('logusn')
                    if logpassword != usn_pass_dict[logusn]:
                        return HttpResponse('Invalid Password')
                    status = action
                    curr_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                    
                    login_logout = LoginLogout(USN=register_instance, PASSWORD=logpassword, STATUS=status.upper(), LOGIN_LOGOUT_TIME=curr_time)
                    login_logout.save()
                else:
                    return HttpResponse('Invalid USN format.')
                
            elif action == 'logout':
                passwords = Register.objects.values_list('USN','PASSWORD')
                passwords_list = list(passwords)
                usn_pass_dict = {usn: password for usn, password in passwords_list}
                usn_pattern = re.compile(r'^4GM\d\d[A-Z][A-Z]\d\d\d$')
                if usn_pattern.match(request.POST.get('logusn')) is not None:
                    logusn = request.POST.get('logusn')
                    try:
                        register_instance = Register.objects.get(USN=logusn)
                    except Register.DoesNotExist:
                        return HttpResponse('You are not registered.')
                    
                    logpassword = request.POST.get('logpassword')
                    if logpassword != usn_pass_dict[logusn]:
                        return HttpResponse('Invalid Password')
                    status = action
                    curr_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                    
                    login_logout = LoginLogout(USN=register_instance, PASSWORD=logpassword, STATUS=status.upper(), LOGIN_LOGOUT_TIME=curr_time)
                    login_logout.save()
                else:
                    return HttpResponse('Invalid USN format.')

    current_time = datetime.now().time()
    cutoff_datetime = datetime.combine(date.today(), time(21, 0))

    if current_time > cutoff_datetime.time() and not update_executed_today:
        update_attendance() 
        print('Attendance Updated')
        update_executed_today = True
    return render(request, 'index.html')







    # if current_time >= cutoff_datetime.time():