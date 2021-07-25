from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from administrator.models import *
from django import forms




# student profile form
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
                  widget=forms.NumberInput(attrs={'class': 'form-control','id':'student'}))
    firstscore = forms.DecimalField(
              label='First CA',
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'firstscore'}))
    secondscore = forms.DecimalField(

              label='Second CA',
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'secondscore'}))
    thirdscore = forms.DecimalField(
              label='Third CA',
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'thirdscore'}))
    totalca = forms.DecimalField(
              label='Total CA',
              # disabled='True',
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'totalca'}))
    examscore = forms.DecimalField(
              label='Exam Score',
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'examscore'}))
    subjecttotal = forms.DecimalField(
              label='Subject Total',
              # disabled='True',
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'subjecttotal'}))

    # def clean_subject(self):
    #     data = self.cleaned_data['subject']
    #     # data = Subject.objects.get(id=subj_id)
    #
    #     # Check if a date is not in the past.
    #     if not data:
    #         raise ValidationError(_('Invalid date - renewal in past'))
    #
    #     # # Check if a date is in the allowed range (+4 weeks from today).
    #     # if data > datetime.date.today() + datetime.timedelta(weeks=4):
    #     #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
    #     #
    #     # Remember to always return the cleaned data.
    #     return data


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
