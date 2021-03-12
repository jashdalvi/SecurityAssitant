from django.shortcuts import render, redirect


def signIn(request):
    return render(request, 'signIn.html')
