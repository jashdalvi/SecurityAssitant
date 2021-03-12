from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.http import HttpResponse
from asst.src.recognize_faces_ssd import FaceDetect
from asst.src.yolo_object_detection import Temperature


def userDashboard(request):
    if request.method == 'POST':
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword')
        print(" userEmail : ", userEmail)
        print(" userPassword : ", userPassword)
        return render(request, 'userDashboard.html')
    return render(request, 'userDashboard.html')


def visitorRegistration(request):
    return render(request, 'visitorRegistration.html')


def postVisitorRegistration(request):
    if request.method == 'POST':
        visitorName = request.POST.get('visitorName')
        # gender = request.POST.get('gender')
        visitorAddress = request.POST.get('visitorAddress')
        phoneNumber = request.POST.get('phoneNumber')
        visitorWork = request.POST.get('visitorWork')
        flatNo = request.POST.get('flatNo')
        print("visitorName : ", visitorName)
        # print("gender: ", gender)
        print("visitorAddress : ", visitorAddress)
        print("phoneNumber : ", phoneNumber)
        print("visitorWork : ", visitorWork)
        print("flatNo : ", flatNo)
        return render(request, 'userDashboard.html')
    return render(request, 'visitorRegistration.html')


def postVisitorRecognition(request):
    if request.method == 'POST':
        visitorName = request.POST.get('visitorName')
        visitorAddress = request.POST.get('visitorAddress')
        phoneNumber = request.POST.get('phoneNumber')
        visitorWork = request.POST.get('visitorWork')
        flatNo = request.POST.get('flatNo')
        temperature = request.POST.get('temperature')
        print("visitorName : ", visitorName)
        print("visitorAddress : ", visitorAddress)
        print("phoneNumber : ", phoneNumber)
        print("visitorWork : ", visitorWork)
        print("flatNo : ", flatNo)
        print("temperature : ", temperature)
        return render(request, 'userDashboard.html')
    return render(request, 'createVisitorReport.html')


def userReports(request):
    return render(request, 'userReports.html')


def faceRecognition(request):
    return render(request, 'faceRecognition.html')

camera = FaceDetect()
temperature = Temperature()


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
    return StreamingHttpResponse(gen(camera),
                                content_type='multipart/x-mixed-replace; boundary=frame')

def temperature_feed(request):
    camera.destroy()
    temperature.camera_init()

    return StreamingHttpResponse(gen(temperature),
                                content_type='multipart/x-mixed-replace; boundary=frame')

def createVisitorReport(request):
    temperature.destroy()
    print(camera.get_name())
    print(temperature.get_temperature())
    return render(request, 'createVisitorReport.html')

def recordVisitorTemperature(request):
    return render(request, 'recordVisitorTemperature.html')

# def facecam_feed(request):
#     camera = FaceDetect()
#     while True:
#         frame = camera.get_frame()
#         message = (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#         response = HttpResponse(message,content_type='multipart/x-mixed-replace; boundary=frame',streaming = True)
#         response['Content-Disposition'] = 'multipart/x-mixed-replace; boundary=frame'

#         response['Content-Length'] = len(message)

#         return response
