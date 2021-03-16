from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http.response import StreamingHttpResponse
from asst.src.recognize_faces_ssd import FaceDetect
from asst.src.yolo_object_detection import Temperature
from asst.src.create_dataset import CreateDataset
import pyrebase
from datetime import datetime,timezone
import time
import pytz
import uuid

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

camera = FaceDetect()
temperature = Temperature()
create_dataset = CreateDataset()


def postUserLogin(request):
    userEmail = request.POST.get('userEmail')
    userPassword = request.POST.get('userPassword')
    try:
        user = firebaseAuth.sign_in_with_email_and_password(
            userEmail, userPassword)
        uid = user['localId']
        session_id = user['idToken']
        idToken = request.session['uid'] = str(session_id)
        isAdmin = database.child('users').child('watchman').child(
            uid).child('details').child('isAdmin').get(idToken).val()
        if (isAdmin == False):
            return render(request, 'userDashboard.html')
        else:
            message = "You are not a user"
        return render(request, 'signIn.html', {"message": message})

    except:
        message = "Email/Password is Incorrect , Try Again"
        return render(request, 'signIn.html', {"message": message})


def postForgotPassword(request):
    email = request.POST.get('email')
    # print(email)
    try:
        message = "Reset password link has been sent to your email"
        sent = firebaseAuth.send_password_reset_email(email)
        # print(sent)
        return render(request, 'signIn.html', {"message": message})
    except:
        message = 'Not a valid account'
        return render(request, "forgotPassword.html", {"message": message})


def postVisitorRegistration(request):
    visitorName = request.POST.get('visitorName')
    visitorAddress = request.POST.get('visitorAddress')
    phoneNumber = request.POST.get('phoneNumber')
    visitorWork = request.POST.get('visitorWork')
    flatNo = request.POST.get('flatNo')
    try:

        idToken = request.session['uid']
        info = firebaseAuth.get_account_info(idToken)
        userToken = info['users'][0]['localId']
        data = {"visitorName": visitorName, "visitorAddress": visitorAddress, "phoneNumber": phoneNumber,
                "visitorWork": visitorWork, "flatNo": flatNo}
        secretaryId = database.child('users').child('watchman').child(
            userToken).child('details').child('secretaryId').get(idToken).val()
        database.child("users").child("secretary").child(secretaryId).child(
            "visitors").child(visitorName).set(data, idToken)
        create_dataset.send_label(visitorName)
        return render(request, 'createDataset.html')
    except:
        return render(request, 'visitorRegistration.html')


def postVisitorRecognition(request):
    visitorName = request.POST.get('visitorName')
    visitorAddress = request.POST.get('visitorAddress')
    phoneNumber = request.POST.get('phoneNumber')
    visitorWork = request.POST.get('visitorWork')
    flatNo = request.POST.get('flatNo')
    temperature = request.POST.get('temperature')
    try:
        idToken = request.session['uid']
        info = firebaseAuth.get_account_info(idToken)
        userToken = info['users'][0]['localId']
        # print(userToken)
        secretaryId = database.child('users').child('watchman').child(
            userToken).child('details').child('secretaryId').get(idToken).val()
        # print(secretaryId)
        watchmanName = database.child('users').child('watchman').child(
            userToken).child('details').child('name').get(idToken).val()
        # print(watchmanName)
        # datetime object containing current date and time
        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(timezone.utc).astimezone(tz)
        # now = datetime.now()
        # dd/mm/YY H:M:S
        todayDate = now.strftime("%b-%d-%Y")
        inTime = now.strftime("%H:%M")
        reportId = uuid.uuid4()
        data = {"visitorName": visitorName, "visitorAddress": visitorAddress, "phoneNumber": phoneNumber,
                "visitorWork": visitorWork, "flatNo": flatNo, "temperature": temperature + "°F", "watchmanName": watchmanName, "inTime": inTime}
        database.child("users").child("secretary").child(secretaryId).child(
            "reports").child(todayDate).child(reportId).set(data, idToken)
        return render(request, 'userDashboard.html')
    except:
        return render(request, 'createVisitorReport.html')


def userReports(request):
    worker_details = []
    # data_not_found = True
    try:
        idToken = request.session['uid']
        if (idToken):
            info = firebaseAuth.get_account_info(idToken)
            # print(info)
            userToken = info['users'][0]['localId']
            # print(userToken)
            secretaryId = database.child('users').child('watchman').child(
                userToken).child('details').child('secretaryId').get(idToken).val()
            # print(secretaryId)
            todayDate = datetime.now().strftime("%b-%d-%Y")
            # print(todayDate)
            data = database.child("users").child("secretary").child(
                secretaryId).child("reports").child(todayDate).get(idToken).val()
            # print("data", data)
            if data == None:
                data_not_found = False
                combine = None
            else:
                data_not_found = True
                for key, value in data.items():
                    # print(key)
                    worker_details.append(value)
                # print(worker_details)
                sr_no = list(range(1, len(worker_details) + 1))
                combine = zip(sr_no, worker_details)
            # print(data_not_found)
            return render(request, 'userReports.html', {"data_not_found": data_not_found, "combine": combine})
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})





def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    except:
        pass


def facecam_feed(request):
    camera.camera_init()
    response = StreamingHttpResponse(gen(camera),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
    return response


def temperature_feed(request):
    camera.destroy()
    temperature.camera_init()
    response = StreamingHttpResponse(gen(temperature),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
    return response 


def createDataset_feed(request):
    create_dataset.camera_init()
    return StreamingHttpResponse(gen(create_dataset), content_type='multipart/x-mixed-replace; boundary=frame')


def createVisitorReport(request):
    try:
        temperature.destroy()
        idToken = request.session['uid']
        # print(idToken)
        if (idToken):
            info = firebaseAuth.get_account_info(idToken)
            # print(info)
            userToken = info['users'][0]['localId']
            # print(userToken)
            secretaryId = database.child('users').child('watchman').child(
                userToken).child('details').child('secretaryId').get(idToken).val()
            # print(secretaryId)
            name = camera.get_name()
            temperature1 = temperature.get_temperature()
            camera.re_init()
            temperature.re_init()
            # print(name)
            # print(temperature1)
            if name != 'Guest':
                data = database.child("users").child("secretary").child(
                    secretaryId).child("visitors").child(name).get(idToken).val()
                # print(data)
            else:
                data = {'visitorName': 'Guest', 'flatNo': '',
                        'visitorAddress': '', 'phoneNumber': '', 'visitorWork': ''}
            return render(request, 'createVisitorReport.html', {"data": data, "temperature": temperature1})
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})


def recordVisitorTemperature(request):
    try:
        idToken = request.session['uid']
        if (idToken):
            print(camera.names_display)
            return render(request, 'recordVisitorTemperature.html')
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})
