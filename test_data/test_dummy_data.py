from datetime import datetime, time, timedelta
import random
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="darshans",
    password="darshans",
    database="test"
)

LIMIT = 50

def clear_todaysattendance():
    cursor = conn.cursor()
    table_name = "attendance_todaysattendance"
    delete_query = f"DELETE FROM {table_name};"
    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()
    
def clear_loginlogout():
    cursor = conn.cursor()
    table_name = "attendance_loginlogout"
    delete_query = f"DELETE FROM {table_name};"
    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()
    
def clear_register():
    cursor = conn.cursor()
    table_name = "attendance_register"
    delete_query = f"DELETE FROM {table_name};"
    cursor.execute(delete_query)
    conn.commit()
    cursor.close()
    conn.close()
    
def dummy_data_register():
    cursor = conn.cursor()
    with open('./test_data/register_dummy_data.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    sql_statements = sql_script.split(';')
    for statement in sql_statements:
        if statement.strip():  # Ignore empty statements
            try:
                cursor.execute(statement)
            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:  # Duplicate entry error code
                    print("Skipping duplicate entry:", e.msg)
                else:
                    raise
    
    conn.commit()
    cursor.close()
    # conn.close()

def dummy_data_loginlogout_subset():
    cursor = conn.cursor()
    command = f"SELECT USN, PASSWORD FROM attendance_register LIMIT {LIMIT}"
    cursor.execute(command)
    existing_records = cursor.fetchall()
    num_dummy_records = 3
    dummy_data = []
    for usn, password in existing_records:
        # Initialize the count of login and logout records
        login_count = 0
        logout_count = 0
        for _ in range(num_dummy_records):
            # Ensure there are at least 2 login and 1 logout records
            if login_count < 2:
                status = 'LOGIN'
                login_count += 1
            else:
                status = 'LOGOUT'
                logout_count += 1
            current_date = datetime.now().date()
            start_time = time(6, 0, 0)  # 06:00
            end_time = time(23, 59, 59)  # 23:59
            random_time = (
                datetime.combine(current_date, start_time)
                + timedelta(seconds=random.randint(0, int((datetime.combine(current_date, end_time) - datetime.combine(current_date, start_time)).total_seconds())))
            ).time()
            random_datetime = datetime.combine(current_date, random_time)
            login_logout_time = random_datetime.strftime('%Y-%m-%d %H:%M:%S')
            dummy_data.append((usn, password, status, login_logout_time))
    for record in dummy_data:
        usn, password, status, login_logout_time = record
        sql = f"INSERT INTO test.attendance_loginlogout (USN_id, PASSWORD, STATUS, LOGIN_LOGOUT_TIME) VALUES ('{usn}', '{password}', '{status}', '{login_logout_time}');"
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    # conn.close()

     
# clear_todaysattendance()
# clear_loginlogout()
# clear_register()
# dummy_data_register()
# dummy_data_loginlogout_subset()
# dummy_data_all()