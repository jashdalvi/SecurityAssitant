from django.shortcuts import render
import pyrebase
from datetime import datetime,timezone
import pandas as pd
import pytz

firebaseConfig = {
    "apiKey": "AIzaSyDTxZrx6g5MiyLZwlvwzCA5oPOHLphxsd8",
    "authDomain": "asst-c43bb.firebaseapp.com",
    "databaseURL": "https://asst-c43bb-default-rtdb.firebaseio.com",
    "projectId": "asst-c43bb",
    "storageBucket": "asst-c43bb.appspot.com",
    "messagingSenderId": "415093243443",
    "appId": "1:415093243443:web:b7241504706fdf07a52d46",
    "measurementId": "G-8FL5E9K5N3"
}

firebase = pyrebase.initialize_app(firebaseConfig)

firebaseAuth = firebase.auth()
database = firebase.database()


def postAdminLogin(request):
    adminEmail = request.POST.get('adminEmail')
    adminPassword = request.POST.get('adminPassword')
    try:
        user = firebaseAuth.sign_in_with_email_and_password(
            adminEmail, adminPassword)
        uid = user['localId']
        session_id = user['idToken']
        idToken = request.session['uid'] = str(session_id)
        check = database.child('users').child('secretary').child(
            uid).child('details').child('isAdmin').get(idToken).val()
        # print("check : ", check)
        if (check):
            return render(request, 'adminDashboard.html')
        else:
            message = "You are not an Admin"
            return render(request, 'signIn.html', {"message": message})
    except:
        message = "Email/Password is Incorrect , Try Again"
        return render(request, 'signIn.html', {"message": message})


def postUserRegistration(request):
    userName = request.POST.get('userName')
    phoneNumber = request.POST.get('phoneNumber')
    userEmail = request.POST.get('userEmail')
    userPassword = request.POST.get('userPassword')
    buildingAssigned = request.POST.get('buildingAssigned')
    try:
        user = firebaseAuth.create_user_with_email_and_password(
            userEmail, userPassword)
        uid = user['localId']
        idToken = str(user['idToken'])
        secretaryToken = request.session['uid']
        info = firebaseAuth.get_account_info(secretaryToken)
        secretaryId = info['users'][0]['localId']
        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(timezone.utc).astimezone(tz)
        todayDate = now.strftime("%d,%b %Y %H:%M")
        data = {"name": userName, "email": userEmail,
                "phoneNumber": phoneNumber, "buildingAssigned": buildingAssigned,
                "isAdmin": False, "secretaryId": secretaryId, "createdAt": todayDate}
        database.child("users").child("watchman").child(
            uid).child("details").set(data, idToken)
        return render(request, 'adminDashboard.html')
    except:
        message = "Unable to create account , Try Again"
        return render(request, 'userRegistration.html', {"message": message})


def users(request):
    user_details = []
    idMatch = ""
    data_found = False
    try:
        idToken = request.session['uid']
        if (idToken):
            info = firebaseAuth.get_account_info(idToken)
            secretaryId = info['users'][0]['localId']
            data = database.child('users').child('watchman').get(idToken).val()
            for key, value in data.items():
                for i, j in value.items():
                    idMatch = j['secretaryId']
                    # print(idMatch)
                    if idMatch == secretaryId:
                        user_details.append(j)
                        print(user_details)
                        data_found = True
            # print(data_found)
            sr_no = list(range(1, len(user_details) + 1))
            combine = zip(sr_no, user_details)
            return render(request, 'users.html', {"combine": combine, "data_found": data_found})
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})


def adminReports(request):
    worker_details = []
    # data_not_found = True
    try:
        idToken = request.session['uid']
        print(idToken)
        if (idToken):
            info = firebaseAuth.get_account_info(idToken)
            userToken = info['users'][0]['localId']
            print(userToken)
            tz = pytz.timezone('Asia/Kolkata')
            now = datetime.now(timezone.utc).astimezone(tz)
            # now = datetime.now()
            # dd/mm/YY H:M:S
            todayDate = now.strftime("%b-%d-%Y")
            print(todayDate)
            data = database.child("users").child("secretary").child(
                userToken).child("reports").child(todayDate).get(idToken).val()
            print(data)
            if data == None:
                data_not_found = False
                combine = None
            else:
                data_not_found = True
                excel_file = []
                for key, value in data.items():
                    # print(key)
                    temp_data = []
                    worker_details.append(value)
                    column_names = []
                    for i,j in value.items():
                        column_names.append(i)
                        temp_data.append(j)
                    excel_file.append(temp_data)
                    print(column_names)
                    print(temp_data)
                print(excel_file)
                df = pd.DataFrame(excel_file,columns = column_names)
                df["date"] = pd.to_datetime(df["inTime"],format = "%H:%M")
                df = df.sort_values(by = "date",ascending = True)
                df_save = df.drop("date",axis = 1)
                df_save.to_csv("/home/jash/Desktop/JashWork/asst21/asst/output/report{}.csv".format(todayDate),index = False)
                columns = df_save.columns
                data_send = df_save.values.tolist()
                worker_details = []
                for x in data_send:
                    temp_dict = {}
                    for i,j in zip(columns,x):
                        temp_dict[i] = j
                    worker_details.append(temp_dict)
                print(worker_details)
                sr_no = list(range(1, len(worker_details) + 1))
                combine = zip(sr_no, worker_details)
            # print(data_not_found)
            return render(request, 'adminReports.html', {"data_not_found": data_not_found, "combine": combine})
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})

