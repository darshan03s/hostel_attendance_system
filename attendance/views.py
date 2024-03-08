from django.shortcuts import render, HttpResponse
from datetime import datetime, date, time
from attendance.models import Register, LoginLogout
import re
from attendance.update_attendance import update_attendance

""" Set this flag to false , when attendance is updated at 21:00 , this flag becomes true. """
update_executed_today = False

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
        return HttpResponse('Invalid USN')                              #returns a blank page response with only text
    regbranch = request.POST.get('regbranch')
    regphone = request.POST.get('regphone')
    regpassword = request.POST.get('regpassword')
    regdate = datetime.now()                                            #get current date and time
    
    """Create register object and save the details"""
    registration = Register(STUDENT_NAME=regusername, USN=regusn, BRANCH=regbranch, PHONE=regphone, PASSWORD=regpassword, REGISTRATION_DATE=regdate)
    registration.save()

""" Function to create records of login and logout activity of students
Details stored - USN, Login date-time"""
def login_logout_student(request, action):
    """Get data from the html form"""
    
    logusn = request.POST.get('logusn')
    if not validate_usn(logusn):                                        #validate usn
        return HttpResponse('Invalid USN format.')
    try:
        register_instance = Register.objects.get(USN=logusn)            #check if student has registered
    except Register.DoesNotExist:
        return HttpResponse('You are not registered.')
    logpassword = request.POST.get('logpassword')
    passwords = Register.objects.values_list('USN', 'PASSWORD')
    passwords_list = list(passwords)
    usn_pass_dict = {usn: password for usn, password in passwords_list}
    if logpassword != usn_pass_dict[logusn]:                            #check if usn matches with students created password
        return HttpResponse('Invalid Password')
    status = action.upper()                                             #convert string to uppercase
    curr_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")          #store login date-time
    login_logout = LoginLogout(USN=register_instance, PASSWORD=logpassword, STATUS=status, LOGIN_LOGOUT_TIME=curr_time)
    login_logout.save()

def index(request):
    global update_executed_today
    if request.method == 'POST':                                        #request sent from html form to backend using POST http-request
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'register':
                register_student(request)
            elif action == 'login':
                login_logout_student(request, action)
            elif action == 'logout':
                login_logout_student(request, action)

    current_time = datetime.now().time()                                #to only check attendance for todays date
    cutoff_datetime = datetime.combine(date.today(), time(21, 0))       #set cut-off time to 21:00 

    if current_time > cutoff_datetime.time() and not update_executed_today:     
        update_attendance()                                             #update_attendance() runs once a day at 21:00 for todays date
        print('Attendance Updated')
        update_executed_today = True                                    #update flag to true after function executed once once
        
        
    """For testing purpose"""
    # update_attendance()
    # print('Attendance Updated')

    return render(request, 'index.html')                                #return the html page stored in templates folder using render method