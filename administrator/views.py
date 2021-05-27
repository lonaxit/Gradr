from django.shortcuts import render,redirect

from django.http import HttpResponse
# import for user registration form
from  django.contrib.auth.forms import UserCreationForm
from accounts.forms import ClientRegisterForm, contactForm, ClientForm
# from administrator.forms import TermForm,SessionForm
from administrator.forms import *
from django.contrib import messages
#import for restricting access to pages
from django.contrib.auth.decorators import login_required

# import for creating a group
from django.contrib.auth.models import Group

# import models
from accounts.models import Client
from .models import *

#custom decorator
from accounts.decorators import unauthenticated_user,allowed_users,admin_only



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createClient(request):
    user = request.user
    ClientProfile  = Client.objects.get(user_id=user.id)
    form = ClientForm(instance=user)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # form.save()
            ClientProfile.profile_image = form.cleaned_data.get('profile_image')
            ClientProfile.address = form.cleaned_data.get('address')
            ClientProfile.school_type = form.cleaned_data.get('school_type')
            ClientProfile.school_name = form.cleaned_data.get('school_name')
            ClientProfile.phone = form.cleaned_data.get('phone')
            ClientProfile.email = form.cleaned_data.get('email')
            ClientProfile.save()
            messages.success(request, 'Institution profile  created successfully')
            return redirect('admin-setting')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('admin-setting')
    context = {'form':form}
    return render(request, 'admin/client-setting.html',context)


# create a new term
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addTerm(request):
    client = Client.objects.get(user_id=request.user.id)
    form = TermForm()
    context = {}
    if request.method == "POST":

        form = TermForm(request.POST)
        if form.is_valid():
            term = form.cleaned_data.get("term")
            client = client
            obj = Term.objects.create(
                                 term = term,
                                 client = client
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('create-term')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('create-term')
    context={'form':form}
    return render(request, "admin/addTerm.html", context)


# add session
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addSession(request):
    client = Client.objects.get(user_id=request.user.id)
    form = SessionForm()
    context = {}
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.cleaned_data.get("session")
            client = client
            obj = Session.objects.create(
                                 session = session,
                                 client = client
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('add-session')
        else:
            messages.success(request, 'oops! something went wrong')
            return redirect('add-session')
    context={'form':form}
    return render(request, "admin/addSession.html", context)


# Add class
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addClass(request):
    client = Client.objects.get(user_id=request.user.id)
    form = ClassForm()
    context = {}
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():

            classname = form.cleaned_data.get("class_name")
            client = client
            obj = StudentClass.objects.create(
                                 class_name = classname,
                                 client = client
                                     )
            obj.save()

            messages.success(request, 'Record added')
            return redirect('add-class')
        else:

            messages.success(request, 'oops! something went wrong')
            return redirect('add-class')
    context={'form':form}
    return render(request, "admin/addClass.html", context)


# add subject
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addSubject(request):
    client = Client.objects.get(user_id=request.user.id)
    form = SubjectForm()
    context = {}
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            client = client
            obj = Subject.objects.create(
                                 subject = subject,
                                 client = client
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('add-subject')
        else:
            messages.success(request, 'oops! something went wrong')
            return redirect('add-session')
    context={'form':form}
    return render(request, "admin/addSubject.html", context)


# client profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def profile(request):
    context ={}
    terms = Term.objects.all()
    classlist = StudentClass.objects.all()[:3]
    sessions = Session.objects.all()[:3]
    subjects = Subject.objects.all()[:3]

    context ={
    'terms':terms,
    'classlist':classlist,
    'sessions':sessions,
    'subjects':subjects
    }

    return render(request, 'admin/client-profile.html',context)


# register user with group
@unauthenticated_user
def register(request):
    # redirect authenticated user to the dashboard


    form = ClientRegisterForm()
    if request.method == 'POST':
        form  = ClientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #getting username from form
            username = form.cleaned_data.get('username')
            # associate user with admin
            group = Group.objects.get(name='admin')
            user.groups.add(group)

            # attach a profile to a client
            Client.objects.create(
                user = user,
            )

            messages.success(request, 'Account creation successful for ' + username)
            return redirect('login')

    context={'form': form}

    return render (request,'accounts/register.html',{'form':form})




#
# register user with out group
@unauthenticated_user
def registerPage(request):
    #redirect authenticated user to the dashboard
    form = ClientRegisterForm()
    if request.method == 'POST':
        form  = ClientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #getting username from form
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account creation successful for ' + user)
            return redirect('login')

    context={'form': form}

    return render (request,'accounts/register.html',{'form':form})
