from django.db import models
from django.contrib.auth.models import User
from accounts.models import *

from datetime import datetime

# Create your models here.

# Model to hold terms

class Guardian(models.Model):
    GENDER = (
                ('M','MALE'),
                ('F','FEMALE'),
                )  
    surname = models.CharField(max_length=100,null=True,blank=True)
    firstname = models.CharField(max_length=100,null=True,blank=True)
    othername = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,null=True,on_delete=models.DO_NOTHING)
    student = models.ForeignKey("accounts.Student",on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.surname

class Term(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,null=True,on_delete=models.DO_NOTHING)
    term = models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.term


class Session(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    session = models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.session


class StudentClass(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    class_name = models.CharField(max_length=100,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.class_name


# subject model
class Subject(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=100,null=True,blank=True)
    subject_code = models.CharField(max_length=6)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject

# subject per class
class SubjectPerClass(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    sch_class = models.ForeignKey(StudentClass,on_delete=models.CASCADE)
    no_subject = models.IntegerField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.sch_class.class_name

class AttendanceSetting(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term,on_delete=models.DO_NOTHING)
    days_open = models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True)
    days_closed = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.days_open


class ResumptionSetting(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term,on_delete=models.DO_NOTHING)
    term_begins = models.DateField(blank=True,null=True)
    term_ends = models.DateField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.term_begins

class Country(models.Model):

    country = models.CharField(max_length=200,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.country

class State(models.Model):

    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    state = models.CharField(max_length=200,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.state

# lga
class Lga(models.Model):
    # country = models.ForeignKey(Country,on_delete=models.CASCADE)
    # state = models.ForeignKey(State,on_delete=models.CASCADE)
    lga = models.CharField(max_length=200,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.lga

# city
class City(models.Model):
    # created_by = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    city = models.CharField(max_length=200,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    # date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.lga

# assign subject to teachers model
class SubjectTeacher(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    classroom = models.ForeignKey(StudentClass,on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey("accounts.Teacher",on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50, default='Active')
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.teacher.surname


# assign class teacher
class ClassTeacher(models.Model):
    createdby = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING)
    client = models.ForeignKey("accounts.Client",on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term,on_delete=models.DO_NOTHING)
    classroom = models.ForeignKey(StudentClass,on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey("accounts.Teacher",on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.teacher.surname
    
    
