from django.shortcuts import render,redirect

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

# import for creating a group
from django.contrib.auth.models import Group

# import models
from accounts.models import *
from administrator.models import *
from .models import *
from django.db.models import Q

#custom decorator
from accounts.decorators import unauthenticated_user,allowed_users,admin_only
# Create your views here.

@login_required(login_url='login')
# @admin_only
@allowed_users(allowed_roles=['teacher'])
def teacherHome(request):
    students = Student.objects.all()
    context = {'students':students}
    return render(request,'teacher/teacher_home.html',context)


# add new scores
@allowed_users(allowed_roles=['teacher'])
def addScores(request):

    loggedin = request.user.teacher

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

        teacherObj = SubjectTeacher.objects.get(id=loggedin.id)
        subjectObj = Subject.objects.get(id=subj)
        classroomObj = StudentClass.objects.get(id=studclass)
        studObj = Student.objects.get(id=studid)

        # check if record for the subject exist
        scores = Scores.objects.filter(Q(term=activeTerm) & Q(studentclass=classroomObj)
        & Q(session=activeSession) & Q(subject=subjectObj) & Q(student=studObj) )

        if scores:
            messages.error(request, 'Record exist')
            return redirect('new-scores')
        else:
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
            messages.success(request, 'Scores created')
            # return redirect('assign-subject')
    # context = {'form':form}
    return render(request,'teacher/new_scores.html',context)


# edit scores
@allowed_users(allowed_roles=['teacher'])
def editScores(request,pk):

    loggedin = request.user.teacher
    scores = Scores.objects.get(id=pk)
    form = ScoresForm(instance=scores)

    context = {'form':form}
    if request.method =='POST':

        form = ScoresForm(request.POST,instance=scores)

        # subj = request.POST['subject']
        # studclass = request.POST['studentclass']
        # studid = request.POST['studentnumber']
        # ca1 = request.POST['firstscore']
        # ca2 = request.POST['secondscore']
        # ca3 = request.POST['thirdscore']
        # totalass = request.POST['totalca']
        # exam = request.POST['examscore']
        # total = request.POST['subjecttotal']

        # get sctive term and session
        # activeTerm = Term.objects.get(status='True')
        # activeSession = Session.objects.get(status='True')
        #
        # teacherObj = SubjectTeacher.objects.get(id=loggedin.id)
        # subjectObj = Subject.objects.get(id=subj)
        # classroomObj = StudentClass.objects.get(id=studclass)
        # studObj = Student.objects.get(id=studid)
        #
        # # check if record for the subject exist
        # scores = Scores.objects.filter(Q(term=activeTerm) & Q(studentclass=classroomObj)
        # & Q(session=activeSession) & Q(subject=subjectObj) & Q(student=studObj) )
        #
        # if scores:
        #     messages.error(request, 'Record exist')
        #     return redirect('new-scores')
        # else:
        #     obj = Scores.objects.create(
        #                          firstscore = ca1,
        #                          secondscore = ca2,
        #                          thirdscore = ca3,
        #                          totalca = totalass,
        #                          examscore = exam,
        #                          session = activeSession,
        #                          studentclass = classroomObj,
        #                          subject = subjectObj,
        #                          subjectteacher = teacherObj,
        #                          term = activeTerm,
        #                          subjecttotal = total,
        #                          client = loggedin.client,
        #                          student = studObj,
        #                              )
        #     obj.save()
        #     messages.success(request, 'Scores created')
            # return redirect('assign-subject')
    # context = {'form':form}
    return render(request,'teacher/edit_scores.html',context)



# get scores filter form
@allowed_users(allowed_roles=['teacher'])
def scoresFilter(request):

    loggedin = request.user.teacher

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


# get subjects on class change
def get_subjects(request,pk):
    loggedin = request.user.teacher

    result = list(Subject.objects.filter(subjectteacher__classroom_id=pk).filter(subjectteacher__teacher_id=loggedin.id).values())
    #lg_data = list(Lga.objects.filter(state_id=pk).values())


    return JsonResponse({'data':result})
