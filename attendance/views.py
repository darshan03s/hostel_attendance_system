from django.shortcuts import render
from datetime import datetime, date, time
from .custom.operations import * 
from django.contrib import messages

update_executed_today = False

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
        messages.success(request, f'Attendance updated at {datetime.now().strftime("%H:%M:%S")}')
        update_executed_today = True
        
    """For testing"""
    update_attendance()                         
    messages.success(request, f'Attendance updated at {datetime.now().strftime("%H:%M:%S")}')
    
    return render(request, 'index.html')        