"""asst URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views, userViews, adminViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signIn, name="signIn"),
    path('postVisitorRegistration', userViews.postVisitorRegistration,
         name="postVisitorRegistration"),
    path('userDashboard', userViews.userDashboard, name="userDashboard"),
    path('visitorRegistration', userViews.visitorRegistration,
         name="visitorRegistration"),
    path('userReports', userViews.userReports, name="userReports"),
    path('adminDashboard', adminViews.adminDashboard, name="adminDashboard"),
    path('userRegistration', adminViews.userRegistration,
         name="userRegistration"),
    path('postUserRegistration', adminViews.postUserRegistration,
         name="postUserRegistration"),
    path('users', adminViews.users, name="users"),
    path('adminReports', adminViews.adminReports, name="adminReports"),
    path('faceRecognition', userViews.faceRecognition, name='faceRecognition'),
    path('facecam_feed', userViews.facecam_feed, name='facecam_feed'),
    path('temperature_feed',userViews.temperature_feed, name="temperature_feed"),
    path('createReport', userViews.createVisitorReport, name="createReport"),
    path('recordVisitorTemperature', userViews.recordVisitorTemperature,
         name="recordVisitorTemperature")
]
