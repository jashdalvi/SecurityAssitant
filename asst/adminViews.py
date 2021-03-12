from django.shortcuts import render


def adminDashboard(request):
    if request.method == 'POST':
        adminEmail = request.POST.get('adminEmail')
        adminPassword = request.POST.get('adminPassword')
        print(" adminEmail : ", adminEmail)
        print(" adminPassword : ", adminPassword)
        return render(request, 'adminDashboard.html')
    return render(request, 'adminDashboard.html')


def userRegistration(request):
    return render(request, 'userRegistration.html')


def postUserRegistration(request):
    if request.method == 'POST':
        userName = request.POST.get('userName')
        phoneNumber = request.POST.get('phoneNumber')
        userEmail = request.POST.get('userEmail')
        userPassword = request.POST.get('userPassword')
        buildingAssigned = request.POST.get('buildingAssigned')
        print(" userName : ", userName)
        print(" phoneNumber : ", phoneNumber)
        print(" userEmail : ", userEmail)
        print(" userPassword : ", userPassword)
        print(" buildingAssigned : ", buildingAssigned)
        return render(request, 'adminDashboard.html')
    return render(request, 'userRegistration.html')


def users(request):
    return render(request, 'users.html')


def adminReports(request):
    return render(request, 'adminReports.html')
