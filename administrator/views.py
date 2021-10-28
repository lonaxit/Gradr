from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse,JsonResponse
# import for user registration form
from  django.contrib.auth.forms import UserCreationForm
# from accounts.forms import ClientRegisterForm, contactForm, ClientForm,StudentRegisterForm
from accounts.forms import *
# from administrator.forms import TermForm,SessionForm
from administrator.forms import *
from teacher.forms import *
from django.contrib import messages
#import for restricting access to pages
from django.contrib.auth.decorators import login_required
# import make password for bulk creation
from django.contrib.auth.hashers import make_password

# import for creating a group
from django.contrib.auth.models import Group

# import models
from accounts.models import *
from teacher.models import *
from .models import *
from django.db.models import Q

#custom decorator
from accounts.decorators import unauthenticated_user,allowed_users,admin_only

# import transactions
from django.db import transaction

import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from teacher.views import *

# academics routine
# Filter Scores
@allowed_users(allowed_roles=['admin'])
def scoresFilter(request):

    # loggedin = request.user.teacher

    # try:
    #     pass
    # except Exception as e:
    #     print(e)


    form = ScoresFilterForm()


    if request.method =='POST':

        classroom = request.POST['classroom']
        subject = request.POST['subject']
        session = request.POST['session']
        term = request.POST['term']

        # check if record for the subject exist
        scores = Scores.objects.filter(Q(term=term) & Q(studentclass=classroom)
        & Q(session=session) & Q(subject=subject))

        #
        if not scores:
            messages.error(request, 'No record exist')
            return redirect('scores-summary')
        else:
            context ={ 'form':form,'scores':scores}
            return render(request,'admin/scores_summary.html',context)
    context = {'form':form}
    return render(request,'admin/scores_summary.html',context)


# filter result for head teacher comments
@allowed_users(allowed_roles=['admin'])
def resultFilter(request):

    # loggedin = request.user.tutor.pk

    form = ResultFilterForm()
    # entry = ClassTeacher.objects.filter(teacher=loggedin)

    if request.method =='POST':

        if request.POST.get('result-id'):

            resultObj = Result.objects.get(pk=request.POST['result-id'])
            # select all result that fit criteria
            # the result is used to send back to the page
            result = Result.objects.filter(Q(term=resultObj.term) & Q(studentclass=resultObj.studentclass)
            & Q(session=resultObj.session)).order_by('termposition')

            # save/update comment here
            comment = request.POST['comment']

            resultObj.headteachercomment=comment
            resultObj.save()

            messages.success(request, 'Comment added')
            context ={ 'form':form,'result':result}
            return render(request,'admin/comment_result.html',context)
        else:
            classroom = request.POST['classroom']
            session = request.POST['session']
            term = request.POST['term']

            # if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():

                # select reesult
            result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).order_by('termposition')

                #check for availability of result
            if not result:

                messages.error(request, 'No record exist')
                return redirect('comment-result')
            else:

                context ={ 'form':form,'result':result}
                return render(request,'admin/comment_result.html',context)

    context = {'form':form}
    return render(request,'admin/comment_result.html',context)


# result summary
@allowed_users(allowed_roles=['admin'])
def resultAnalysis(request):

    # loggedin = request.user.tutor.pk

    form = ResultFilterForm()
    # entry = ClassTeacher.objects.filter(teacher=loggedin)



    if request.method =='POST':


        classroom = request.POST['classroom']
        session = request.POST['session']
        term = request.POST['term']

        # if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():

            # select reesult
        result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).order_by('termposition')
        resultObj = result.first()


        nocommentsCount = result.filter(classteachercomment__isnull=True).count()
        yescommentsCount = result.filter(classteachercomment__isnull=False).count()

        no_headcommentsCount = result.filter(headteachercomment__isnull=True).count()
        yes_headcommentsCount = result.filter(headteachercomment__isnull=False).count()

        affective = Studentaffective.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).values('student').distinct('student')


        yesaffective = result.filter(student__in=affective).count()
        noaffective = result.exclude(student__in=affective).count()


        psychomotor = Studentpsychomotor.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).values('student').distinct('student')


        yespsycho = result.filter(student__in=psychomotor).count()
        nopsycho = result.exclude(student__in=psychomotor).count()

        noattendance = result.filter(attendance__isnull=True).count()
        yesattendance = result.filter(attendance__isnull=False).count()


        # find pass rate
        totalStudents = result.count()

        passedStudents = result.filter(termaverage__gte=40).count()

        passRate = passedStudents/totalStudents*100


        #check for availability of result
        if not result:

            messages.error(request, 'No record exist')
            return redirect('result-analysis')
        else:
                context ={ 'form':form,
                          'result':result,
                          'yescomment':yescommentsCount,
                          'nocomment':nocommentsCount,
                          'head_yescomment':yes_headcommentsCount,
                          'head_nocomment':no_headcommentsCount,
                          'yesaffective':yesaffective,
                          'noaffective':noaffective,
                          'yespsycho':yespsycho,
                          'nopsycho':nopsycho,
                          'yesattendance':yesattendance,
                          'noattendance':noattendance,
                          'resultObj':resultObj,
                          'passRate':passRate,
                          'totalStudents':totalStudents
                          }
                return render(request,'admin/resultAnalysis.html',context)
    context = {'form':form}
    return render(request,'admin/resultAnalysis.html',context)


# Approve result
@allowed_users(allowed_roles=['admin'])
def approveResult(request,classroom,term,session):

    # select reesult
    result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
        & Q(session=session))

    # Update the status of the result
    result.update(status='approved')
    submitCount = result.filter(status__isnull=False).count()
    messages.success(request, 'Result Approved Successfully!')
    # context={ 'result':result,'published':submitCount}
    # return render(request, 'admin/resultAnalysis.html',context)

    return redirect('result-analysis')


# create client
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

# Generate Admission Numbers
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def generateAdmissionNumber(request):

    user = request.user
    ClientProfile  = Client.objects.get(user_id=user.id)
    if request.method == 'POST':

        start = request.POST['start']
        end = request.POST['end']

        if not start or not end:
            messages.success(request, 'All fields are required')
            return redirect('generate-numbers')
        else:

        # # create range and save in the database
            for i in range(int(start),int(end)):
                obj = AdmissionNumber.objects.create(
                    client= ClientProfile,
                    serial_no = i
                )
                obj.save()

        messages.success(request, 'Admission numbers generated successfully')
        return redirect('generate-numbers')

    return render(request, 'admin/generateNumbers.html')

# update student with admission number
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateNumber(request,pk):

    user = request.user
    student  = Student.objects.get(pk=pk)
    no_item = AdmissionNumber.objects.filter(status='No').first()
    no_ = no_item.serial_no
    context = {
        'serial_no': no_
    }
    ClientProfile  = Client.objects.get(user_id=user.id)
    if request.method == 'POST':

        reg_no = request.POST['reg_no']

        if not reg_no:
            messages.success(request, 'Please provide a value')
            return redirect('update-numbers',pk=pk)
        else:
           


             # Get prefix
            sch_prefix = RegPrefix.objects.filter(client=ClientProfile).first()

            # casting int to str
            full_adm_string = sch_prefix.reg_prefix + student.session_admitted.session + str(no_)


            # update student with the serial reg number
            student.reg_no = no_
            student.full_reg_no = full_adm_string
            student.save()
            no_item.status='Yes'
            no_item.save()
            messages.success(request, 'Admission number updated successfully')
            # return to list students
            return redirect('list-students')

    return render(request, 'admin/update_number.html',context)


# define prefix
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def definePrefix(request):

    user = request.user
    ClientProfile  = Client.objects.get(user_id=user.id)

    if request.method == 'POST':

        prefix = request.POST['prefix']

        if not prefix:

            messages.success(request, 'Please provide a string')
            return redirect('define-prefix')
        else:
            # save the record

            obj = RegPrefix.objects.create(
                reg_prefix = prefix,
                client = ClientProfile
            )
            obj.save()
            messages.success(request, 'Admission prefix created  successfully')
            # return to list students
            return redirect('list-prefix')

    return render(request, 'admin/definePrefix.html')


# list all prefix
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listPrefix(request):
    prefix = RegPrefix.objects.all()
    context={
        'prefix':prefix
    }
    return render(request, 'admin/list_prefix.html',context)


# update prefix
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updatePrefix(request,pk):

    user = request.user
    prefixObj  = RegPrefix.objects.get(pk=pk)

    context = {
        'prefix': prefixObj
    }

    if request.method == 'POST':

        prefix = request.POST['prefix']

        if not prefix:

            messages.success(request, 'Please provide a string')
            return redirect('update-prefix',pk=pk)
        else:

            prefixObj.reg_prefix=prefix
            prefixObj.save()
            messages.success(request, 'Updated successful!')
            # return to list students
            return redirect('list-prefix')

    return render(request, 'admin/update_prefix.html',context)


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
            return redirect('admin-profile')
    context = {'form':form}
    return render(request, 'admin/updateClient.html',context)


# sign up new a student user
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def newStudent(request):
    # redirect authenticated user to the dashboard
    form = StudentRegisterForm()
    # loggedin = request.user.tutor.pk
    # myclient = request.user.tutor
    logged_inuser = request.user
    clientProfile  = Client.objects.get(user_id=logged_inuser.id)
    # context={'form': form}
    if request.method == 'POST':
        try:
            
            # transaction
            with transaction.atomic():
                form  = StudentRegisterForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    #getting username from form
                    username = form.cleaned_data.get('username')
                    email = form.cleaned_data.get('email')
                    # associate user with admin
                    group = Group.objects.get(name='student')
                    user.groups.add(group)

                    # attach a profile to a student
                    StudObj = Student.objects.create(
                    user = user,
                    email=email,
                    client = clientProfile,
                    createdby=User.objects.get(pk=logged_inuser.pk)
                    )
                    StudObj.save()

                messages.success(request, 'Student account creation successful for ' + username + ',  please update the profile')
                return redirect('update-student',pk=StudObj.pk)
        except Exception as e:
            messages.error(request, e)
            return render (request,'admin/newStudent.html',{'form':form})

    return render (request,'admin/newStudent.html',{'form':form})



# update student profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateStudentProfile(request,pk):
    user = request.user
    student  = Student.objects.get(pk=pk)
    ClientProfile  = Client.objects.get(user_id=user.id)

    form = StudentProfileForm(instance=student)
    # form = StudentProfileForm()
    context = {'form':form}
    if request.method == 'POST':
        form = StudentProfileForm(request.POST,request.FILES, instance=student)
        if form.is_valid():
            form.save()

            messages.success(request, 'Student profile  modification/creation was  successful')
            return redirect('view-student',pk=student.pk)
        else:


            messages.success(request, 'Something went wrong')
            return redirect('update-student',pk=pk)

    return render(request, 'admin/updateStudentProfile.html',context)

# Change student photo
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def studentPhoto(request,pk):
    user = request.user
    student  = Student.objects.get(pk=pk)

    form = StudentImageUpdateForm(instance=student)

    context = {'form':form}
    if request.method == 'POST':
        form = StudentImageUpdateForm(request.POST,request.FILES,instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo changed')
            return redirect('view-student',pk=pk)
        else:
             messages.success(request, 'Photo update failed')
             return redirect('student-photo',pk=pk)

    return render(request, 'admin/changeProfilePicture.html',context)


# update institution logo
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def logo(request,pk):
    user = request.user
    client  = Client.objects.get(pk=pk)

    form = LogoUpdateForm(instance=client)

    context = {'form':form}
    if request.method == 'POST':
        form = LogoUpdateForm(request.POST,request.FILES,instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Logo updated')
            return redirect('admin-profile')
        else:
             messages.success(request, 'Photo update failed')
             return redirect('logo',pk=pk)

    return render(request, 'admin/updateLogo.html',context)

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
        # transaction
        with transaction.atomic():
            form  = StaffRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                #getting username from form
                username = form.cleaned_data.get('username')
                # associate user with admin
                group = Group.objects.get(name='teacher')
                user.groups.add(group)

                # attach a profile to a client
                TeacherObj = Teacher.objects.create(
                    user = user,
                    client = clientProfile,
                    createdby=User.objects.get(pk=logged_inuser.pk),
                )
                TeacherObj.save()


                messages.success(request, 'Account creation successful for ' + username + ',  please update the profile')
                return redirect('update-teacher',pk=TeacherObj.pk)

    return render (request,'admin/newTeacher.html',{'form':form})

# update teacher profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateTeacherProfile(request,pk):
    user = request.user
    # ClientProfile  = Client.objects.get(user_id=user.id)
    teacher  = Teacher.objects.get(pk=pk)
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


# teacher profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def viewTeacher(request,pk):
    context ={}
    teacher = Teacher.objects.get(pk=pk)

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


# update teacher photo
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def teacherPhoto(request,pk):
    user = request.user
    teacher  = Teacher.objects.get(pk=pk)

    form = TeacherImageUpdateForm(instance=teacher)

    context = {'form':form}
    if request.method == 'POST':
        form = TeacherImageUpdateForm(request.POST,request.FILES,instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo changed')
            return redirect('view-teacher',pk=pk)
        else:
             messages.success(request, 'Photo update failed')
             return redirect('teacher-photo',pk=pk)

    return render(request, 'admin/changeTeacherPicture.html',context)



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
                                     client = client,
                                     createdby= User.objects.get(pk=request.user.pk)
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
                                     client = client,
                                     createdby=User.objects.get(pk=request.user.pk)
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
    
    form = TermForm()
    context = {}
    if request.method == "POST":
        try:
            
            client = Client.objects.get(user_id=request.user.pk)
            form = TermForm(request.POST)
            if form.is_valid():
                term = form.cleaned_data.get("term")
                client = client
                obj = Term.objects.create(
                                 term = term,
                                 client = client,
                                 createdby=User.objects.get(pk=request.user.pk)
                                     )
                obj.save()
                messages.success(request, 'Record added')
                return redirect('create-term')
            else:
                messages.success(request, 'Something went wrong')
                return redirect('create-term')
        except Exception as e:
            messages.error(request,  e)
            context={'form':form}
            return render(request, "admin/addTerm.html", context)
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
                                 client = client,
                                 createdby=User.objects.get(pk=request.user.pk)
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
                                 client = client,
                                 createdby=User.objects.get(pk=request.user.pk)
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
    
    form = ClassForm()
    context = {}
    if request.method == 'POST':
        try:
            
            client = Client.objects.get(user_id=request.user.id)
            form = ClassForm(request.POST)
            if form.is_valid():

                classname = form.cleaned_data.get("class_name")
                client = client
                obj = StudentClass.objects.create(
                                 class_name = classname,
                                 client = client,
                                 createdby= User.objects.get(pk=request.user.pk)
                                     )
                obj.save()
                

                messages.success(request, 'Record added')
                return redirect('add-class')
            else:

                messages.success(request, 'oops! something went wrong')
                return redirect('add-class')
        except Exception as e:
            messages.error(request,  e)
            return render(request, "admin/addClass.html", context)
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
            subject_code = form.cleaned_data.get("subject_code")
            client = client
            obj = Subject.objects.create(
                                 subject = subject,
                                 client = client,
                                 subject_code=subject_code,
                                 createdby=User.objects.get(pk=request.user.pk)
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
            # return redirect('admin-profile')
            return redirect('all-subjects')
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
                                 client = client,
                                 createdby= User.objects.get(pk=request.user.pk)
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
                                 client = client,
                                 createdby=User.objects.get(pk=request.pk)
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
    student = Student.objects.get(pk=pk)
    result = Result.objects.filter(student=student).distinct('session')

    context ={
    'student':student,
    'result':result
    }

    return render(request, 'admin/view_student_profile.html',context)


# admission list

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admissionList(request):
    form = AdmissionListForm()
    # context ={'form':form}
    if request.method == 'POST':
        form = AdmissionListForm(request.POST)
        if form.is_valid():
            term = Term.objects.get(pk=request.POST['term'])
            session = Session.objects.get(pk=request.POST['session'])
            classroom = Term.objects.get(pk=request.POST['classroom'])
            # term_id = request.POST['term']
            # session_id = request.POST['session']
            # class_id = request.POST['classroom']
            # term = Term.objects.get(pk=term_id)
            
            
            # select students based on search parameter
            result = Student.objects.filter(Q(session_admitted=session.pk)  & Q(class_admitted=classroom.pk) & Q(term_admitted=term.pk))
            if not result:
                messages.error(request, 'No record exist')
                return redirect('admission-list')
            else:
                context = { 'form':form,
                           'result':result,
                           'term':term,
                           'session':session,
                           'classroom':classroom
                           }
                return render(request,'admin/filter_admission_list.html',context)
        else:
            messages.error(request, 'oops! something went wrong')
            return redirect('admission-list')

    context ={'form':form}
    return render(request, 'admin/filter_admission_list.html',context)

# export admission List
@allowed_users(allowed_roles=['admin'])
def exportAdmissionList(request,session,classroom,term):


    try:
        termObj = Term.objects.get(pk=term)
        sessObj = Session.objects.get(pk=session)
        classroomObj = StudentClass.objects.get(pk=classroom)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Admission_List_'+classroomObj.class_name+'_'+termObj.term+'_'+sessObj.session+'.csv'
        writer = csv.writer(response)

        writer.writerow(['Name','Class','Sex','Session','RegNumber'])

        students = Student.objects.filter(Q(session_admitted=sessObj) & Q(term_admitted=termObj.pk) & Q(class_admitted=classroomObj.pk)).order_by('sur_name')
         
        for student in students:
            writer.writerow([student.sur_name+ ' ' +student.first_name,student.class_admitted.class_name,student.sex,student.session_admitted.session,student.full_reg_no])

        return response

    except Exception as e:
             messages.error(request,  e)
             return render(request,'admin/filter_admission_list.html')


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




# create affective domain
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addAffective(request):
    # client = Client.objects.get(user_id=request.user.id)
    form = AffectiveForm()
    context = {}
    if request.method == "POST":

        form = AffectiveForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data.get("domain")
            # client = client
            obj = Affective.objects.create(
                                 domain = domain
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('add-affective')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('add-affective')
    context={'form':form}
    return render(request, "admin/addAffective.html", context)


# list all affective domain
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listAffective(request):
    affective = Affective.objects.all()

    if affective:
        context = { 'affective': affective}
        return render(request, "admin/listAffective.html", context)
    else:
        messages.error(request, 'No record available')
        return redirect('list-affective')
    return render(request, "admin/listAffective.html")


# update affective domain
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateAffective(request,pk):

    affective = Affective.objects.get(id=pk)
    form = AffectiveForm(instance=affective)
    context = {'form':form}
    if request.method == "POST":

        form = AffectiveForm(request.POST,instance=affective)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated')
            return redirect('list-affective')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('update-affective',pk=pk)
    context={'form':form}
    return render(request, "admin/updateAffective.html", context)


# create psychomotor
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addPsychomotor(request):
    # client = Client.objects.get(user_id=request.user.id)
    form = PsychomotorForm()
    context = {}
    if request.method == "POST":

        form = PsychomotorForm(request.POST)
        if form.is_valid():
            skill = form.cleaned_data.get("skill")
            # client = client
            obj = Psychomotor.objects.create(
                                 skill = skill
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('add-psychomotor')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('add-psychomotor')
    context={'form':form}
    return render(request, "admin/addPsychomotor.html", context)


# list all psychomotor skills
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listPsychomotor(request):
    skills = Psychomotor.objects.all()

    if skills:
        context = { 'skills': skills}
        return render(request, "admin/listPsychomotor.html", context)
    else:
        messages.error(request, 'No record available')
        return redirect('list-psychomotor')
    return render(request, "admin/listPsychomotor.html")


# update Psychomotor skill
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updatePsychomotor(request,pk):

    skill = Psychomotor.objects.get(id=pk)
    form = PsychomotorForm(instance=skill)
    context = {'form':form}
    if request.method == "POST":

        form = PsychomotorForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated')
            return redirect('list-psychomotor')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('update-psychomotor',pk=pk)
    context={'form':form}
    return render(request, "admin/updatePsychomotor.html", context)


# create rating
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addRating(request):

    form = RatingForm()
    context = {}
    if request.method == "POST":

        form = RatingForm(request.POST)
        if form.is_valid():

            description = form.cleaned_data.get("description")
            score = form.cleaned_data.get("scores")

            obj = Rating.objects.create(
                                 description = description,
                                 scores=score
                                     )
            obj.save()
            messages.success(request, 'Record added')
            return redirect('add-rating')
        else:

            messages.error(request, 'Something went wrong')
            return redirect('add-rating')
    context={'form':form}
    return render(request, "admin/addRating.html", context)


# list all ratings
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def listRating(request):
    ratings = Rating.objects.all()

    if ratings:
        context = { 'ratings': ratings}
        return render(request, "admin/listRating.html", context)
    else:
        messages.error(request, 'No record available')
        return redirect('list-rating')
    return render(request, "admin/listRating.html")


# update Rating
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateRating(request,pk):

    rating = Rating.objects.get(id=pk)
    form = RatingForm(instance=rating)
    context = {'form':form}
    if request.method == "POST":

        form = RatingForm(request.POST,instance=rating)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated')
            return redirect('list-rating')
        else:
            messages.success(request, 'Something went wrong')
            return redirect('update-rating',pk=pk)
    context={'form':form}
    return render(request, "admin/updateRating.html", context)


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


# code below for datamigration purposes only, remove afterwards
# not complete

@allowed_users(allowed_roles=['admin'])
def migrateAss(request):

    loggedin = request.user.tutor.pk
    myclient = request.user.tutor

    # try:
    classes = StudentClass.objects.all()
    context={
    'classes': classes
    }

    if request.method=='POST' and request.POST.get('subject'):

        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')
        # classteacher
        teacherObj = SubjectTeacher.objects.get(pk=loggedin)
        classroom = request.POST['studentclass']

        # classroom object
        classroomObj = StudentClass.objects.get(pk=classroom)
        subject_id = request.POST['subject']
        # subject object
        subjectObj = Subject.objects.get(pk=subject_id)


        myfile = request.FILES['csvFile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        excel_file = uploaded_file_url
        # print(excel_file)
        empexceldata = pd.read_csv("media/"+filename,encoding='utf-8')
        # print(type(empexceldata))
        dbframe = empexceldata

        with transaction.atomic():

            for dbframe in dbframe.itertuples():
                studentObj=Student.objects.get(pk=dbframe.StudentID)
                # check if records of a student exist in that subject, class,term,session
                scoresExist = Scores.objects.filter(session=activeSession,term=activeTerm,subject=subjectObj,studentclass=classroomObj,student=studentObj.pk)
                if scoresExist:
                    pass
                else:

                    # fromdate_time_obj = dt.datetime.strptime(dbframe.DOB, '%d-%m-%Y')
                    obj = Scores.objects.create(
                        firstscore=dbframe.FirstCA,
                        secondscore=dbframe.SecondCA,
                        thirdscore=dbframe.ThirdCA,
                        totalca=dbframe.CATotal,
                        examscore=dbframe.Exam,
                        subjecttotal=dbframe.Total,
                        session=activeSession,
                        term=activeTerm,
                        student=studentObj,
                        studentclass=classroomObj,
                        subjectteacher= teacherObj,
                        client= myclient.client,
                        subject=subjectObj,
                    )
                    # DOB=fromdate_time_obj,
                    # qualification=dbframe.qualification)
                    # print(type(obj))
                    obj.save()
                    # process Scores
                    processScores(subjectObj,classroomObj)

                    # process terminal result
                    processTerminalResult(obj)

                    # process terminal result
                    processAnnualResult(obj)

                    # Add auto comment
                    autoAddComment(classroomObj,activeSession,activeTerm)
            messages.success(request,  'Successful')
            return render(request,'admin/import_assessment_sheet.html',context)

        # return render(request, 'teacher/import_assessment_sheet.html',context)

    messages.error(request,  'Ensure you specify all information and you have a csv file selected!')
    return render(request,'teacher/import_assessment_sheet.html',context)


# bulk create students
# sign up new a student user
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def bulkStudent(request):
    
    logged_inuser = request.user
    clientProfile  = Client.objects.get(user_id=logged_inuser.id)
    
    if request.method == 'POST':
        
        myfile = request.FILES['csvFile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        excel_file = uploaded_file_url
        # print(excel_file)
        exceldata = pd.read_csv("media/"+filename,encoding='utf-8')
        # print(type(empexceldata))
        dbframe = exceldata

        with transaction.atomic():

            for dbframe in dbframe.itertuples():
                
                sessObj=Session.objects.get(pk=dbframe.SESSID)
                regString= "SKY/STD/"+sessObj.session+"/"+str(dbframe.REGNUM)
               
                # comment out
                
                obj = User.objects.create(
                    username=dbframe.UNAME, 
                    password=make_password(dbframe.PWD),
                    email=dbframe.EMAIL,           
                    )     
                obj.save()
            
                
                #getting username from form
                # username = form.cleaned_data.get('username')
                # email = form.cleaned_data.get('email')
                # # associate user with student
                group = Group.objects.get(name='student')
                obj.groups.add(group)

                # attach a profile to a client
                StudObj = Student.objects.create(
                user = obj,
                sex=dbframe.GENDER,
                lga=dbframe.LGA,
                # STATE=dbframe.STATE,
                blood_group=dbframe.BLOODGROUP,
                address=dbframe.CONTADD,
                # class_admitted=StudentClass.objects.get(pk=dbframe.CLASS),
                # session_admitted=Session.objects.get(pk=dbframe.SESSION),
                sur_name=dbframe.SURNAME,
                first_name=dbframe.LASTNAME,
                reg_no=dbframe.REGNUM,
                full_reg_no=regString,
                session_admitted=sessObj,
                class_admitted=StudentClass.objects.get(pk=dbframe.CLASSID),
                client =clientProfile,
                createdby=User.objects.get(pk=request.user.pk)
                )
                StudObj.save()

            messages.success(request, 'Student account creation successful')
            return redirect('create-students')

    return render (request,'admin/create_bulk_users.html')
