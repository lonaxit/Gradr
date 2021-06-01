from django.db import models
from django.contrib.auth.models import User
from accounts.models import *

from datetime import datetime

# Create your models here.

# Model to hold terms

class Term(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    term = models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    # list_date = models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.term


class Session(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    session = models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(default=False,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    # list_date = models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.session


class StudentClass(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    class_name = models.CharField(max_length=100,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    # list_date = models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.class_name



class Subject(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=100,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    # list_date = models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return self.subject

class AttendanceSetting(models.Model):
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term,on_delete=models.DO_NOTHING)
    days_open = models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True)
    days_closed = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.days_open


class ResumptionSetting(models.Model):
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    term = models.ForeignKey(Term,on_delete=models.DO_NOTHING)
    term_begins = models.DateField(blank=True,null=True)
    term_ends = models.DateField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return self.term_begins
