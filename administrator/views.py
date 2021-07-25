from django.shortcuts import render,redirect

from django.http import HttpResponse,JsonResponse
# import for user registration form
from  django.contrib.auth.forms import UserCreationForm
# from accounts.forms import ClientRegisterForm, contactForm, ClientForm,StudentRegisterForm
from accounts.forms import *
# from administrator.forms import TermForm,SessionForm
from administrator.forms import *
from django.contrib import messages
#import for restricting access to pages
from django.contrib.auth.decorators import login_required

# import for creating a group
from django.contrib.auth.models import Group

# import models
from accounts.models import *
from .models import *
from django.db.models import Q

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


# sign up new a student user
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def newStudent(request): 
    # redirect authenticated user to the dashboard
    form = StudentRegisterForm()
    logged_inuser = request.user
    clientProfile  = Client.objects.get(user_id=logged_inuser.id)
    context={'form': form}
    if request.method == 'POST':
        form  = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #getting username from form
            username = form.cleaned_data.get('username')
            # associate user with admin
            group = Group.objects.get(name='student')
            user.groups.add(group)

            # attach a profile to a client
            Student.objects.create(
                user = user,
                client = clientProfile,
            )

            messages.success(request, 'Student account creation successful for ' + username + ',  please update the profile')
            return redirect('update-student',pk=user.id)

    return render (request,'admin/newStudent.html',{'form':form})



# update student profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateStudentProfile(request,pk):
    user = request.user
    ClientProfile  = Client.objects.get(user_id=user.id)
    student  = Student.objects.get(user_id=pk)
    form = StudentProfileForm(instance=student)
    # form = StudentProfileForm()
    context = {'form':form}
    if request.method == 'POST':
        form = StudentProfileForm(request.POST,request.FILES, instance=student)
        if form.is_valid():
            form.save()

            messages.success(request, 'Student profile  modification/creation was  successful')
            return redirect('view-student',pk=pk)
        else:

            messages.success(request, 'Something went wrong')
            return redirect('update-student',pk=pk)

    return render(request, 'admin/updateStudentProfile.html',context)

# list all students
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listStudents(request):
    students = Student.objects.all()
    context = {'students':students}
    return render(request, "admin/list_students.html", context)


# sign up new a teacher user
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def newTeacher(request):
    # redirect authenticated user to the dashboard
    form = StaffRegisterForm()
    logged_inuser = request.user
    clientProfile  = Client.objects.get(user_id=logged_inuser.id)
    context={'form': form}
    if request.method == 'POST':
        form  = StaffRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #getting username from form
            username = form.cleaned_data.get('username')
            # associate user with admin
            group = Group.objects.get(name='teacher')
            user.groups.add(group)

            # attach a profile to a client
            Teacher.objects.create(
                user = user,
                client = clientProfile,
            )

            messages.success(request, 'Account creation successful for ' + username + ',  please update the profile')
            return redirect('update-teacher',pk=user.id)

    return render (request,'admin/newTeacher.html',{'form':form})

# update teacher profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateTeacherProfile(request,pk):
    user = request.user
    # ClientProfile  = Client.objects.get(user_id=user.id)
    teacher  = Teacher.objects.get(user_id=pk)
    form = TeacherProfileForm(instance=teacher)
    # form = StudentProfileForm
    context = {'form':form}
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST,request.FILES, instance=teacher)
        if form.is_valid():
            form.save()

            messages.success(request, 'Teacher profile  modification/creation was  successful')
            return redirect('view-teacher',pk=pk)
        else:

            messages.success(request, 'Something went wrong')
            return redirect('update-teacher',pk=pk)

    return render(request, 'admin/updateTeacherProfile.html',context)


# student profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewTeacher(request,pk):
    context ={}
    teacher = Teacher.objects.get(user_id=pk)

    context ={
    'teacher':teacher,
    }

    return render(request, 'admin/view_teacher.html',context)


# list teacher
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listTeacher(request):
    teacher = Teacher.objects.all()
    context = {'teacher':teacher}
    return render(request, "admin/list_teachers.html", context)


# assign subject to teacher
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def assignSubject(request):
    form = AssignSubjectForm()
    context = {'form':form}
    client = Client.objects.get(user_id=request.user.id)
    if request.method == "POST":
        form = AssignSubjectForm(request.POST)
        if form.is_valid():
            teacher = request.POST["teacher"]
            classroom = request.POST["classroom"]
            subject = request.POST["subject"]

            # #
            teacherObj = Teacher.objects.get(id=teacher)
            subjectObj = Subject.objects.get(id=subject)
            classroomObj = StudentClass.objects.get(id=classroom)
            result = SubjectTeacher.objects.filter(Q(teacher=teacherObj) & Q(classroom=classroomObj)
            & Q(subject=subjectObj))

            if result:

                 messages.error(request, 'Unable to assign subject teacher, check the deails')
                 return redirect('assign-subject')
            else:


                obj = SubjectTeacher.objects.create(
                                     teacher = teacherObj,
                                     classroom = classroomObj,
                                     subject = subjectObj,
                                     client = client
                                         )
                obj.save()
                messages.success(request, 'Subject successfully assigned')
                return redirect('assign-subject')
    return render(request, "admin/assign_subject.html", context)

# update subject assinged to teacher
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateSubjectTeacher(request,pk):
    subjectTeacher = SubjectTeacher.objects.get(id=pk)
    form = AssignSubjectForm(instance=subjectTeacher)
    context = {'form':form}
    client = Client.objects.get(user_id=request.user.id)
    if request.method == "POST":
        form = AssignSubjectForm(request.POST,instance=subjectTeacher)
        if form.is_valid():
            # print('valid')
            teacher = request.POST["teacher"]
            classroom = request.POST["classroom"]
            subject = request.POST["subject"]

            # #
            teacherObj = Teacher.objects.get(id=teacher)
            subjectObj = Subject.objects.get(id=subject)
            classroomObj = StudentClass.objects.get(id=classroom)
            result = SubjectTeacher.objects.filter(Q(teacher=teacherObj) & Q(subject=subjectObj)
            | Q(classroom=classroomObj) & Q(subject=subjectObj))

            # result = SubjectTeacher.objects.filter(Q(teacher=teacherObj) & Q(classroom=classroomObj)
            # | Q(classroom=classroomObj) & Q(subject=subjectObj))

            if result:
                 messages.error(request, 'Unable to update record, check for details')
                 return redirect('update-subject-teacher',pk=pk)
            else:
                form.save()
                messages.success(request, 'Record updated successfully')
                return redirect('list-subject-teachers')
    return render(request, "admin/assign_subject.html", context)



# list subejct teachers
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listSubjectTeachers(request):
    records = SubjectTeacher.objects.all()
    context = {'records':records}
    return render(request, "admin/all_subject_teachers.html", context)

# assign class teacher
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def assignClassTeacher(request):
    form = AssignClassTeacherForm()
    context = {'form':form}
    client = Client.objects.get(user_id=request.user.id)
    if request.method == "POST":
        form = AssignClassTeacherForm(request.POST)
        if form.is_valid():
            # form.save()
            teacher = request.POST["teacher"]
            classroom = request.POST["classroom"]
            session = request.POST["session"]
            term = request.POST["term"]

            # #
            teacherObj = Teacher.objects.get(id=teacher)
            sessionObj = Session.objects.get(id=session)
            termObj = Term.objects.get(id=term)
            classroomObj = StudentClass.objects.get(id=classroom)
            result = ClassTeacher.objects.filter(Q(teacher=teacherObj) & Q(classroom=classroomObj))

            if result:

                 messages.error(request, 'Record already exist')
                 return redirect('assign-class-teacher')
            else:

                obj = ClassTeacher.objects.create(
                                     teacher = teacherObj,
                                     classroom = classroomObj,
                                     session =sessionObj,
                                     term = termObj,
                                     client = client
                                         )
                obj.save()
                messages.success(request, 'Class teacher  successfully assigned')
                return redirect('assign-class-teacher')
    return render(request, "admin/assign_class_teacher.html", context)

# update class teacher
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateClassTeacher(request,pk):
    classTeacher = ClassTeacher.objects.get(id=pk)
    form = AssignClassTeacherForm(instance=classTeacher)
    context = {'form':form}

    if request.method == "POST":
        form = AssignClassTeacherForm(request.POST,instance=classTeacher)
        if form.is_valid():
            # form.save()
            teacher = request.POST["teacher"]
            classroom = request.POST["classroom"]
            session = request.POST["session"]
            term = request.POST["term"]

            # #
            teacherObj = Teacher.objects.get(id=teacher)
            sessionObj = Session.objects.get(id=session)
            termObj = Term.objects.get(id=term)
            classroomObj = StudentClass.objects.get(id=classroom)
            result = ClassTeacher.objects.filter(Q(teacher=teacherObj) & Q(classroom=classroomObj))

            if result:

                 messages.error(request, 'Record already exist')
                 return redirect('update-class-teacher',pk=pk)
            else:
                form.save()

                # obj = ClassTeacher.objects.create(
                #                      teacher = teacherObj,
                #                      classroom = classroomObj,
                #                      session =sessionObj,
                #                      term = termObj,
                #                      client = client
                #                          )
                # obj.save()
                messages.success(request, 'Class teacher updated successfully')
                return redirect('list-class-teacher')
    return render(request, "admin/assign_class_teacher.html", context)


# list class teachers
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listClassTeacher(request):
    records = ClassTeacher.objects.all()
    context = {'records':records}
    return render(request, "admin/list_class_teacher.html", context)

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


# add subject per class
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def subjectPerClass(request):
    client = Client.objects.get(user_id=request.user.id)
    form = SubjectPerClassForm()
    context={'form':form}
    if request.method == "POST":

        form = SubjectPerClassForm(request.POST)
        if form.is_valid():

            sch_class = form.cleaned_data.get("sch_class")
            no_subject = form.cleaned_data.get("no_subject")

            obj = SubjectPerClass.objects.create(
                                 sch_class = sch_class,
                                 no_subject = no_subject,
                                 client = client
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('subject-perclass')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('subject-perclass')

    return render(request, "admin/subjectperclass.html", context)


# list subject per class
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listSubjectPerClass(request):
    subjectsInClass = SubjectPerClass.objects.all()
    context = {'subjectsInClass':subjectsInClass}
    return render(request, "admin/subjectsperclass_list.html", context)


# update subjects in class

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateSubjectPerClass(request,pk):
    subjectsInClass = SubjectPerClass.objects.get(id=pk)
    form = SubjectPerClassForm(instance=subjectsInClass)
    context={'form':form}
    if request.method == "POST":

        form = SubjectPerClassForm(request.POST,instance=subjectsInClass)
        if form.is_valid():
            form.save()

            # sch_class = form.cleaned_data.get("sch_class")
            # no_subject = form.cleaned_data.get("no_subject")
            #
            # obj = SubjectPerClass.objects.create(
            #                      sch_class = sch_class,
            #                      no_subject = no_subject,
            #                      client = client
            #                          )
            # obj.save()
            messages.success(request, 'Record updated!')
            return redirect('subject-perclass-list')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('update=subject-perclass-list')

    return render(request, "admin/updateSubjPerClass.html", context)



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
            return redirect('all-classes')
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
    # subjects = Subject.objects.all()[:3]
    resumption = ResumptionSetting.objects.all()
    # active settings
    term = Term.objects.all()[:3]
    # activeSession = Session.objects.all()[:3]
    attendance = AttendanceSetting.objects.all()[:3]
    # attendance = AttendanceSetting.objects.filter(term_id=term.id)


    context ={
    'terms':terms,
    'classlist':classlist,
    'sessions':sessions,
    'subjects':subjects,
    'attendance':attendance,
    'activeTerm':term,
    # 'activeSession':activeSession,
    'resumption':resumption
    }

    return render(request, 'admin/client-profile.html',context)


# student profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewStudent(request,pk):
    context ={}
    student = Student.objects.get(user_id=pk)

    context ={
    'student':student,
    }

    return render(request, 'admin/view_student_profile.html',context)


# admission list
# student profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admissionList(request):
    form = AdmissionListForm()
    # context ={'form':form}
    if request.method == 'POST':
        form = AdmissionListForm(request.POST)
        if form.is_valid():
            term = Term.objects.get(id=request.POST['term'])
            session = Session.objects.get(id=request.POST['session'])

            # select students based on search parameter
            result = Student.objects.filter(Q(session_admitted=session) & Q(term_admitted=term))

            return redirect('admin-profile')
        else:
            # print('shhhh')
            messages.error(request, 'oops! something went wrong')
            return redirect('admission-list')
        context ={'form':form}

    return render(request, 'admin/filter_admission_list.html',context)

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


# get state data via json
def get_json_state_data(request,pk):

    state_data = list(State.objects.filter(country_id=pk).values())

    return JsonResponse({'data':state_data})



# get lg data via json
def get_json_lg_data(request,pk):
    lg_data = list(Lga.objects.filter(state_id=pk).values())
    # counrty_data = list(Country.objects.values())
    return JsonResponse({'data':lg_data})
