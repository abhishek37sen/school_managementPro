from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from school_managementapp.EmailBackEnd import EmailBackEnd


def home(request):
    return render(request,'index.html')

def showlogin(request):
    return render(request,'login.html')


def dologin(request):
    if request.method !="POST":
        return HttpResponse("<h2>Method NOt Allowed<h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type == "1":
                return HttpResponseRedirect('admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect('staff_home')
            elif user.user_type == "3":
                return HttpResponseRedirect('student_home')
            else:
                return render(request,'login.html',{'error_message':"Invalid Login Details.."})
        else:
            return render(request, 'login.html', {"error_message": "Invalid Login Details.."})


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.username+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')






