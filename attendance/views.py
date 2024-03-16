from django.shortcuts import render
from .custom.operations import * 

def index(request):
    if request.method == 'POST':        
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'register':
                register_student(request)
            elif action == 'login':
                login_logout_student(request, action)
            elif action == 'logout':
                login_logout_student(request, action)
                
    run_update(request, test=True)
    
    return render(request, 'index.html')        