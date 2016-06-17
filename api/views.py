__author__ = 'christian.cecilia1@gmail.com'
##### imported modules #####
import os
import json
import datetime
import urllib
import string
import hashlib
import re
from random import choice, randint
import datetime

###### Django modules #####
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils import timezone

##### From Project #####
from .models import *


#### Ajax ####
def registerUser(request):
    username = str(request.POST['username'])
    email = str(request.POST['email'])
    password = str(request.POST['password'])
    print("username="+username+"\nemail="+email+"\npassword="+password)
    username_check = User.objects.filter(username=username)
    email_check = User.objects.filter(login_email=email)

    if len(username_check) != 0:
        print("register failed: username_error")
        response = {
            'status': "fail",
            'error': "username_error",
            'error_message': "Username taken"
        }
    elif len(email_check) != 0:
        print("register failed: email_error")
        response = {
            'status': "fail",
            'error': "email_error",
            'error_message': "Email already exists"
        }
    else:
        # Hash Password
        h = hashlib.md5()
        h.update(password)

        #Create User
        new_user = User(username=username, login_email=email, password=h.hexdigest())
        new_user.save()
        print("registered new user")

        # Send Welcome Email
        body = open('templates/email/welcome.html', 'r+')
        body = body.read()
        body = string.replace(body, "{{ email }}", str(new_user.login_email))
        body = string.replace(body, "{{ password }}", str(password))
        email = EmailMessage("Responsibility", body, "noreply@responsibility.com", [str(new_user.login_email)])
        email.content_subtype = "html"
        email.send()
        print("welcome email sent")

        #Set Session
        request.session['user_id'] = str(new_user.uid)

        response = {
            'status': "success",
            'user_id': str(new_user.uid)
        }

    return HttpResponse(json.dumps(response))

def loginAjax(request):
    email = str(request.POST['email'])
    password = str(request.POST['password'])

    email_check = User.objects.filter(login_email=email)

    # Hash Password
    h = hashlib.md5()
    h.update(password)

    #User Check
    if len(email_check) == 0:
        print("login failed: email_error")
        response = {
            'status': "fail",
            'error': "email_error",
            'error_message': "Email not in system"
        }
        return HttpResponse(json.dumps(response))
    else:
        user = email_check[0]

    #Password Check
    if str(user.password) == h.hexdigest():
        #Set Session
        request.session['user_id'] = str(new_user.uid)

        #Update User Data
        user.last_login = timezone.now()
        user.save()

        print("login success")
        return redirect(dashboard(request,str(user.uid)))
    else:
        print("login fail: password error")
        response = {
            'status': "fail",
            'error': "password_error",
            'error_message': "Password Incorrect"
        }
        return HttpResponse(json.dumps(response))




#### Page Rendering ####
def index(request):
    #Declare Vars
    print("index(request):init")
    #Page Data
    data = {
        'page': "index",
    }
    #Render Page
    return render(request,'desktop/index.html',data)

def dashboard(request,user_uid):
    #Declare Vars
    print("dashboard(request):init")
    if request.session.get('user_id', user_uid):
        user = User.objects.filter(uid=str(user_uid))[0]
        #Page Data
        data = {
            'page': "dashboard",
            'user': user
        }
        #Render Page
        return render(request,'desktop/dashboard.html',data)
    else:
        return redirect(index(request))