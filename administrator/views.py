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

# update client
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateClient(request,pk):
    # user = request.user
    ClientProfile  = Client.objects.get(user_id=pk)
    form = ClientForm(instance=ClientProfile)
    context = {'form':form}
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=ClientProfile)
        if form.is_valid():
            form.save()

            messages.success(request, 'Institution profile  updated  successfully')
            return redirect('admin-profile')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('update-profile')
    context = {'form':form}
    return render(request, 'admin/updateClient.html',context)

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

# Edit term

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def editTerm(request,pk):

    term = Term.objects.get(id=pk)
    form = TermForm(instance=term)
    context = {'form':form}
    if request.method == "POST":

        form = TermForm(request.POST,instance=term)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated')
            return redirect('admin-profile')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('update-term')
    context={'form':form}
    return render(request, "admin/editTerm.html", context)

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


# all sessions
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def allSessions(request):
    sessions = Session.objects.all()
    context = {'sessions':sessions}
    return render(request, "admin/list-sessions.html", context)
# update session
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateSession(request,pk):
    session = Session.objects.get(id=pk)
    form = SessionForm(instance=session)
    context = {'form': form}
    if request.method == 'POST':
        form = SessionForm(request.POST,instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Session updated')
            return redirect('admin-profile')
        else:
            messages.success(request, 'oops! something went wrong')
            return redirect('update-session')
    # context={'form':form}
    return render(request, "admin/editSession.html", context)


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


# update class
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateClass(request,pk):
    classobj = StudentClass.objects.get(id=pk)
    form = ClassForm(instance=classobj)
    context = {'form':form}
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=classobj)
        if form.is_valid():
            form.save()


            messages.success(request, 'Class updated')
            return redirect('admin-profile')
        else:

            messages.success(request, 'oops! something went wrong')
            return redirect('update-class')
    context={'form':form}
    return render(request, "admin/updateClass.html", context)

# all classes
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def allClasses(request):
    listClass = StudentClass.objects.all()
    context = {'listClass':listClass}
    return render(request, "admin/list-classes.html", context)


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
            return redirect('add-subject')
    context={'form':form}
    return render(request, "admin/addSubject.html", context)


# update subject
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateSubject(request,pk):
    subject = Subject.objects.get(id=pk)
    form = SubjectForm(instance=subject)
    context = {'form':form}
    if request.method == 'POST':
        form = SubjectForm(request.POST,instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated')
            return redirect('admin-profile')
        else:
            messages.success(request, 'oops! something went wrong')
            return redirect('update-subject')
    context={'form':form}
    return render(request, "admin/updateSubject.html", context)


# all subjects
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def allSubjects(request):
    subjects = Subject.objects.all()
    context = {'subjects':subjects}
    return render(request, "admin/list-subjects.html", context)





# add attendance settings
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def attendance_settings(request):
    client = Client.objects.get(user_id=request.user.id)
    form = AttendanceSettingForm()
    context = {}
    if request.method == 'POST':
        form = AttendanceSettingForm(request.POST)
        if form.is_valid():

            daysopen = request.POST['days_open']
            daysclosed = request.POST['days_closed']
            term = request.POST['term']
            session = request.POST['session']

            obj = AttendanceSetting.objects.create(
                                 days_open = daysopen,
                                 days_closed =daysclosed,
                                 term_id=term,
                                 session_id=session,
                                 client = client
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('attendance-setting')
        else:
            messages.success(request, 'oops! something went wrong')
            return redirect('attendance-setting')
    context={'form':form}
    return render(request, "admin/add_attendance_setting.html", context)


# resumption date setting
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def resumption_settings(request):
    client = Client.objects.get(user_id=request.user.id)
    form = ResumptionSettingForm()
    context={'form':form}
    if request.method == 'POST':
        form = ResumptionSettingForm(request.POST)
        if form.is_valid():
            # resumption = form.save(commit=False)
            # resumption.client_id = client.id
            # resumption.save()

            term_begins = request.POST['term_begins']
            term_ends = request.POST['term_ends']

            term = request.POST['term']
            session = request.POST['session']

            obj = ResumptionSetting.objects.create(
                                 term_begins = term_begins,
                                 term_ends =term_ends,
                                 term_id=term,
                                 session_id=session,
                                 client = client
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('admin-profile')
        else:
            # print('shhhh')
            messages.success(request, 'oops! something went wrong')
            return redirect('resumption-setting')

    return render(request, "admin/resumption_settings.html", context)


# update resumption dates
# update subject
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateResumption(request,pk):
    resumption = ResumptionSetting.objects.get(id=pk)
    form = ResumptionSettingForm(instance=resumption)
    context = {'form':form}
    if request.method == 'POST':
        form = ResumptionSettingForm(request.POST,instance=resumption)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resumption date updated')
            return redirect('admin-profile')
        else:
            messages.success(request, 'oops! something went wrong')
            return redirect('update-resumption')
    context={'form':form}
    return render(request, "admin/updateResumption.html", context)


# all resumption dates
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def resumptionDates(request):
    resumption = ResumptionSetting.objects.all()
    context = {'resumption':resumption}
    return render(request, "admin/list_resumption.html", context)




# client profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def profile(request):
    context ={}
    terms = Term.objects.all()
    classlist = StudentClass.objects.all()[:3]
    sessions = Session.objects.all()[:3]
    subjects = Subject.objects.all()[:3]
    subjects = Subject.objects.all()[:3]
    resumption = ResumptionSetting.objects.all()
    # active settings
    term = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    # attendance = AttendanceSetting.objects.filter(term_id=term.id)


    context ={
    'terms':terms,
    'classlist':classlist,
    'sessions':sessions,
    'subjects':subjects,
    # 'attendance':attendance,
    'activeTerm':term,
    'activeSession':activeSession,
    'resumption':resumption
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
