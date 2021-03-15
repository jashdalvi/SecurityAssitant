from django.shortcuts import render, redirect


def signIn(request):
    return render(request, 'signIn.html')


def logout(request):
    try:
        del request.session['uid']
        return render(request, 'signIn.html')
    except KeyError:
        pass


def adminDashboard(request):
    try:
        idToken = request.session['uid']
        if (idToken):
            return render(request, 'adminDashboard.html')
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})


def userDashboard(request):
    try:
        idToken = request.session['uid']
        if (idToken):
            return render(request, 'userDashboard.html')
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})


def visitorRegistration(request):
    try:
        idToken = request.session['uid']
        if (idToken):
            return render(request, 'visitorRegistration.html')
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})


def userRegistration(request):
    try:
        idToken = request.session['uid']
        if (idToken):
            return render(request, 'userRegistration.html')
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})


def faceRecognition(request):
    try:
        idToken = request.session['uid']
        if (idToken):
            return render(request, 'faceRecognition.html')
    except:
        message = "Please Login To Continue"
        return render(request, 'signIn.html', {"message": message})


def forgotPassword(request):
    return render(request, "forgotPassword.html")
