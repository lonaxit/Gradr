from django.forms import ModelForm
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms



# class TermForm(forms.Form):
#
#     term = forms.CharField(label='Term',
#                            max_length=100, required=True,
#                            widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter new term','id':'term'}))


# new term form
class TermForm(ModelForm):

    # term = forms.CharField(label='Term',
    #                        max_length=100, required=True,
    #                        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter new term','id':'term'}))
    class Meta:
        model = Term
        fields = '__all__'
        exclude = ['client']
        widgets= {'term': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter new term','id':'term'}),
                # 'venuetypes' : forms.Select(queryset=Venuetypes.objects.all,
                #                                     attrs={'class' : 'venue_type_select'}
                #                                     )
                  }

# session form
class SessionForm(ModelForm):

    session = forms.CharField(label='Session',
                               max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter new session','id':'session'}))
    # status = forms.BooleanField(label='Status',
    #
    #                            widget=forms.Select(attrs={'class': 'form-control','id':'status'}),
    #                            queryset=Session.objects.values_list('status'),
    #                            )


    class Meta:
        model = Session
        fields = '__all__'
        exclude = ['client']
        # widgets= {'session': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter New term','id':'term'}),
                  # 'status' : forms.ChoiceField(queryset=Session.objects.values_list('status'),
                  #                                      attrs={'class' : 'form-ocontrol'}
                  #                                      )

                      # }

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



class AttendanceSettingForm(forms.ModelForm):

    days_open = forms.CharField(label='Days Open',
             max_length=200,
             widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Days Open','id':'days_open'}))

    days_closed = forms.CharField(label='Days Closed',
                      max_length=200,
                      widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter Days Closed','id':'days_closed'}))
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

#
    class Meta:
        model = AttendanceSetting
        fields = '__all__'
        exclude = ['client']
        # widgets= {
        #         'term': forms.TextInput(attrs={'class':'form-control','id':'term'}),
        #         'days_open' : forms.NumberInput(attrs={'class' : 'form-control','id':'days_open'}),
        #         'days_closed': forms.NumberInput(attrs={'class':'form-control','id':'days_closed'}),
        #           }

class ResumptionSettingForm(forms.ModelForm):

    term_begins = forms.DateField(
        widget=forms.DateInput(
        # format='%Y-%m-%d',
        attrs={
        'class': 'form-control',
        'id':'term_begins','placeholder':'Select Date'}),
        # input_formats=('%Y-%m-%d', )
        )
    term_ends = forms.DateField(
        widget=forms.DateInput(
        # format='%Y-%m-%d',
        attrs={
        'class': 'form-control',
        'id':'term_ends','placeholder':'Select Date'}),
        # input_formats=('%Y-%m-%d', )
        )
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

    class Meta:
        model = ResumptionSetting
        fields = '__all__'
        exclude = ['client']
