from django import template
register = template.Library()

from accounts.models import *
from administrator.models import *
from teacher.models import *

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