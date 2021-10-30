from django.shortcuts import render,redirect
from django.http import HttpResponse
# import for user registration form
from  django.contrib.auth.forms import UserCreationForm
# from .forms import ClientRegisterForm,contactForm
from .forms import *
from django.contrib import messages
# login imports
from django.contrib.auth import authenticate, login, logout

#import for restricting access to pages
from django.contrib.auth.decorators import login_required

# import for creating a group
from django.contrib.auth.models import Group

# import models
from .models import Client

#custom decorator
from .decorators import unauthenticated_user, allowed_users,admin_only
# import transactions
from django.db import transaction

# for migration
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# register a client with group
@unauthenticated_user
def register(request):
    # redirect authenticated user to the dashboard
    form = ClientRegisterForm()
    if request.method == 'POST':
        
        with transaction.atomic():
            
            form  = ClientRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                #getting username from form
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                # associate user with admin
                group = Group.objects.get(name='admin')
                user.groups.add(group)

                # attach a profile to a client
                Client.objects.create(
                user = user,
                )
            
                # attach a profile to a student
                StudObj = Student.objects.create(
                user = user,
                email=email,
                client = Client.objects.get(pk=1),
                createdby=user
                )
                StudObj.save()

                messages.success(request, 'Account creation successful for ' + username)
                return redirect('login')

    context={'form': form}

    return render (request,'accounts/register.html',context)


# register user with out group
# @unauthenticated_user
# def registerPage(request):
#     #redirect authenticated user to the dashboard
#     form = ClientRegisterForm()
#     if request.method == 'POST':
#         form  = ClientRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             #getting username from form
#             user = form.cleaned_data.get('username')
#             messages.success(request, 'Account creation successful for ' + user)
#             return redirect('login')

#     context={'form': form}

#     return render (request,'accounts/register.html',{'form':form})

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('admin')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request,'accounts/login.html')

    return render(request,'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def admin(request):
   
    students = Student.objects.filter(reg_no__isnull=True)
    context = {'students':students}
    return render(request,'accounts/admin.html',context)
