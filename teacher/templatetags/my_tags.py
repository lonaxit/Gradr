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

