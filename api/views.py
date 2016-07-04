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

#### Global ####
def loginCheck(request,user_uid):
    ####################################################
    # Description: Check if user is logged in by session
    #
    # arg0: request   {object}
    # arg1:  user_uid  {string}
    ####################################################

    if request.session.get('user_id', user_uid):
        #Get User model
        user = User.objects.filter(uid=str(user_uid))[0]

        #Respond
        return user
    else:
        #Redirect to login
        return redirect(index(request))

def respondSuccess():
    response = {
        'status': "success"
    }
    return HttpResponse(json.dumps(response))

def respondFail():
    response = {
        'status': "fail"
    }
    return HttpResponse(json.dumps(response))

#### Ajax ####
def registerUser(request):
    ################################################
    # Description: Creates a new 'User' model object
    #
    # arg0: request   {object}
    ################################################

    #Declare Vars
    username = str(request.POST['username'])
    email = str(request.POST['email'])
    password = str(request.POST['password'])
    print("username="+username+"\nemail="+email+"\npassword="+password)

    #Check to see if username taken
    username_check = User.objects.filter(username=username)

    #Check to see if email is already in system
    email_check = User.objects.filter(login_email=email)

    if len(username_check) != 0:
        #Respond with failure
        print("register failed: username_error")
        response = {
            'status': "fail",
            'error': "username_error",
            'error_message': "Username taken"
        }
    elif len(email_check) != 0:
        #Respond with failure
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

        #Respond success
        response = {
            'status': "success",
            'user_id': str(new_user.uid)
        }

    return HttpResponse(json.dumps(response))

def loginAjax(request):
    ##########################################################
    # Description: Checks validity of email password POST body
    # elements then adds user uid to sessions
    #
    # arg0: request   {object}
    ##########################################################

    #Declare Vars
    email = str(request.POST['email'])
    password = str(request.POST['password'])

    #Cehck for email in system
    email_check = User.objects.filter(login_email=email)

    # Hash Password
    h = hashlib.md5()
    h.update(password)

    #User Check
    if len(email_check) == 0:
        #Respond Failure
        print("login failed: email_error")
        response = {
            'status': "fail",
            'error': "email_error",
            'error_message': "Email not in system"
        }
        return HttpResponse(json.dumps(response))
    else:
        #Set User model object
        user = email_check[0]

    #Password Check
    if str(user.password) == h.hexdigest():
        #Check Email Verified
        if user.email_verified == False:
            #Respond with Failure
            response = {
                'status': "fail",
                'error': "verification_error",
                'error_message': "Email verification needed"
            }
            return HttpResponse(json.dumps(response))

        #Set Session
        request.session['user_id'] = str(user.uid)

        #Update User Data
        user.last_login = timezone.now()
        user.save()

        #Respond with success
        print("login success")
        response = {
            'status': "success",
            'user_id': str(user.uid)
        }

        return HttpResponse(json.dumps(response))
    else:
        #Respond with Failure
        print("login fail: password error")
        response = {
            'status': "fail",
            'error': "password_error",
            'error_message': "Password Incorrect"
        }
        return HttpResponse(json.dumps(response))

def addMainGroup(request):
    #####################################################
    # Description: Creates a new 'MainGroup' model object
    #
    # arg0: request   {object}
    ####################################################

    #Declare Vars
    name = str(request.POST['name'])
    user_id = str(request.session.get('user_id'))
    user = User.objects.filter(uid=user_id)[0]
    print(str(user.username))

    #Create new group
    new_group = MainGroup(name=name,user=user)
    new_group.save()

    #Respond success
    return respondSuccess()

def getServices(request):
    #######################################################################
    # Description: Returns back Service models base upon responsinilty type
    #
    # arg0: request   {object}
    ########################################################################

    #Declare Vars
    responsibility_type_id = str(request.POST['type_id'])
    print(responsibility_type_id)
    responsibility_type = ResponsibilityType.objects.get(pk=responsibility_type_id)
    services_formatted = []
    services_raw = Service.objects.filter(type=responsibility_type).values('id', 'name', 'logo_image_url')
    print(services_raw)


    #Respond success
    if len(services_raw) != 0:
        for service in services_raw:
            services_formatted.append(service)

        response = {
            'status': "success",
            'services': services_formatted
        }
        return HttpResponse(json.dumps(response))
    #Respond Failure
    else:
        return respondFail()

def getServiceOptions(request):
    ###########################################
    # Description: Returns back Service options
    #
    # arg0: request   {object}
    ###########################################

    # Declare Vars
    service_id = str(request.POST['service_id'])
    service = Service.objects.get(pk=service_id)
    print(str(service.name))
    user_id = str(request.session.get('user_id'))
    user = User.objects.filter(uid=user_id)[0]
    print(str(user.username))

    #Get Options
    options_raw = service.options.all().values('id', 'name')
    print(options_raw)

    #Format Options to json
    options = []
    for option in options_raw:
        options.append(option)

    #respond
    response = {
        'status': "success",
        'options': options
    }
    return HttpResponse(json.dumps(response))

def getOptionInputs(request):
    ###########################################################
    # Description: Returns back required inputs for option form
    #
    # arg0: request   {object}
    ###########################################################

    # Declare Vars
    option_id = str(request.POST['option_id'])
    option = ServiceOption.objects.get(pk=option_id)
    print(str(option.name))

    #Get Inputs
    inputs_raw = option.inputs.all()
    print(inputs_raw)

    #Format Inputs to json
    inputs = []
    for input in inputs_raw:
        #Construct Html
        name = str(input.name)
        input_type = str(input.input_type)
        placeholder = str(input.placeholder)
        value_one = str(input.value_one)
        value_two = str(input.value_two)

        #Set up single input
        if input_type != "radio" and input_type != "checkbox":
            output_html = "<input name='" + name + "' type='" + input_type + "' "
        else:
            #Else setup double input for radio and checkbox
            output_1 = "<input name='" + name + "' type='" + input_type + "' "
            output_2 = "<input name='" + name + "' type='" + input_type + "' "
            response = {
                'status': "success",
                'input_html': output_1 + output_2
            }
            return HttpResponse(json.dumps(response))
        #Add in placeholder
        if placeholder != '':
            output_html += "placeholder='" + placeholder + "' "

        #Add values to checkbox/radios inputs
        if value_one != '':
            output_html  += "value='" + value_one + "' "
            inputs.append(output_html)

        if value_two != '':
            output_html += "value='" + value_two + "' "
            inputs.append(output_html)

        output_html += "/>"

        inputs.append(output_html)

    #respond
    response = {
        'status': "success",
        'input_html': inputs,
        'map_required': str(option.map_required)
    }
    print("map required="+str(option.map_required))
    return HttpResponse(json.dumps(response))



#### API #####
def emailVerification(request,user_uid):
    ##############################################
    # Description: Verifies a users email is valid
    #
    # arg0: request   {object}
    # arg1:  user_uid  {string}
    ##############################################
    user_check = User.objects.filter(uid=str(user_uid))
    if len(user_check) != 0:
        user = user_check[0]
        user.email_verified = True
        user.save()
        data = {
            'page': "index",
        }
        # Render Page
        return render(request, 'desktop/index.html', data)



#### Page Rendering ####
def index(request):
    #########################################
    # Description: Renders the home page html
    #
    # arg0: request   {object}
    #########################################
    #Declare Vars
    print("index(request):init")
    #Page Data
    data = {
        'page': "index",
    }
    #Render Page
    return render(request,'desktop/index.html',data)

def dashboard(request,user_uid):
    ###############################################
    # Description: Renders the dashboard page html
    #
    # arg0: request   {object}
    # arg1:  user_uid  {string}
    ###############################################
    #Declare Vars
    print("dashboard(request):init")
    user = loginCheck(request,user_uid)
    main_groups = MainGroup.objects.filter(user=user)
    #Page Data
    data = {
        'page': "dashboard",
        'user': user,
        'mainGroups': main_groups
    }
    #Render Page
    return render(request,'desktop/dashboard.html',data)

def profile(request,user_uid):
    ############################################
    # Description: Renders the profile page html
    #
    # arg0: request   {object}
    # arg1:  user_uid  {string}
    ############################################
    #Declare Vars
    print("dashboard(request):init")
    user = loginCheck(request, user_uid)
    #Page Data
    data = {
        'page': "profile",
        'user': user
    }
    #Render Page
    return render(request,'desktop/profile.html',data)

def groupPage(request,group_id):
    ####################################################
    # Description: Renders the dashboard group page html
    #
    # arg0: request   {object}
    # arg1:  group_uid  {string}
    ####################################################
    #Declare Vars
    #Gather info for page
    user_id = str(request.session.get('user_id'))
    user = User.objects.filter(uid=user_id)[0]
    group = MainGroup.objects.get(id=group_id)
    main_groups = MainGroup.objects.filter(user=user)
    types = ResponsibilityType.objects.all()

    #Page Data
    data = {
        'page': "group",
        'user': user,
        'group': group,
        'mainGroups': main_groups,
        'types': types
    }

    #Render Page
    return render(request, 'desktop/group.html', data)
