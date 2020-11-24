from django.shortcuts import render
#from login.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth import authenticate,login,logout
#from .models import UserProfileInfo, CourseSession
from django.db import connection
import cx_Oracle
#from django.contrib.auth.models import User
import os
import hashlib
from django.contrib import messages



# Create your views here.
def index(request):
    # dsn_tns = cx_Oracle.makedsn('localhost', '1521',
    #                             service_name='ORCL')
    # assert isinstance(dsn_tns, object)
    # connection = cx_Oracle.connect('noobshafaet', '123456', dsn_tns)
    return render(request, "login/homepage.html")

#@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    print('I am in sign up')
    usr = None
    try:
        user_logout(request)
    except:
        print('sign up please')
        print('couldnt make it')
    if request.method == "POST":
        profileid = request.POST.get('profileid')
        username = request.POST.get('username')
        emailid = request.POST.get('emailid')
        dateofbirth = request.POST.get('dateofbirth')
        city = request.POST.get('city')
        street = request.POST.get('street')
        password = request.POST.get('password')
        role = request.POST.get('Role')
        salt = os.urandom(32)
        # password = 'password123'
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,  # 100,000 iterations of SHA-256
            # dklen=128  #128 byte key
        )
        is_teacher = None
        is_student = None
        if (role == "Teacher"):
            is_teacher = 1
            is_student = 0

        elif (role == "Student"):
            is_student =1
            is_teacher = 0

        sql = "INSERT INTO PEOPLE(PROFILE_ID, NAME, EMAIL_ID, DATE_OF_BIRTH, CITY, STREET , KEY, SALT,IS_STUDENT, IS_TEACHER) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor = connection.cursor()

            cursor.execute(sql, [profileid, username, emailid, dateofbirth, city, street, key, salt, is_student, is_teacher])
            connection.commit()
            cursor.close()
            print('trying')
            return redirect('login/homepage.html')
        except:
            print('except')
            return render(request, 'login/homepage.html', {'message': "Thanks! your Resgistration is successful!"})
    else:
        print('nothing')
        return render(request, 'login/registration.html', {})

def user_login(request):
    print("i m log in")

    try:
        usr = request.session['username']
        return redirect('/login/homepage.html')
    except:
        print("not logged in please log in")

    if request.method == 'POST':
        # email = request.POST.get('email')
        # print(email)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        msg = 'Enjoy Buying!'
        try:
            cur = connection.cursor()
            sql = "select  NAME, KEY ,SALT, PROFILE_ID from PEOPLE where NAME = %s"
            print(sql)
            print(username)
            cur.execute(sql,[username])
            result = cur.fetchone()
            dic_res = []
            # dbemail = None
            dbkey = None
            dbuser = None
            dbsalt = None
            name = None
            dbuser = result[0]
            dbkey = result[1]
            dbsalt = result[2]
            name = result[3]

            # for r in result:
            #     dbuser = r[0]
            #     dbkey = r[1]
            #     dbsalt = r[2]
            #     name = r[3]

            print("from database:...")
            print("dbuser:" + dbuser)
            if dbuser == username:
                print("username verified")
                new_key =hashlib.pbkdf2_hmac(
                    'sha256',  # The hash digest algorithm for HMAC
                    password.encode('utf-8'),
                    dbsalt ,
                    100000, # 100,000 iterations of SHA-256
                    # dklen = 128
                )

                if new_key == dbkey:
                    print("success")
                    print("sql:" + sql)
                    # request.session.__setitem__('username',dbuser)
                    request.session['username'] = dbuser
                    request.session['name'] = name
                    # request.session.__setitem__('username',username)
                    print("success2")
                    print("usernameform session: " + request.session['username'])
                    #return redirect('/home')
                    return redirect('/home')
                    #return render(request, 'login/homepage.html', {'isLoggedIn':True})

                else:
                    print("failed man!")
                    print("dbkey: ")
                    print(dbkey)
                    print("userkey: ")
                    print(new_key)
                    return redirect('/home')
                    #return render(request, 'login/homepage.html', {'isLoggedIn': True})

            else:
                print("wrong username!")
                return redirect('user_login/')
        except:
            messages = "something went wrong! try again"
            print(messages)
            return render(request,'login/login.html')
    else:
        return render(request, 'login/login.html')

def list_sessions(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521',service_name='ORCL')
    #assert isinstance(dsn_tns, object)
    connection = cx_Oracle.connect('moodleproject','123456', dsn_tns)
    cursor = connection.cursor()
    sql = "SELECT * FROM COURSE"
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    dict_result = []

    for r in result:
        course_id = r[0]
        session_id = r[1]
        course_title = r[2]
        credit_hour = r[3]
        row = {'course_id':course_id, 'session_id':session_id, 'course_title':course_title,'credit_hour':credit_hour}
        dict_result.append(row)

    return render(request,'login/course_list.html',{'COURSE': dict_result})


def list_people(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    # assert isinstance(dsn_tns, object)
    #connection = cx_Oracle.connect('moodleproject', '123456', dsn_tns)
    cursor = connection.cursor()
    sql = "SELECT * FROM PEOPLE"
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    dict_result = []

    for r in result:
        profile_id = r[0]
        profile_name = r[1]
        profile_email = r[2]
        profile_dob = r[3]
        profile_city = r[4]
        profile_street = r[5]
        #profile_password = r[6]
        profile_is_student = r[8]
        profile_is_teacher = r[9]


        row = {'pro_id': profile_id, 'pro_name': profile_name, 'pro_email': profile_email,
               'pro_dob': profile_dob, 'pro_city' : profile_city, 'pro_street' : profile_street, 'pro_student' : profile_is_student, 'pro_teacher': profile_is_teacher }
        dict_result.append(row)

    return render(request, 'login/people.html', {'PEOPLE_PROFILE': dict_result})

def studentlogin(request):
    return render(request,'login/studentlogin.html')
def teacherlogin(request):
    return render(request, 'login/TeacherLogin.html')

def file_upload(request):
    return render(request, 'login/fileupload.html')

    """""
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    # assert isinstance(dsn_tns, object)
    connection = cx_Oracle.connect('noobshafaet', '123456', dsn_tns)
    cursor = connection.cursor()
    sql = "SELECT * FROM ASSUGNMENT_FILES"
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    dict_result = []
    for r in result:
        file_path = r[0]
    row = {'file_path':FILE_LINK}
    dict_result.append(row)
"""





