from django.forms import ModelForm
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from teacher.models import *
from accounts.models import *
from django import forms


# student photo form
class StudentImageUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Upload Your logo',
                            max_length=100,
                            widget=forms.FileInput(attrs={'class': ''}))
    class Meta:
        model=Student
        fields=['profile_image']
        exclude = ['client','user','reg_no','full_reg_no','sur_name','first_name','other_name','sex','dob','country']
       
# Institution logo form

class LogoUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Upload Your logo',
                            max_length=100,
                            widget=forms.FileInput(attrs={'class': ''}))
    class Meta:
        model=Client
        fields=['profile_image']
        exclude = ['user','school_name','school_type','phone','address','email','city','lga','country','state']
 
# teacher photo form
class TeacherImageUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Upload Your logo',
                            max_length=100,
                            widget=forms.FileInput(attrs={'class': ''}))
    class Meta:
        model=Teacher
        fields=['profile_image']
        exclude = ['client','user','surname','firstname','othername','sex','dob','country'] 

     


# new term form
class TermForm(ModelForm):

    # term = forms.CharField(label='Term',
    #                        max_length=100, required=True,
    #                        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter new term','id':'term'}))
    class Meta:
        model = Term
        fields = '__all__'
        exclude = ['client','createdby']
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
        exclude = ['client','createdby']
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
        exclude = ['client','createdby']


class SubjectForm(forms.ModelForm):

    subject = forms.CharField(label='Subject',
             max_length=200,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter subject','id':'subject'}))
    subject_code = forms.CharField(label='Subject Code',
             max_length=6,required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Subject Code','id':'subject_code'}))
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
        exclude = ['client','createdby']

# subject per class form
class SubjectPerClassForm(forms.ModelForm):

    no_subject = forms.CharField(label='Number of Subjects',
             max_length=10,
             widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter number of subjects','id':'no_subject'}))

    sch_class= forms.ModelChoiceField(
              queryset=StudentClass.objects.all(),
              empty_label=None,
              required=True,
              to_field_name='id',
              label='Select Class',
              widget=forms.Select(attrs={'class': 'form-control','id':'sch_class'}))

#
    class Meta:
        model = SubjectPerClass
        fields = '__all__'
        exclude = ['client','createdby']


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
        exclude = ['client','createdby']
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
        exclude = ['client','createdby']


# student profile form
class StudentProfileForm(forms.ModelForm):
    GENDER = (
            ('M','Male'),
            ('F','Female'),
    )

    BLOODGROUP = (
                ('A+','A+'),
                ('A-','A-'),
                ('AB','AB'),
                ('B+','B+'),
                ('O+','O+'),
                ('O-','O-'),
                )
    RELIGION =(
    ('CHRISTIANITY', 'CHRISTIANITY'),
    ('ISLAM','ISLAM'),
    ('OTHERS','OTHERS')
    )
    address = forms.CharField(label='Address',
             max_length=100,required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter address','id':'address'}))
    sur_name = forms.CharField(label='Surname',
             max_length=100,required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter surname','id':'sur_name'}))

    first_name = forms.CharField(label='Firstname',
             max_length=100, required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter firstname','id':'first_name'}))
    other_name = forms.CharField(label='Othername',
             max_length=100,required=False,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter other_name','id':'other_name'}))
    email = forms.CharField(label='E-Mail',
                required=False,
                 max_length=100,
                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter optional email','id':'email'}))
    phone = forms.CharField(label='Phone Number',
                 required=False,
                 max_length=100,
                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter optional phone number','id':'phone'}))
    dob = forms.DateField(
        widget=forms.DateInput(
        # format='%Y-%m-%d',
        attrs={
        'class': 'form-control',
        'id':'term_begins','placeholder':'Choose date of birth'}),
        # input_formats=('%Y-%m-%d', )
        )
    class_admitted = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Class Admitted',
                  widget=forms.Select(attrs={'class': 'form-control','id':'stud-class'}))
    term_admitted = forms.ModelChoiceField(
                  queryset=Term.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Term Admitted',
                  widget=forms.Select(attrs={'class': 'form-control','id':'term'}))
    session_admitted = forms.ModelChoiceField(
              queryset=Session.objects.all(),
              empty_label=None,
              required=True,
              to_field_name='id',
              label='Session Admitted',
              widget=forms.Select(attrs={'class': 'form-control','id':'session'}))

    country = forms.ModelChoiceField(
              queryset=Country.objects.all(),
              empty_label=None,
              required=True,
              to_field_name='id',
              label='Country',
              widget=forms.Select(attrs={'class': 'form-control','id':'country'}))
    state = forms.ModelChoiceField(
              queryset=State.objects.all(),
              label='State',
              to_field_name='id',
              widget=forms.Select(attrs={'class': 'form-control','id':'state'}))

    lga = forms.CharField(
              # queryset=Lga.objects.all(),
              label='Lga',
              widget=forms.TextInput(attrs={'class': 'form-control','id':'lga'}))
    city = forms.CharField(
              label='City',
              widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter city','id':'city'}))
    sex = forms.ChoiceField(
              label='Choose Sex',
              choices=GENDER,
              widget=forms.Select(attrs={'class': 'form-control','id':'city'}))
    blood_group = forms.ChoiceField(
              label='Blood Group',
              choices=BLOODGROUP,
              widget=forms.Select(attrs={'class': 'form-control','id':'city'}))
    religion = forms.ChoiceField(
              label='Religion',
              choices=RELIGION,
              widget=forms.Select(attrs={'class': 'form-control','id':'religion'}))

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['client','user','reg_no','full_reg_no','profile_image','createdby']


# teacher profile form
class TeacherProfileForm(forms.ModelForm):
    CERTIFICATE = (
                ('SSCE','SSCE'),
                ('NCE','NCE'),
                ('OND','OND'),
                ('HND','HND'),
                ('BSC','BSC'),
                ('B.ED','B.ED'),
                ('MA','MA'),
                ('MSC','MSC'),
                ('PHD','PHD'),
                )
    GENDER = (
            ('M','Male'),
            ('F','Female'),
    )

    address = forms.CharField(label='Address',
             max_length=100,required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter address','id':'address'}))
    surname = forms.CharField(label='Surname',
             max_length=100,required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter surname','id':'sur_name'}))

    firstname = forms.CharField(label='Firstname',
             max_length=100, required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter firstname','id':'first_name'}))
    othername = forms.CharField(label='Othername',
             max_length=100,required=False,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter other_name','id':'other_name'}))
    email = forms.CharField(label='E-Mail',
                required=False,
                 max_length=100,
                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter optional email','id':'email'}))
    phone = forms.CharField(label='Phone Number',
                 required=False,
                 max_length=100,
                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter optional phone number','id':'phone'}))
    dob = forms.DateField(
        widget=forms.DateInput(
        # format='%Y-%m-%d',
        attrs={
        'class': 'form-control',
        'id':'term_begins','placeholder':'Choose date of birth'}),
        # input_formats=('%Y-%m-%d', )
        )

    country = forms.ModelChoiceField(
              queryset=Country.objects.all(),
              empty_label=None,
              required=True,
              to_field_name='id',
              label='Country',
              widget=forms.Select(attrs={'class': 'form-control','id':'country'}))
    state = forms.ModelChoiceField(
              queryset=State.objects.all(),
              label='State',
              to_field_name='id',
              widget=forms.Select(attrs={'class': 'form-control','id':'state'}))

    lga = forms.CharField(
              # queryset=Lga.objects.all(),
              label='Lga',
              widget=forms.TextInput(attrs={'class': 'form-control','id':'lga'}))
    city = forms.CharField(
              label='City',
              widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter city','id':'city'}))
    sex = forms.ChoiceField(
              label='Choose Sex',
              choices=GENDER,
              widget=forms.Select(attrs={'class': 'form-control','id':'city'}))
    certificate = forms.ChoiceField(
              label='Choose Certificate',
              choices=CERTIFICATE,
              widget=forms.Select(attrs={'class': 'form-control','id':'certificate'}))
    discipline = forms.CharField(
              label='Discipline',
              widget=forms.TextInput(attrs={'class': 'form-control','id':'discipline'}))


    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['client','user','createdby']

# Parent/Guardian form

class GuardianProfileForm(forms.ModelForm):
  
    GENDER = (
            ('M','Male'),
            ('F','Female'),
    )

    surname = forms.CharField(label='Surname',
             max_length=100,required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter surname','id':'sur_name'}))

    firstname = forms.CharField(label='Firstname',
             max_length=100, required=True,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter firstname','id':'first_name'}))
    othername = forms.CharField(label='Othername',
             max_length=100,required=False,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter other_name','id':'other_name'}))
    email = forms.CharField(label='E-Mail',
                required=False,
                 max_length=100,
                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter optional email','id':'email'}))
    phone = forms.CharField(label='Phone Number',
                 required=True,
                 max_length=100,
                 widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone number','id':'phone'}))  
    sex = forms.ChoiceField(
              label='Choose Sex',
              choices=GENDER,
              widget=forms.Select(attrs={'class': 'form-control','id':'city'}))
    address = forms.CharField(label='Address',
             max_length=300,required=False,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter address','id':'address'}))
    occupation = forms.CharField(label='Occupation',
             max_length=300,required=False,
             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter occupation','id':'occupation'}))

    class Meta:
        model = Guardian
        fields = '__all__'
        exclude = ['client','student','createdby']


# assign subject
class AssignSubjectForm(forms.ModelForm):

    classroom = forms.ModelChoiceField(
              queryset=StudentClass.objects.all(),
              empty_label=None,
              required=True,
              to_field_name='id',
              label='Select Class',
              widget=forms.Select(attrs={'class': 'form-control','id':'classroom'}))
    subject = forms.ModelChoiceField(
              queryset=Subject.objects.all(),
              label='Subject',
              to_field_name='id',
              widget=forms.Select(attrs={'class': 'form-control','id':'subject'}))
    teacher = forms.ModelChoiceField(
                  queryset=Teacher.objects.all(),
                  label='Select Teacher',
                  to_field_name='id',
                  widget=forms.Select(attrs={'class': 'form-control','id':'teacher'}))
    
    session = forms.ModelChoiceField(
                  queryset=Session.objects.all(),
                  label='Select Session',
                  to_field_name='id',
                  widget=forms.Select(attrs={'class': 'form-control','id':'sch_session'}))
    
    # term = forms.ModelChoiceField(
    #               queryset=Term.objects.all(),
    #               label='Select Session',
    #               to_field_name='id',
    #               widget=forms.Select(attrs={'class': 'form-control','id':'term'}))


    class Meta:
        model = SubjectTeacher
        fields = '__all__'
        exclude = ['client','createdby','status']

# class teacher form
class AssignClassTeacherForm(forms.ModelForm):

    classroom = forms.ModelChoiceField(
              queryset=StudentClass.objects.all(),
              empty_label=None,
              required=True,
              to_field_name='id',
              label='Select Class',
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
              label='Select Session',
              widget=forms.Select(attrs={'class': 'form-control','id':'session'}))

    teacher = forms.ModelChoiceField(
                  queryset=Teacher.objects.all(),
                  label='Select Teacher',
                  to_field_name='id',
                  widget=forms.Select(attrs={'class': 'form-control','id':'teacher'}))


    class Meta:
        model = ClassTeacher
        fields = '__all__'
        exclude = ['client','createdby']

class AdmissionListForm(forms.Form):

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
                  label='Select Session',
                  widget=forms.Select(attrs={'class': 'form-control','id':'session'}))
    classroom = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select Class',
                  widget=forms.Select(attrs={'class': 'form-control','id':'classroom'}))
    
# admission list by class form
class StudentsByClassForm(forms.Form):
    
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
                  label='Select Session',
                  widget=forms.Select(attrs={'class': 'form-control','id':'session'}))
    classroom = forms.ModelChoiceField(
                  queryset=StudentClass.objects.all(),
                  empty_label=None,
                  required=True,
                  to_field_name='id',
                  label='Select Class',
                  widget=forms.Select(attrs={'class': 'form-control','id':'classroom'}))


class AffectiveForm(ModelForm):
    class Meta:
        model = Affective
        fields = '__all__'
        # exclude = ['client']
        widgets= {'domain': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter new domain','id':'affective-domain'}),
                  }

class PsychomotorForm(ModelForm):
    class Meta:
        model = Psychomotor
        fields = '__all__'
        # exclude = ['client']
        widgets= {'skill': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter new psychomotor','id':'psychomotor-domain'}),
                  }


# Rating form
class RatingForm(forms.ModelForm):
    
    description = forms.CharField(
              label='Description',
              required=True,
              widget=forms.TextInput(attrs={'class': 'form-control','id':'rating-description'}))
    scores = forms.CharField(
              label='Rating Score',
              required=True,
              widget=forms.NumberInput(attrs={'class': 'form-control','id':'rating-score'}))
    class Meta:
        model = Rating
        fields = '__all__'
        # exclude = ['client','user']