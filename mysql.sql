SELECT * FROM final_dbms3.attendance_register ORDER BY REGISTRATION_DATE DESC;

SELECT * FROM final_dbms3.attendance_loginlogout ORDER BY id DESC;

SELECT * FROM final_dbms3.attendance_todaysattendance ORDER BY id DESC ;


-- MySQL equivalent code for Django Models
-- Register Table
CREATE TABLE Register (
    STUDENT_NAME VARCHAR(100),
    USN CHAR(10) PRIMARY KEY,
    BRANCH CHAR(5),
    PHONE CHAR(10),
    PASSWORD CHAR(15),
    REGISTRATION_DATE DATE
);

-- LoginLogout
CREATE TABLE LoginLogout (
    id INT AUTO_INCREMENT PRIMARY KEY,
    USN CHAR(10),
    PASSWORD CHAR(15),
    STATUS CHAR(6),
    LOGIN_LOGOUT_TIME DATETIME,
    FOREIGN KEY (USN) REFERENCES Register(USN)
);

-- TodaysAttendance
CREATE TABLE TodaysAttendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    STUDENT_NAME VARCHAR(100),
    USN CHAR(10),
    BRANCH CHAR(5),
    LAST_LOGIN DATETIME,
    ATTENDANCE CHAR(10),
    FOREIGN KEY (USN) REFERENCES Register(USN)
);

DESC final_dbms3.attendance_register;

DESC final_dbms3.attendance_loginlogout;

DESC final_dbms3.attendance_todaysattendance;



-- truncate table final_dbms3.attendance_todaysattendance; 