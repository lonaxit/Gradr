from django.db import models
from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
from administrator.models import *

from datetime import datetime
# Create your models here.

class Scores(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    term = models.ForeignKey("administrator.Term",on_delete=models.DO_NOTHING)
    session = models.ForeignKey("administrator.Session",on_delete=models.DO_NOTHING)
    studentclass = models.ForeignKey("administrator.StudentClass",on_delete=models.DO_NOTHING)
    subject = models.ForeignKey("administrator.Subject",on_delete=models.DO_NOTHING)
    subjectteacher = models.ForeignKey("administrator.SubjectTeacher",on_delete=models.DO_NOTHING)
    firstscore = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    secondscore = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    thirdscore = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    totalca = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    examscore = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    subjecttotal = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    subjaverage = models.DecimalField(max_digits=4, decimal_places=2,null=True,blank=True)
    subjectposition = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.student.sur_name
