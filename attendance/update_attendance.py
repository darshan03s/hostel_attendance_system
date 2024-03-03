from attendance.models import LoginLogout, Register, TodaysAttendance
from datetime import datetime, time, date

def update_attendance():
    today_date = date.today()
    cutoff_time = time(21, 0)  # 21:00

    login_records = LoginLogout.objects.filter(STATUS='LOGIN').values_list('USN', flat=True)
    login_usn_list = list(login_records)

    last_login_times = {}
    for usn in login_usn_list:
        last_record = None
        records = LoginLogout.objects.filter(USN=usn).order_by('-pk')
        
        for record in records:
            if record.LOGIN_LOGOUT_TIME.time() < cutoff_time:
                last_record = record
                break
            
        if last_record and last_record.STATUS == 'LOGIN':  
            last_login_time = last_record.LOGIN_LOGOUT_TIME
            last_login_time_str = last_login_time.strftime("%Y-%m-%d %H:%M:%S")
            last_login_times[usn] = last_login_time_str
        else:
            last_login_times[usn] = None

    user_details = {}
    for usn, last_login_time in last_login_times.items():
        register_record = Register.objects.filter(USN=usn).first()
        if register_record:
            user_details[usn] = {
                'branch': register_record.BRANCH,
                'student_name': register_record.STUDENT_NAME,
                'phone': register_record.PHONE,
                'last_login_time': last_login_time
            }
        else:
            user_details[usn] = None
            
    for usn, details in user_details.items():
        if details is not None:
            student_name = details.get('student_name')
            branch = details.get('branch')
            last_login_time_str = details.get('last_login_time')
            if last_login_time_str is not None:
                last_login_date_str = last_login_time_str[:10]  
                
                if last_login_date_str == str(today_date):
                    last_login_time = datetime.strptime(last_login_time_str, "%Y-%m-%d %H:%M:%S")  
                    last_login_time_time = last_login_time.time()  
                    
                    # Check if attendance for the student on the current date already exists
                    existing_attendance = TodaysAttendance.objects.filter(USN=usn, LAST_LOGIN__date=today_date).exists()
                    if not existing_attendance:  # If attendance does not exist, create a new entry
                        if last_login_time_time <= cutoff_time:
                            attendance_status = 'PRESENT'
                        else:
                            attendance_status = 'ABSENT'
                        
                        TodaysAttendance.objects.create(
                            STUDENT_NAME=student_name,
                            USN=usn,
                            BRANCH=branch,
                            LAST_LOGIN=last_login_time,
                            ATTENDANCE=attendance_status  
                        )



# update_attendance()
# TodaysAttendance.objects.all().delete()