from attendance.models import LoginLogout, Register, TodaysAttendance
from datetime import time, date

def update_attendance():
    today_date = date.today()
    cutoff_time = time(21, 0)  # 21:00

    # Get all login/logout records for today
    today_records = LoginLogout.objects.filter(LOGIN_LOGOUT_TIME__date=today_date)

    # Get unique USNs from today's records
    unique_usns = today_records.values_list('USN', flat=True).distinct()

    for usn in unique_usns:
        # Get the last record before the cutoff time for the current USN
        last_record = today_records.filter(USN=usn, LOGIN_LOGOUT_TIME__time__lt=cutoff_time).order_by('-LOGIN_LOGOUT_TIME').first()

        if last_record:
            # Check if the last record was a login
            if last_record.STATUS == 'LOGIN':
                register_record = Register.objects.get(USN=usn)
                student_name = register_record.STUDENT_NAME
                branch = register_record.BRANCH
                last_login_time = last_record.LOGIN_LOGOUT_TIME

                # Check if attendance for the student already exists for today
                existing_attendance = TodaysAttendance.objects.filter(USN=usn, LAST_LOGIN__date=today_date).exists()
                if not existing_attendance:
                    # Create a new attendance record
                    TodaysAttendance.objects.create(
                        STUDENT_NAME=student_name,
                        USN=register_record,
                        BRANCH=branch,
                        LAST_LOGIN=last_login_time,
                        ATTENDANCE='PRESENT'
                    )