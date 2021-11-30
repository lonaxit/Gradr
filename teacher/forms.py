from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from administrator.models import *
from django import forms




# Scores form
class ScoresForm(forms.ModelForm):

    subject = forms.CharField(label='Subject',

             widget=forms.Select(attrs={'class': 'form-control','id':'subject'}))

    studentclass = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Choose Class',
                  widget=forms.Select(attrs={'class': 'form-control','id':'stud-class'}))
    studentnumber = forms.IntegerField(
                  label='Student Number',
                  required=False,
                  widget=forms.NumberInput(attrs={'class': 'form-control','id':'student'}))
    firstscore = forms.DecimalField(
              label='First CA',
              required=False,
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'firstscore'}))
    secondscore = forms.DecimalField(

              label='Second CA',
              required=False,
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'secondscore'}))
    thirdscore = forms.DecimalField(
              label='Third CA',
              required=False,
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'thirdscore'}))
    totalca = forms.DecimalField(
              label='Total CA',
              # disabled='True',
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'totalca'}))
    examscore = forms.DecimalField(
              label='Exam Score',
              required=False,
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'examscore'}))
    subjecttotal = forms.DecimalField(
              label='Subject Total',
              # disabled='True',
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'subjecttotal'}))

    class Meta:
        model = Scores
        fields = '__all__'
        exclude = ['client','student','term','session','subjectteacher','subjaverage','subjectposition']


class ScoresFilterForm(forms.Form):
    classroom = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Choose Class',
                  widget=forms.Select(attrs={'class': 'form-control','id':'classroom'}))
    subject = forms.ModelChoiceField(
                      queryset=Subject.objects.all(),
                      empty_label=None,
                      required=True,
                      to_field_name='id',
                      label='Choose Subject',
                      widget=forms.Select(attrs={'class': 'form-control','id':'subject'}))
    term = forms.ModelChoiceField(
                  queryset=Term.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select Term',
                  widget=forms.Select(attrs={'class': 'form-control','id':'term'}))
    session = forms.ModelChoiceField(
                  queryset=Session.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select session',
                  widget=forms.Select(attrs={'class': 'form-control','id':'session'}))
    

class ResultFilterForm(forms.Form):
    classroom = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Choose Class',
                  widget=forms.Select(attrs={'class': 'form-control','id':'classroom'}))
    term = forms.ModelChoiceField(
                  queryset=Term.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select Term',
                  widget=forms.Select(attrs={'class': 'form-control','id':'term'}))
    session = forms.ModelChoiceField(
                  queryset=Session.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select session',
                  widget=forms.Select(attrs={'class': 'form-control','id':'session'}))
    
    # filter form migrate
class ScoresProcessForm(forms.Form):
    classroom = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Choose Class',
                  widget=forms.Select(attrs={'class': 'form-control','id':'classroom'}))
    term = forms.ModelChoiceField(
                  queryset=Term.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select Term',
                  widget=forms.Select(attrs={'class': 'form-control','id':'term'}))
    session = forms.ModelChoiceField(
                  queryset=Session.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select session',
                  widget=forms.Select(attrs={'class': 'form-control','id':'session'}))
    subject = forms.ModelChoiceField(
                  queryset=Subject.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select subject',
                  widget=forms.Select(attrs={'class': 'form-control','id':'subject'}))

# annual result summary form
class AnnualResultFilterForm(forms.Form):
    classroom = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Choose Class',
                  widget=forms.Select(attrs={'class': 'form-control','id':'classroom'}))
    # term = forms.ModelChoiceField(
    #               queryset=Term.objects.all(),
    #               empty_label=None,
    #               required=True,
    #               to_field_name='id',
    #               label='Select Term',
    #               widget=forms.Select(attrs={'class': 'form-control','id':'term'}))
    session = forms.ModelChoiceField(
                  queryset=Session.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select session',
                  widget=forms.Select(attrs={'class': 'form-control','id':'session'}))

# Comment form
class CommentForm(forms.ModelForm):

    classteachercomment = forms.CharField(label='Comment',
             max_length=100, required=True,
             widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Enter Comments','id':'comments'}))
    class Meta:
        model = Result
        exclude = ['client','student','term','session','studentclass','classteacher','termtotal','termposition','termaverage','headteachercomment']


# Add Affective domain
class StudentAffectiveForm(forms.ModelForm):
    
    affective = forms.ModelChoiceField(
                  queryset=Affective.objects.all(),
                  empty_label=None,
                  to_field_name='id',
                  label='Affective Domain',
                  widget=forms.Select(attrs={'class': 'form-control','id':'affective-domain'}))
    rating = forms.ModelChoiceField(
                  queryset=Rating.objects.all(),
                  empty_label=None,
                  to_field_name='id',
                  label='Rating',
                  widget=forms.Select(attrs={'class': 'form-control','id':'rating'}))

    class Meta:
        model = Studentaffective
        fields = '__all__'
        exclude = ['client','student','term','session','classteacher','studentclass']
        
        
class StudentPsychomotorForm(forms.ModelForm):
    
    psychomotor = forms.ModelChoiceField(
                  queryset=Psychomotor.objects.all(),
                  empty_label=None,
                  to_field_name='id',
                  label='Psychomotor Domain',
                  widget=forms.Select(attrs={'class': 'form-control','id':'psychomotor-domain'}))
    rating = forms.ModelChoiceField(
                  queryset=Rating.objects.all(),
                  empty_label=None,
                  to_field_name='id',
                  label='Rating',
                  widget=forms.Select(attrs={'class': 'form-control','id':'rating'}))

    class Meta:
        model = Studentpsychomotor
        fields = '__all__'
        exclude = ['client','student','term','session','classteacher','studentclass']
        
    
# Class enrollment form
class ClassEnrollmentForm(forms.ModelForm):
    class_room = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Choose Class',
                  widget=forms.Select(attrs={'class': 'form-control','id':'class_room'}))
    student= forms.CharField(label='Reg No',
             max_length=10,
             required=True,
             widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Reg Number eg 876','id':'student'}))
    
    class Meta:
        model = Classroom
        fields = '__all__'
        exclude = ['client','term','session']
