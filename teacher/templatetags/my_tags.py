from django import template
register = template.Library()

from accounts.models import *
from administrator.models import *
from teacher.models import *
from django.db.models import Q, Sum, Avg, Max, Min

@register.simple_tag
def affective_domain(term,session,student):
    affective_list = Studentaffective.objects.filter(student=student,term=term,session=session).count()
    return affective_list



@register.simple_tag
def psycho_domain(term,session,student):
    psycho_list = Studentpsychomotor.objects.filter(student=student,term=term,session=session).count()
    return psycho_list

@register.simple_tag
def totalStudents():
    students = Student.objects.all().count()
    return students

@register.simple_tag
def activeStudents():
    students = Student.objects.all()
    i =0
    for student in students:
        if student.user.is_active == True:
            i =i+1 
        else:
            pass
    return i

@register.simple_tag
def inActiveStudents():
    students = Student.objects.all()
    i =0
    for student in students:
        
        if student.user.is_active == False:
            i =i+1 
        else:
            pass
    return i
   
# total Teachers
@register.simple_tag
def totalStaff():
    students = Teacher.objects.all().count()
    return students


@register.simple_tag
def staff_sign(teacherid):
    teacherObj = Teacher.objects.get(pk=teacherid)
    return teacherObj.surname


@register.simple_tag
def getSubjTotal(scoresList,subjid,studentid):
    filteredObj = scoresList.filter(student=studentid,subject=subjid).first()
    if filteredObj:
        return filteredObj.subjecttotal
    return "Null"

@register.simple_tag
def getTermTotal(resultList,studentid):
    
    resultObj = resultList.filter(student=studentid).first()
    if resultObj:
        return resultObj.termtotal
    return "Null"
 
@register.simple_tag
def getTermPosition(resultList,studentid):
    resultObj = resultList.filter(student=studentid).first()
    if resultObj:
        return resultObj.termposition
    return "Null" 

@register.simple_tag
def firstTermTotal(annualResult,studentid,subjid):
    resultObj = annualResult.filter(student=studentid,term=1,subject=subjid).first()
    if resultObj:
        return resultObj.subjecttotal
    return "Null" 

@register.simple_tag
def secondTermTotal(scores,studentid,subjid):
    resultObj = scores.filter(student=studentid,term=2,subject=subjid).first()
    if resultObj:
        return resultObj.subjecttotal
    return "Null" 

@register.simple_tag
def thirdTermTotal(scores,studentid,subjid):
    resultObj = scores.filter(student=studentid,term=3,subject=subjid).first()
    if resultObj:
        return resultObj.subjecttotal
    return "Null" 


@register.simple_tag
def annualTotal(scores,studentid):
    resultObj = scores.filter(student=studentid).aggregate(annual_sum=Sum('subjecttotal'))
    return resultObj['annual_sum']

@register.simple_tag
def annualAv(resultList,studentid):
    resultObj = resultList.filter(student=studentid).first()
    if resultObj:
        return resultObj.termaverage
    return "Null" 

@register.simple_tag
def annualSubjectTotal(scores,studentid,subjid):
    resultObj = scores.filter(student=studentid,subject=subjid).aggregate(annualsubject_sum=Sum('subjecttotal'))
    return resultObj['annualsubject_sum']
    
    # if resultObj:
    #     return resultObj.subjecttotal
    # return "Null"


    