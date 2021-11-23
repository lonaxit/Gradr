from django.forms import ModelForm
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms
from teacher.models import *
from accounts.models import *

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user']
# exclude teacher from editing user


class ClientForm(ModelForm):
    school_name = forms.CharField(label='school name',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Institution name','id':'sch_name'}))
    school_type = forms.CharField(label='School Type',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Secondary','id':'sch_type'}))
    email = forms.EmailField(label='E-Mail',
                            max_length=100,
                            widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email','id':'email'}))
    phone = forms.CharField(label='Phone',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter phone number','id':'phone'}))
    address = forms.CharField(label='Address',
                            max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Address','id':'address'}))
    
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
              label='Lga',
              widget=forms.TextInput(attrs={'class': 'form-control','id':'lga'}))
    city = forms.CharField(
              label='City',
              widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter city','id':'city'}))
    
    # profile_image = forms.ImageField(label='Upload Your logo',
    #                         max_length=100,
    #                         widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['user','profile_image']



class ClientRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your username','id':'username'}))
    email = forms.EmailField(label='E-Mail',
                            max_length=100,
                            widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email','id':'email'}))
    password1 = forms.CharField(label='Password',
                            max_length=100,
                            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your password','id':'password1'}))
    password2 = forms.CharField(label='Confirm Password',
                            max_length=100,
                            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm your Password','id':'password2'}))

    class Meta:
        model = User
        fields =['username','email','password1','password2']

# student signup form
class StudentRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your username','id':'username'}))
    email = forms.EmailField(label='E-Mail',
                                max_length=100,
                                widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email','id':'email'}))

    password1 = forms.CharField(label='Password',
                            max_length=100,
                            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your password','id':'password1'}))
    password2 = forms.CharField(label='Confirm Password',
                            max_length=100,
                            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm your Password','id':'password2'}))

    class Meta:
        model = User
        fields =['username','email','password1','password2']


# staff signup form
class StaffRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your username','id':'username'}))
    email = forms.EmailField(label='E-Mail',
                                max_length=100,
                                widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email','id':'email'}))

    password1 = forms.CharField(label='Password',
                            max_length=100,
                            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your password','id':'password1'}))
    password2 = forms.CharField(label='Confirm Password',
                            max_length=100,
                            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm your Password','id':'password2'}))

    class Meta:
        model = User
        fields =['username','email','password1','password2']

# user update form

class UserUpdateForm(forms.ModelForm):
    
    email = forms.EmailField(label='E-Mail',
            max_length=100,
            widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email','id':'email'}))
    
    class Meta:
        model=User
        fields=['username','email']
        

# update profile picture

class ClientPictureUpdateForm(forms.ModelForm):
    
    # email = forms.EmailField(label='E-Mail',
    #         max_length=100,
    #         widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email','id':'email'}))
    
    class Meta:
        model=Client
        fields=['profile_image']

class StudentPictureUpdateForm(forms.ModelForm):
    
    class Meta:
        model=Student
        fields=['profile_image']

class TeacherPictureUpdateForm(forms.ModelForm):
    
    class Meta:
        model=Client
        fields=['profile_image']


class contactForm(forms.Form):
    # username= forms.CharField(max_length=20)
    # email= forms.EmailField()
    # password1= forms.CharField(max_length=20)
    # password2=forms.CharField(max_length=20)

    # model form using widgets
    # class MyComplicatedModelForm(forms.ModelForm):
    # field_z = forms.ModelChoiceField(
    #     queryset=AnyClass.objects.all(),
    #     empty_label=None,
    #     required=True,
    #     to_field_name='id',
    #     label='Select your Z value here',
    #     widget=forms.SelectMultiple(attrs={'class': 'myclass'})
    # )
    #
    # class Meta:
    #     model = MyComplicatedModel
    #     fields = ['field_z']
    # end model form with widget

    # placeholder in a form example
    # class Userform(forms.Form):
    # firstname= forms.CharField(max_length=100,
    #                        widget= forms.TextInput
    #                        (attrs={'placeholder':'Enter your first name'}))
    # email= forms.CharField(max_length=100,
    #                        widget= forms.EmailInput
    #                        (attrs={'placeholder':'Enter your email'}))
    # phonenumber= forms.CharField(max_length=100,
    #                        widget= forms.TextInput
    #                        (attrs={'placeholder':'(xxx)xxx-xxxx'}))
    # end placeholder in a form

    # placeholder in a model form
    # class Userform(forms.ModelForm):
    # firstname= forms.CharField(widget= forms.TextInput
    #                        (attrs={'placeholder':'Enter your first name'}))
    # email= forms.CharField(widget= forms.EmailInput
    #                        (attrs={'placeholder':'Enter your email'}))
    # phonenumber= forms.CharField(widget= forms.TextInput
    #                        (attrs={'placeholder':'(xxx)xxx-xxxx'}))
    # It's the same as the form before, but now we don't have to add the max_length attribute, because it would already be defined in the models.py file.
    #
    # And this is how to add a placeholder to a Django form field.
    # end placeholder in a model form here

# favourite_provider = forms.ModelChoiceField(queryset=Provider.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username',
                           max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your username','id':'username'}))
    email = forms.EmailField(label='E-Mail',
                            max_length=100,
                            widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email','id':'email'}))
    password1 = forms.CharField(label='Password',
                            max_length=100,
                            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your password','id':'password1'}))
    password2 = forms.CharField(label='Confirm Password',
                            max_length=100,
                            widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm your Password','id':'password2'}))
