from django.shortcuts import render,redirect


from django.http import HttpResponse,JsonResponse

import csv
# import models
# from accounts.models import *
# from administrator.models import *
from accounts.models import Client,Student
from administrator.models import Session,Term,StudentClass,Subject,SubjectTeacher,ClassTeacher
from .models import *
from django.db.models import Q, Sum, Avg, Max, Min
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

# import for creating a group
from django.contrib.auth.models import Group


#custom decorator
from accounts.decorators import unauthenticated_user,allowed_users,admin_only
# Create your views here.

# xhtml2pdf imports
# import os
# from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# from django.contrib.staticfiles import finder

# import transactions
from django.db import transaction

def printResultHtml(request,pk):
    teacher_loggedin = request.user.tutor
    result = Result.objects.get(pk=pk)
    academic_scores = Scores.objects.filter(student=result.student,studentclass=result.studentclass,term=result.term,session=result.session)
    student_count = Scores.objects.filter(studentclass=result.studentclass,term=result.term,session=result.session).distinct('student').count()
    affective = Studentaffective.objects.filter(student=result.student,studentclass=result.studentclass,session=result.session,term=result.term)

    psychomotor = Studentpsychomotor.objects.filter(student=result.student,studentclass=result.studentclass,session=result.session,term=result.term)



    # academic_scores = Scores.objects.filter(student=1,studentclass=1,term=1,session=1)
    context={
        'scores':academic_scores,
        'result':result,
        'student_count':student_count,
        'affective':affective,
        'psychomotor':psychomotor
    }
    return render(request,'teacher/print.html',context)


def render_pdf_view(request):
    teacher_loggedin = request.user.teacher
    result = Result.objects.get(pk=3)
    academic_scores = Scores.objects.filter(student=1,studentclass=1,term=1,session=1)
    student_count = Scores.objects.filter(studentclass=result.studentclass,term=result.term,session=result.session).distinct('student').count()
    affective = Studentaffective.objects.filter(student=result.student,studentclass=result.studentclass,session=result.session,term=result.term)

    psychomotor = Studentpsychomotor.objects.filter(student=result.student,studentclass=result.studentclass,session=result.session,term=result.term)

    template_path = 'teacher/print.html'
    # academic_scores = Scores.objects.filter(student=1,studentclass=1,term=1,session=1)
    context={
        'scores':academic_scores,
        'result':result,
        'student_count':student_count,
        'affective':affective,
        'psychomotor':psychomotor
    }
    # context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if download: run this line of code below
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # if display: run this line of code
    # response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    # removed link call back
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    #    html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response






@login_required(login_url='login')
# @admin_only
@allowed_users(allowed_roles=['teacher'])
def teacherHome(request):
    students = Student.objects.all()
    context = {'students':students}
    return render(request,'teacher/teacher_home.html',context)



# teacher profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacherProfile(request):

    return render(request, 'teacher/teacher_profile.html')

# change avatar
@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teacherAvatar(request):
    teacher = request.user.tutor
    # teacher  = Teacher.objects.get(pk=pk)

    form = TeacherImageUpdateForm(instance=teacher)

    context = {'form':form}
    if request.method == 'POST':
        form = TeacherImageUpdateForm(request.POST,request.FILES,instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo changed')
            return redirect('teacher-profile')
        else:
             messages.success(request, 'Photo update failed')
             return redirect('teacher-avatar')

    return render(request, 'teacher/changeTeacherAvatar.html',context)

# list all my subjects
def mySubjects(request):
    loggedin = request.user.tutor
    my_subjects = SubjectTeacher.objects.filter(teacher=loggedin.pk)
    context = {'mysubjects':my_subjects}
    return render(request,'teacher/my_subjects.html',context)


# add new scores
@allowed_users(allowed_roles=['teacher'])
def addScores(request):

    loggedin = request.user.tutor

    form = ScoresForm()

    context = {'form':form}
    if request.method =='POST':
        subj = request.POST['subject']
        studclass = request.POST['studentclass']
        studid = request.POST['studentnumber']
        ca1 = request.POST['firstscore']
        ca2 = request.POST['secondscore']
        ca3 = request.POST['thirdscore']
        totalass = request.POST['totalca']
        exam = request.POST['examscore']
        total = request.POST['subjecttotal']

        # get sctive term and session
        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')

        teacherObj = SubjectTeacher.objects.get(pk=loggedin.pk)
        subjectObj = Subject.objects.get(pk=subj)
        classroomObj = StudentClass.objects.get(pk=studclass)
        studObj = Student.objects.get(pk=studid)


        # check if record for the subject exist
        scores = Scores.objects.filter(Q(term=activeTerm) & Q(studentclass=classroomObj)
        & Q(session=activeSession) & Q(subject=subjectObj) & Q(student=studObj) )

        if scores:
            messages.error(request, 'Record exist')
            return redirect('new-scores')
        else:
            with transaction.atomic():

                obj = Scores.objects.create(
                                 firstscore = ca1,
                                 secondscore = ca2,
                                 thirdscore = ca3,
                                 totalca = totalass,
                                 examscore = exam,
                                 session = activeSession,
                                 studentclass = classroomObj,
                                 subject = subjectObj,
                                 subjectteacher = teacherObj,
                                 term = activeTerm,
                                 subjecttotal = total,
                                 client = loggedin.client,
                                 student = studObj,
                                     )
                obj.save()

                # process Scores
                processScores(subjectObj,classroomObj)

                # process terminal result
                processTerminalResult(obj)


                # Add auto comment
                autoAddComment(classroomObj,activeSession,activeTerm)

                messages.success(request, 'Scores created')
                # return redirect('assign-subject')
    # context = {'form':form}
    return render(request,'teacher/new_scores.html',context)


# edit scores
@allowed_users(allowed_roles=['teacher'])
def editScores(request,id):

    loggedin = request.user.tutor
    scores = Scores.objects.get(pk=id)
    form = ScoresForm(instance=scores)
    # student = Student.objects.get(id=scores.student.id)

    context = {'form':form,'scores':scores}
    if request.method =='POST':


        # form = ScoresForm(request.POST,instance=scores)
        subj = request.POST['subject']
        studclass = request.POST['studentclass']
        studid = request.POST['studentnumber']

        ca1 = request.POST['firstscore']
        ca2 = request.POST['secondscore']
        ca3 = request.POST['thirdscore']
        totalass = request.POST['totalca']
        exam = request.POST['examscore']
        total = request.POST['subjecttotal']

        # get active term and session
        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')

        teacherObj = SubjectTeacher.objects.get(pk=loggedin.pk)
        subjectObj = Subject.objects.get(pk=subj)
        classroomObj = StudentClass.objects.get(pk=studclass)
        studObj = Student.objects.get(pk=studid)

        # use transaction
        with transaction.atomic():
            scores_Obj = Scores.objects.select_for_update().get(pk=id)

            scores_Obj.firstscore = ca1
            scores_Obj.secondscore = ca2
            scores_Obj.thirdscore = ca3
            scores_Obj.totalca = totalass
            scores_Obj.examscore = exam
            scores_Obj.session = activeSession
            scores_Obj.studentclass = classroomObj
            scores_Obj.subject = subjectObj
            scores_Obj.subjectteacher = teacherObj
            scores_Obj.term = activeTerm
            scores_Obj.subjecttotal = total
            scores_Obj.client = loggedin.client
            scores_Obj.student = studObj
            scores_Obj.save()

            # process Scores
            processScores(subjectObj,classroomObj)

            # process terminal result
            processTerminalResult(scores_Obj)

            # auto add comments

            autoAddComment(classroomObj,activeSession,activeTerm)

            # Scores.objects.filter(id=data['id']).update(email=data['email'], phone=data['phone'])
            messages.success(request, 'Scores edited successfully')
            return redirect('filter-scores')
    # context = {'form':form}
    return render(request,'teacher/edit_scores.html',context)

# remove scores

@allowed_users(allowed_roles=['teacher'])
def deleteScores(request,id):

    loggedin = request.user.teacher
    scores = Scores.objects.select_for_update().get(pk=id)

    # get sctive term and session
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    with transaction.atomic():

        scores = Scores.objects.select_for_update().get(pk=id)
        subject = scores.subject
        classroom = scores.studentclass
        studentid = scores.student

        scores.delete()

        # delete terminal result
        deleteResult(studentid,classroom)
        scores_filter = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession).first()

        if scores_filter:
            # process Scores
            processScores(subject,classroom)
            # process terminal result
            processTerminalResult(scores_filter)

            # add auto comment

            autoAddComment(classroom,activeSession,activeTerm)

            # TODO: MAKE SURE TO DELETE CORRESPONDING STUDENT RECORD IN THE RESULT TABLE

    messages.success(request, 'Scores deleted successfully')
    return redirect('filter-scores')

    # return render(request,'teacher/edit_scores.html')


# Filter Scores
@allowed_users(allowed_roles=['teacher'])
def scoresFilter(request):

    loggedin = request.user.tutor.pk

    form = ScoresFilterForm()


    if request.method =='POST':

        classroom = request.POST['classroom']
        subject = request.POST['subject']
        session = request.POST['session']
        term = request.POST['term']


        # get sctive term and session
        # activeTerm = Term.objects.get(status='True')
        # activeSession = Session.objects.get(status='True')
        #
        # teacherObj = SubjectTeacher.objects.get(id=loggedin.id)
        # subjectObj = Subject.objects.get(id=subj)
        # classroomObj = StudentClass.objects.get(id=studclass)
        # studObj = Student.objects.get(id=studid)

        # check if record for the subject exist
        scores = Scores.objects.filter(Q(term=term) & Q(studentclass=classroom)
        & Q(session=session) & Q(subject=subject))

        #
        if not scores:
            messages.error(request, 'No record exist')
            return redirect('filter-scores')
        else:
            context ={ 'form':form,'scores':scores}
            return render(request,'teacher/filterScores.html',context)
    context = {'form':form}
    return render(request,'teacher/filterScores.html',context)





# Result Filter
@allowed_users(allowed_roles=['teacher'])
def resultFilter(request):

    loggedin = request.user.tutor.pk

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

            resultObj.classteachercomment=comment
            resultObj.save()

            messages.success(request, 'Comment added')
            context ={ 'form':form,'result':result}
            return render(request,'teacher/filterResult.html',context)
        else:
            classroom = request.POST['classroom']
            session = request.POST['session']
            term = request.POST['term']

            if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():

                # select reesult
                result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).order_by('termposition')

                #check for availability of result
                if not result:
                    messages.error(request, 'No record exist')
                    return redirect('filter-result')
                else:

                    context ={ 'form':form,'result':result}
                    return render(request,'teacher/filterResult.html',context)

    context = {'form':form}
    return render(request,'teacher/filterResult.html',context)


# Add term Attendance
@allowed_users(allowed_roles=['teacher'])
def addAttendance(request):

    loggedin = request.user.tutor.pk

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
            attendance = request.POST['attendance']

            resultObj.attendance=attendance
            resultObj.save()

            messages.success(request, 'Attendance added')
            context ={ 'form':form,'result':result}
            return render(request,'teacher/addAttendance.html',context)
        else:
            classroom = request.POST['classroom']
            session = request.POST['session']
            term = request.POST['term']

            if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():

                # select reesult
                result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).order_by('termposition')

                #check for availability of result
                if not result:
                    messages.error(request, 'No record exist')
                    return redirect('filter-result')
                else:
                    context ={ 'form':form,'result':result}
                    return render(request,'teacher/addAttendance.html',context)

    context = {'form':form}
    return render(request,'teacher/addAttendance.html',context)



# Enroll students in class
@allowed_users(allowed_roles=['teacher'])
def enrollStudent(request):

    loggedin = request.user.tutor.pk

    if request.method =='POST':
        
        try:
            activeTerm = Term.objects.get(status='True')
            activeSession = Session.objects.get(status='True')
            classTeacher = ClassTeacher.objects.get(teacher=loggedin,term=activeTerm,session=activeSession)
            if classTeacher:
                
    
                enroll = request.POST['enroll']
                if enroll:
                    student = Student.objects.get(reg_no=enroll)

                    # check if student is already enrolled
                    studentEnrolled = Classroom.objects.filter(Q(term=activeTerm) & Q(session=activeSession) & Q      (class_room=classTeacher.classroom.pk) & Q(student=student.pk))
                
                    if studentEnrolled:
                    
                        messages.success(request, 'Student alrteady enrolled')
                        return redirect('enroll')
                    else:
                        # enroll student
                        enrollObj = Classroom.objects.create(
                        class_room=classTeacher.classroom,
                        client =classTeacher.client,
                        session = activeSession,
                        term = activeTerm,
                        student = student
                        )
                        enrollObj.save()
                        messages.success(request, 'Student enrolled successfully!')
                        return redirect('enroll')
                else:
                    messages.error(request, 'Enter a student registration/admission please!')
                    return redirect('enroll')
            else:
                messages.error(request, 'You are not a class teacher you can not enroll a student!')
                return redirect('enroll')
        except Exception as e: 
                messages.error(request,  e)
                return redirect('enroll')
            
    return render(request,'teacher/enroll_student.html')

# remove student in class
# Enroll students in class
@allowed_users(allowed_roles=['teacher'])
def deleteEnrollment(request,pk):

    loggedin = request.user.tutor.pk
        
    try:
        if request.method == 'POST':
            
            activeTerm = Term.objects.get(status='True')
            activeSession = Session.objects.get(status='True')
            classTeacher = ClassTeacher.objects.get(teacher=loggedin,term=activeTerm,session=activeSession)
            if classTeacher:
                student = Classroom.objects.get(pk=pk)
                student.delete() 
                messages.success(request, 'Student unenrolled in this class')
                return redirect('classroom')    
           
            else:
                messages.error(request, 'You are not a class teacher you can not perform this action!')
                return redirect('classroom')
        return render(request,'teacher/confirm_delete.html')
    except Exception as e: 
                messages.error(request,  e)
                return redirect('classroom')


# my classroom enrollees
@allowed_users(allowed_roles=['teacher'])
def myClassroom(request):
    

    loggedin = request.user.tutor.pk
   
    try:
        
        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')

        classTeacher = ClassTeacher.objects.get(teacher=loggedin,term=activeTerm,session=activeSession)
            
        if classTeacher:
            
                students = Classroom.objects.filter(Q(term=activeTerm) & Q(session=activeSession) & Q      (class_room=classTeacher.classroom.pk)).order_by('student__sur_name')
                # ordering using a different table, student field is on classroom table which is related to the student table and sur_name is on the student table
                
                if students:
                    context={
                        'students':students
                    }
                    return render(request,'teacher/classroom.html',context)
        else:
             messages.error(request, 'You are not a class teacher you can not enroll a student!')
             return redirect('teacher')
        
    except Exception as e: 
            messages.error(request,  e)
            return render(request,'teacher/classroom.html')
        

# Get assessment sheet
@allowed_users(allowed_roles=['teacher'])
def assessmentSheet(request):
    

    loggedin = request.user.tutor.pk
    
    classes = StudentClass.objects.all()
    context={
        'classes': classes
    }
    if request.method == 'POST':
        
        try:
            
            activeTerm = Term.objects.get(status='True')
            activeSession = Session.objects.get(status='True')
            classroom = request.POST['studentclass']
            subject_id = request.POST['subject']
            if subject_id:
                
                students = Classroom.objects.filter(Q(term=activeTerm) & Q(session=activeSession) & Q      (class_room=classroom)).order_by('student__sur_name')
                subject = Subject.objects.get(pk=subject_id)
                
                # ordering using a different table, student field is on classroom table which is related to        the student table and sur_name is on the student table
                context={
                    'students':students,
                    'subject':subject,
                    'classroom':classroom
                }
                return render(request, 'teacher/ca_sheet_preview.html',context)
            else:
                messages.error(request, 'Choose a subject')
                return redirect('assessment-sheet')
        except Exception as e:
             messages.error(request,  e)
             return render(request,'teacher/assessment_sheet_find.html')
    
    return render(request, 'teacher/assessment_sheet_find.html',context)
   
    
# export assessment sheet 

@allowed_users(allowed_roles=['teacher'])
def exportSheet(request,classroom,subject):
    

    loggedin = request.user.tutor.pk
      
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=assessmentSheet.csv'
        writer = csv.writer(response)
            
        writer.writerow(['StudentID','Name','Class','Subject','First CA','Second CA','Third CA','CA Total','Exam','Total'])
            
        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')
        
            
        students = Classroom.objects.filter(Q(term=activeTerm) & Q(session=activeSession) & Q(class_room=classroom)).order_by('student__sur_name')
        subject = Subject.objects.get(pk=subject)
                
            # ordering using a different table, student field is on classroom table which is related to the student table and sur_name is on the student table
        for student in students:
            writer.writerow([student.student.pk,student.student.sur_name,student.class_room.class_name,subject.subject,0,0,0,0,0])
        
        return response        
        
    except Exception as e:
             messages.error(request,  e)
             return render(request,'teacher/assessment_sheet_find.html')
    
    



# Select result from finish button action
@allowed_users(allowed_roles=['teacher'])
def resultComments(request,classroom,term,session):

    loggedin = request.user.tutor.pk

    form = ResultFilterForm()
    # entry = ClassTeacher.objects.filter(teacher=loggedin)
    result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).order_by('termposition')

    if request.method =='POST':

        if request.POST.get('result-id'):

            resultObj = Result.objects.get(pk=request.POST['result-id'])
            # select all result that fit criteria
            # the result is used to send back to the page
            result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
            & Q(session=session)).order_by('termposition')

            # save/update comment here
            comment = request.POST['comment']

            resultObj.classteachercomment=comment
            resultObj.save()

            messages.success(request, 'Comment added')
            context ={ 'form':form,'result':result}
            return render(request,'teacher/filterResult.html',context)
        else:
            classroom = request.POST['classroom']
            session = request.POST['session']
            term = request.POST['term']

            if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():

                # select reesult
                result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).order_by('termposition')

                #check for availability of result
                if not result:
                    messages.error(request, 'No record exist')
                    return redirect('filter-result')
                else:

                    context ={ 'form':form,'result':result}
                    return render(request,'teacher/filterResult.html',context)

    context ={'form':form,'result':result}
    return render(request,'teacher/filterResult.html',context)


# Result Summary
@allowed_users(allowed_roles=['teacher'])
def resultSummary(request):

    loggedin = request.user.tutor.pk

    form = ResultFilterForm()
    # entry = ClassTeacher.objects.filter(teacher=loggedin)



    if request.method =='POST':


        classroom = request.POST['classroom']
        session = request.POST['session']
        term = request.POST['term']

        if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():

            # select reesult
            result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).order_by('termposition')
            resultObj = result.first()


            nocommentsCount = result.filter(classteachercomment__isnull=True).count()
            yescommentsCount = result.filter(classteachercomment__isnull=False).count()

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
                return redirect('result-summary')
            else:
                context ={ 'form':form,
                          'result':result,
                          'yescomment':yescommentsCount,
                          'nocomment':nocommentsCount,
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
                return render(request,'teacher/resultSummary.html',context)
    context = {'form':form}
    return render(request,'teacher/resultSummary.html',context)



# submit result
@allowed_users(allowed_roles=['teacher'])
def submitResult(request,classroom,term,session):


    loggedin = request.user.tutor.pk

    if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():
                # select reesult
        result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
        & Q(session=session))

        # Update the status of the result
        result.update(status='submitted')
        submitCount = result.filter(status__isnull=False).count()
        messages.success(request, 'Result Submitted Successfully!')
        context={ 'result':result,'published':submitCount}
        return render(request, 'teacher/resultSummary')

    return redirect('result-summary')



# Add student affective
@allowed_users(allowed_roles=['teacher'])
def addStudentAffective(request,pk):

    loggedin = request.user.tutor.pk

    client = Client.objects.get(pk=request.user.tutor.client.pk)

    resultObj = Result.objects.get(pk=pk)
    student = Student.objects.get(pk=resultObj.student.pk)
    term = Term.objects.get(pk=resultObj.term.pk)
    session = Session.objects.get(pk=resultObj.session.pk)
    classroom = StudentClass.objects.get(pk=resultObj.studentclass.pk)
    classteacher = ClassTeacher.objects.get(teacher=loggedin)

    form = StudentAffectiveForm()


    list_traits = Studentaffective.objects.filter(Q(term=resultObj.term.pk) & Q(studentclass=resultObj.studentclass.pk) & Q(session=resultObj.session.pk) & Q(student=student.pk))

    if request.method =='POST':

        affective = request.POST['affective']
        rating = request.POST['rating']

        affectiveObj = Affective.objects.get(pk=affective)
        ratingObj = Rating.objects.get(pk=rating)



        if ClassTeacher.objects.filter(teacher=loggedin,classroom=resultObj.studentclass.pk,session=resultObj.session.pk,term=resultObj.term.pk).exists():

            # select traits
            affective_traits = Studentaffective.objects.filter(Q(term=resultObj.term.pk) & Q(studentclass=resultObj.studentclass.pk) & Q(session=resultObj.session.pk) & Q(affective=affective) & Q(student=student.pk))

            #check for availability of selected trait
            if affective_traits:
                messages.error(request, 'Selected trait already added!')
                return redirect('add-student-affective',pk=pk)
            else:
                # add the trait to the database
                obj = Studentaffective.objects.create(
                                     affective = affectiveObj,
                                     classteacher = classteacher,
                                     rating = ratingObj,
                                     client = client,
                                     session = session,
                                     student=student,
                                     studentclass=classroom,
                                     term=term
                                         )
                obj.save()
                messages.success(request, 'Trait added successfully!')
                context ={ 'form':form,'list_traits':list_traits}
                return redirect('add-student-affective',pk=pk)
        else:

            messages.error(request, 'You are not allowed to add affective traits')
            context = {'form':form,'student':student,'resultObj':resultObj}
            return render(request,'teacher/addStudentAffectiveDomain.html',context)

    context = {'form':form,'student':student,'resultObj':resultObj,'list_traits':list_traits}
    return render(request,'teacher/addStudentAffectiveDomain.html',context)



#  Add student psycho
@allowed_users(allowed_roles=['teacher'])
def addStudentPsycho(request,pk):

    loggedin = request.user.tutor.pk

    client = Client.objects.get(pk=request.user.tutor.client.pk)

    resultObj = Result.objects.get(pk=pk)
    student = Student.objects.get(pk=resultObj.student.pk)
    term = Term.objects.get(pk=resultObj.term.pk)
    session = Session.objects.get(pk=resultObj.session.pk)
    classroom = StudentClass.objects.get(pk=resultObj.studentclass.pk)
    classteacher = ClassTeacher.objects.get(teacher=loggedin)

    form = StudentPsychomotorForm()


    list_traits = Studentpsychomotor.objects.filter(Q(term=resultObj.term.pk) & Q(studentclass=resultObj.studentclass.pk) & Q(session=resultObj.session.pk) & Q(student=student.pk))

    if request.method =='POST':

        psychomotor = request.POST['psychomotor']
        rating = request.POST['rating']

        psychomotorObj = Psychomotor.objects.get(pk=psychomotor)
        ratingObj = Rating.objects.get(pk=rating)



        if ClassTeacher.objects.filter(teacher=loggedin,classroom=resultObj.studentclass.pk,session=resultObj.session.pk,term=resultObj.term.pk).exists():

            # select traits
            psycho_traits = Studentpsychomotor.objects.filter(Q(term=resultObj.term.pk) & Q(studentclass=resultObj.studentclass.pk) & Q(session=resultObj.session.pk) & Q(psychomotor=psychomotor) & Q(student=student.pk))

            #check for availability of selected trait
            if psycho_traits:
                messages.error(request, 'Selected trait already added!')
                return redirect('add-student-psycho',pk=pk)
            else:
                # add the trait to the database
                obj = Studentpsychomotor.objects.create(
                                     psychomotor = psychomotorObj,
                                     classteacher = classteacher,
                                     rating = ratingObj,
                                     client = client,
                                     session = session,
                                     student=student,
                                     studentclass=classroom,
                                     term=term
                                         )
                obj.save()
                messages.success(request, 'Psychomotor Trait added successfully!')
                context ={ 'form':form,'list_traits':list_traits}
                return redirect('add-student-psycho',pk=pk)
        else:

            messages.error(request, 'You are not allowed to add psychomotor traits')
            context = {'form':form,'student':student,'resultObj':resultObj}
            return render(request,'teacher/addStudentPsychomotorDomain.html',context)

    context = {'form':form,'student':student,'resultObj':resultObj,'list_traits':list_traits}
    return render(request,'teacher/addStudentPsychomotorDomain.html',context)



# get subjects on class change
def get_subjects(request,pk):
    loggedin = request.user.tutor.pk

    result = list(Subject.objects.filter(subjectteacher__classroom_id=pk).filter(subjectteacher__teacher_id=loggedin).values())
    #lg_data = list(Lga.objects.filter(state_id=pk).values())


    return JsonResponse({'data':result})

# find subject and class average
def subjectAverage(subj,classroom):
    # scores = Scores.objects.get(pk=id)
    # get sctive term and session
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    # get scores based on subject
    # scores = Scores.objects.filter(subject=subj,studentclass=classroom,term=activeTerm,session=activeSession).distinct('student').aggregate(Sum('subjAverage'))

    scores = Scores.objects.filter(subject=subj,studentclass=classroom,term=activeTerm,session=activeSession).aggregate(scoresav=Avg('subjecttotal'))

    av = scores['scoresav']

    # scoresAv = scores.aggregate(Sum('subjAverage'))

    return av


# terminal average
def terminalAverage(studentid,classroom):

    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    # get scores based on subject
    # scores = Scores.objects.filter(subject=subj,studentclass=classroom,term=activeTerm,session=activeSession).distinct('student').aggregate(Sum('subjAverage'))

    scores = Scores.objects.filter(student=studentid,studentclass=classroom,term=activeTerm,session=activeSession).aggregate(term_sum=Sum('subjecttotal'))

    term_sum = scores['term_sum']
    # get subject per class
    no_subj_per_class = SubjectPerClass.objects.get(sch_class=classroom)

    class_av = term_sum/no_subj_per_class.no_subject

    # TODO MOVE CODE TO UPDATE TERMINAL AVERAGE HERE
    result = Result.objects.filter(student=studentid,studentclass=classroom,term=activeTerm,session=activeSession).update(termaverage=class_av)


    # return av


#  subject positioning
def subjectPosition(subject, classroom):


    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    scores = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession)
    ordered_scores = []
    counter = 1
    repeated_counter = 0
    # index_counter = 0
    previous_score = Scores.objects.none()
    for score in scores.order_by("-subjecttotal"):
        # repeated_counter = 0
        if counter == 1:
            # this is the first iteration, just assign the first position
            position = counter
             # update the database
            score_entity = Scores.objects.get(pk=score.pk)
            score_entity.subjectposition = position
            score_entity.save()
            # ordered_scores.append({
            # "position": position,
            # "id": score.pk,
            # "subjecttotal": score.subjecttotal
            # })
            previous_score = score
            counter += 1


        else:

            # check for duplicate
            if score.subjecttotal == previous_score.subjecttotal:
                # update database
                score_entity = Scores.objects.get(pk=score.pk)
                score_entity.subjectposition = position
                score_entity.save()

                # position = counter
                # ordered_scores.append({
                # "position": position,
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })
                # position = previous_score.position
                repeated_counter +=1

            else:
                position = counter + repeated_counter
                # update database
                score_entity = Scores.objects.get(pk=score.pk)
                score_entity.subjectposition = position
                score_entity.save()

                # ordered_scores.append({
                # "position": position,
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })

                previous_score = score
                # previous_position = position
                # repeated_counter = position

                counter += 1
    # return render(request, "template.html", {"players": ordered_players})
    # return ordered_scores


# assign terminal result position
def terminalPosition(classroom):


    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    results = Result.objects.filter(studentclass=classroom,term=activeTerm,session=activeSession)
    ordered_scores = []
    counter = 1
    repeated_counter = 0

    previous_score = Result.objects.none()
    for result in results.order_by("-termtotal"):
        # repeated_counter = 0
        if counter == 1:
            # this is the first iteration, just assign the first position
            position = counter
             # update the database
            result_entity = Result.objects.get(pk=result.pk)
            result_entity.termposition = position
            result_entity.save()


            # ordered_scores.append({
            # "position": position,
            # "id": score.pk,
            # "subjecttotal": score.subjecttotal
            # })
            previous_score = result
            counter += 1
        else:

            # check for duplicate
            if result.termtotal == previous_score.termtotal:
                # update database
                result_entity = Result.objects.get(pk=result.pk)
                result_entity.termposition = position
                result_entity.save()

                # position = counter
                # ordered_scores.append({
                # "position": position,
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })
                # position = previous_score.position
                repeated_counter +=1

            else:
                position = counter + repeated_counter
                # update database
                result_entity = Result.objects.get(pk=result.pk)
                result_entity.termposition = position
                result_entity.save()

                # ordered_scores.append({
                # "position": position,
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })

                previous_score = result
                # previous_position = position
                # repeated_counter = position
                counter += 1

# update ratings
def scoresRating(subject,classroom):

    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    minMax = minMaxScores(subject,classroom)

    # TODO: Use select for update because of transaction
    scores = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession)

    for scoresObj in scores:

        if scoresObj.subjecttotal <= 39:
            scoresObj.subjectgrade = 'E'
            scoresObj.subjectrating = 'Poor'
            # scoresObj.highest_inclass = minMax['max_scores']
            # scoresObj.lowest_inclass = minMax['min_scores']
            scoresObj.save()
        elif scoresObj.subjecttotal >= 40 and scoresObj.subjecttotal <= 54.9:
            scoresObj.subjectgrade = 'D'
            scoresObj.subjectrating = 'Fair'
            scoresObj.save()
        elif scoresObj.subjecttotal >= 39 and scoresObj.subjecttotal <= 64.9:
            scoresObj.subjectgrade = 'C'
            scoresObj.subjectrating = 'Good'
            scoresObj.save()
        elif scoresObj.subjecttotal >= 65 and scoresObj.subjecttotal <= 74.9:
            scoresObj.subjectgrade = 'B'
            scoresObj.subjectrating = 'Very Good'
            scoresObj.save()
        elif scoresObj.subjecttotal >= 75 and scoresObj.subjecttotal <= 100:

            scoresObj.subjectgrade = 'A'
            scoresObj.subjectrating = 'Excellent'
            scoresObj.save()
        else:
            scoresObj.subjectgrade = 'NA'
            scoresObj.subjectrating = 'NA'
            scoresObj.save()


# Minimum and Maximum scores
def minMaxScores(subject,classroom):

    # min_max = []

    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    # get scores based on subject
    # scores = Scores.objects.filter(subject=subj,studentclass=classroom,term=activeTerm,session=activeSession).distinct('student').aggregate(Sum('subjAverage'))

    min_max = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession).aggregate(min_scores=Min('subjecttotal'),max_scores=Max('subjecttotal'))

    scores = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession).update(highest_inclass=min_max['max_scores'],lowest_inclass=min_max['min_scores'])



    # return min_max


# update subject average
def processScores(subjectObj,classroomObj):

    # get active term and session
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    subjavg = subjectAverage(subjectObj,classroomObj)

    scores = Scores.objects.filter(subject=subjectObj,studentclass=classroomObj,term=activeTerm,session=activeSession).update(subjaverage=subjavg)

     # update position and grading
    subjectPosition(subjectObj,classroomObj)

    # Update  grades
    scoresRating(subjectObj,classroomObj)

    # update min and max
    minMaxScores(subjectObj,classroomObj)



# Process terminal result
def processTerminalResult(scoresObj):


    # Find record in the result table
    #
    result = Result.objects.filter(student=scoresObj.student, studentclass=scoresObj.studentclass, term=scoresObj.term,session=scoresObj.session)

    scores = Scores.objects.filter(student=scoresObj.student,studentclass=scoresObj.studentclass,term=scoresObj.term,session=scoresObj.session).aggregate(subject_total=Sum('subjecttotal'))

    # print(scores['subject_total'])

    # check for existence of record
    if result:
        # update the record
        result.update(termtotal=scores['subject_total'])

        # update terminal average
        terminalAverage(scoresObj.student,scoresObj.studentclass)
        # update  term position
        terminalPosition(scoresObj.studentclass)
    else:
        # get class teacher
        # TODO: Add class teacher when creating comments
        class_teacher = ClassTeacher.objects.filter(classroom=scoresObj.studentclass,term=scoresObj.term,session=scoresObj.session)
        for i in class_teacher:
            teacher = i.teacher

        # create a new record
        resultObj = Result.objects.create(
                                 termtotal = scores['subject_total'],
                                 classteacher = ClassTeacher.objects.get(pk=teacher.id),
                                 session = scoresObj.session,
                                 studentclass = scoresObj.studentclass,
                                 term = scoresObj.term,
                                 client = scoresObj.client,
                                 student = scoresObj.student
                                     )
        new_Result = resultObj.save()

        # update term average
        terminalAverage(scoresObj.student,scoresObj.studentclass)

        # update  term position
        terminalPosition(scoresObj.studentclass)



# auto add comments
def autoAddComment(classroom,session,term):

    # select result
    resultFilter = Result.objects.select_for_update().filter(studentclass=classroom,session=session,term=term)


    passed = resultFilter.filter(termaverage__gte=40).update(classteachercomment='Passed',headteachercomment='Passed')

    failed = resultFilter.filter(termaverage__lte=39.9).update(classteachercomment='Failed',headteachercomment='Failed')





#   TODO: REMOVE DELETE RESULT METHOD
# delete result object
def deleteResult(studentid,classroom):

     # get sctive term and session
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    result = Result.objects.filter(student=studentid,studentclass=classroom,term=activeTerm,session=activeSession).first()

    if result:
        result.delete()
