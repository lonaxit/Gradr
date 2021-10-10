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
@allowed_users(allowed_roles=['student'])
def studentHome(request):
    student = request.user.learner
    
    result = Result.objects.filter(student=student)
    
    context = {'results':result}
    return render(request,'student/student_home.html',context)



# student profile
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def studentProfile(request):

    return render(request, 'student/student_profile.html')

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


