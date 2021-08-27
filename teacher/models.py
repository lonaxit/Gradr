from django.db import models
from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
from administrator.models import *

from datetime import datetime
# Create your models here.

class Scores(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    client = models.ForeignKey("accounts.Client",on_delete=models.DO_NOTHING)
    student = models.ForeignKey("accounts.Student",on_delete=models.DO_NOTHING)
    term = models.ForeignKey("administrator.Term",on_delete=models.DO_NOTHING)
    session = models.ForeignKey("administrator.Session",on_delete=models.DO_NOTHING)
    studentclass = models.ForeignKey("administrator.StudentClass",on_delete=models.DO_NOTHING)
    subject = models.ForeignKey("administrator.Subject",on_delete=models.DO_NOTHING)
    subjectteacher = models.ForeignKey("administrator.SubjectTeacher",on_delete=models.DO_NOTHING)
    firstscore = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    secondscore = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    thirdscore = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    totalca = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    examscore = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    subjecttotal = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    subjaverage = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    subjectposition = models.IntegerField(null=True)
    subjectgrade = models.CharField(max_length=10,null=True)
    subjectrating = models.CharField(max_length=10,null=True)
    approval_status = models.CharField(default="No", max_length=10,null=True)
    highest_inclass = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    lowest_inclass =  models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.student.sur_name


class Result(models.Model):
    
    client = models.ForeignKey("accounts.Client",on_delete=models.DO_NOTHING)
    student = models.ForeignKey("accounts.Student",on_delete=models.DO_NOTHING)
    term = models.ForeignKey("administrator.Term",on_delete=models.DO_NOTHING)
    session = models.ForeignKey("administrator.Session",on_delete=models.DO_NOTHING)
    studentclass = models.ForeignKey("administrator.StudentClass",on_delete=models.DO_NOTHING)
    classteacher = models.ForeignKey("administrator.ClassTeacher",on_delete=models.DO_NOTHING)
    termtotal = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    termaverage = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    termposition = models.IntegerField(null=True)
    classteachercomment = models.CharField(max_length=200,null=True,blank=True)
    headteachercomment = models.CharField(max_length=200,null=True,blank=True)
    attendance = models.CharField(max_length=20,null=True,blank=True)
    status = models.CharField(max_length=20,null=True,blank=True)
    owing_status = models.CharField(default='open', max_length=20,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.student.sur_name


class Rating(models.Model):
    description = models.CharField(max_length=100,null=True)
    scores = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.description
    
    
class Psychomotor(models.Model):
    
    skill = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.skill
    

class Affective(models.Model):
    
    domain = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.domain
    


class Studentaffective(models.Model):
    
    client = models.ForeignKey("accounts.Client",on_delete=models.DO_NOTHING)
    student = models.ForeignKey("accounts.Student",on_delete=models.DO_NOTHING)
    term = models.ForeignKey("administrator.Term",on_delete=models.DO_NOTHING)
    session = models.ForeignKey("administrator.Session",on_delete=models.DO_NOTHING)
    studentclass = models.ForeignKey("administrator.StudentClass",on_delete=models.DO_NOTHING)
    classteacher = models.ForeignKey("administrator.ClassTeacher",on_delete=models.DO_NOTHING)
    affective = models.ForeignKey(Affective,on_delete=models.DO_NOTHING)
    rating = models.ForeignKey(Rating,on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.student.sur_name


class Studentpsychomotor(models.Model):
    
    client = models.ForeignKey("accounts.Client",on_delete=models.DO_NOTHING)
    student = models.ForeignKey("accounts.Student",on_delete=models.DO_NOTHING)
    term = models.ForeignKey("administrator.Term",on_delete=models.DO_NOTHING)
    session = models.ForeignKey("administrator.Session",on_delete=models.DO_NOTHING)
    studentclass = models.ForeignKey("administrator.StudentClass",on_delete=models.DO_NOTHING)
    classteacher = models.ForeignKey("administrator.ClassTeacher",on_delete=models.DO_NOTHING)
    psychomotor = models.ForeignKey(Psychomotor,on_delete=models.DO_NOTHING)
    rating = models.ForeignKey(Rating,on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.student.sur_name