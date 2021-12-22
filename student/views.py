from django.shortcuts import render,redirect

from accounts.models import Client,Student
from teacher.models import *
from administrator.models import Session,Term,StudentClass,Subject,SubjectTeacher,ClassTeacher
from .models import *
from django.db.models import Q, Sum, Avg, Max, Min
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

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# from django.contrib.staticfiles import finder

# import transactions
from django.db import transaction

import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


@login_required(login_url='login')
# @admin_only
@allowed_users(allowed_roles=['student'])
def studentHome(request):
    student = request.user.learner
    
    result = Result.objects.filter(student=student)
    
    context = {'results':result}
    return render(request,'student/student_home.html',context)


# result list page
@login_required(login_url='login')
# @admin_only
@allowed_users(allowed_roles=['student'])
def resultList(request):
    student = request.user.learner
    
    result = Result.objects.filter(student=student)
    
    context = {'results':result}
    return render(request,'student/resultList.html',context)


# student profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def studentProfile(request):
    # student_loggedin = request.user.learner.pk
    

    return render(request, 'student/student_profile.html')



# Print result
@login_required(login_url='login')
def printResult(request,pk):
    result = Result.objects.get(pk=pk)
    academic_scores = Scores.objects.filter(student=result.student.pk,studentclass=result.studentclass.pk,term=result.term.pk,session=result.session.pk)
    student_count = Scores.objects.filter(studentclass=result.studentclass.pk,term=result.term.pk,session=result.session.pk).distinct('student').count()
    affective = Studentaffective.objects.filter(student=result.student,studentclass=result.studentclass,session=result.session,term=result.term)

    psychomotor = Studentpsychomotor.objects.filter(student=result.student,studentclass=result.studentclass,session=result.session,term=result.term)
    termBegins = ResumptionSetting.objects.get(term=result.term.pk,session=result.session.pk)
    
    attendanceSettings = AttendanceSetting.objects.get(term=result.term.pk,session=result.session.pk)

    # academic_scores = Scores.objects.filter(student=1,studentclass=1,term=1,session=1)
    context={
        'scores':academic_scores,
        'result':result,
        'student_count':student_count,
        'affective':affective,
        'psychomotor':psychomotor,
        'termbegins':termBegins,
        'attendanceSetting':attendanceSettings
    }
    return render(request,'teacher/print.html',context)


# view All asessements
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def allAssessment(request):
    studentId = request.user.learner.pk
    allAssessment = Scores.objects.filter(student=studentId).distinct('term')

    context ={
    'assessment':allAssessment,
    }

    return render(request, 'student/assessmentList.html',context)

# Detail Assessment

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def detailAssessment(request,classroom,term,session):
    studentId = request.user.learner.pk
    allAssessment = Scores.objects.filter(student=studentId,studentclass=classroom,term=term,session=session)

    context ={
    'assessment':allAssessment,
    }

    return render(request, 'student/detailAssessment.html',context)



# Detail Result
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def detailResult(request,classroom,term,session):
    studentId = request.user.learner.pk
    
    allAssessment = Scores.objects.filter(student=studentId,studentclass=classroom,term=term,session=session)

    result = Result.objects.get(student=studentId,studentclass=classroom,term=term,session=session)
    
    student_count = Scores.objects.filter(studentclass=result.studentclass,term=result.term,session=result.session).distinct('student').count()
    
    context ={
    'assessment':allAssessment,
    'result':result,
    'count':student_count
    }

    return render(request, 'student/detailResult.html',context)