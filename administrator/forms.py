from django.forms import ModelForm
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms



class TermForm(forms.Form):

    term = forms.CharField(label='Term',
                           max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter new term','id':'term'}))

# session form
class SessionForm(forms.Form):

    session = forms.CharField(label='Session',
                           max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter new session','id':'term'}))

class ClassForm(forms.ModelForm):

    class_name = forms.CharField(label='Class',
             max_length=200,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter class','id':'class_name'}))
# field_z = forms.ModelChoiceField(
#     queryset=AnyClass.objects.all(),
#     empty_label=None,
#     required=True,
#     to_field_name='id',
#     label='Select your Z value here',
#     widget=forms.SelectMultiple(attrs={'class': 'myclass'})
# )
#
    class Meta:
        model = StudentClass
        fields = '__all__'
        exclude = ['client']


class SubjectForm(forms.ModelForm):

    subject = forms.CharField(label='Subject',
             max_length=200,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter subject','id':'subject'}))
# field_z = forms.ModelChoiceField(
#     queryset=AnyClass.objects.all(),
#     empty_label=None,
#     required=True,
#     to_field_name='id',
#     label='Select your Z value here',
#     widget=forms.SelectMultiple(attrs={'class': 'myclass'})
# )
#
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['client']
# class form
# class classForm(forms.Form):
#
#     session = forms.CharField(label='Session',
#                            max_length=100, required=True,
#                            widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter new session','id':'term'}))
