# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# class User(AbstractUser):
#     is_teacher = models.BooleanField(default=False)
#     is_student = models.BooleanField(default=False)

class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    school_name = models.CharField(max_length=250,null=True,blank=True)
    school_type = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(default='default_img.png',null=True,blank=True)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    country = models.ForeignKey("administrator.Country",on_delete=models.DO_NOTHING,null=True)
    state = models.ForeignKey("administrator.State",on_delete=models.DO_NOTHING,null=True)
    lga = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.school_name


class Teacher(models.Model):
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
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    surname = models.CharField(max_length=200,blank=True,null=True)
    firstname = models.CharField(max_length=200,blank=True,null=True)
    othername = models.CharField(max_length=200,blank=True,null=True)
    sex = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(default='default_img.png',null=True,blank=True)
    address = models.CharField(max_length=200)
    certificate = models.CharField(max_length=20,blank=True,null=True,choices=CERTIFICATE)
    discipline = models.CharField(max_length=100)
    email = models.CharField(max_length=200,blank=True,null=True)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING,null=True)
    country = models.ForeignKey("administrator.Country",on_delete=models.DO_NOTHING,null=True)
    state = models.ForeignKey("administrator.State",on_delete=models.DO_NOTHING,null=True)
    lga = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.surname

class Student(models.Model):
    BLOODGROUP = (
                ('A+','A+'),
                ('A-','A-'),
                ('AB','AB'),
                ('B+','B+'),
                ('O+','O+'),
                ('O-','O-'),
                )
    GENDER = (
            ('M','Male'),
            ('F','Female'),
    )
    RELIGION =(
    ('CHRISTIANITY', 'CHRISTIANITY'),
    ('ISLAM','ISLAM'),
    ('OTHERS','OTHERS')
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    sur_name = models.CharField(max_length=200,blank=True,null=True)
    first_name = models.CharField(max_length=200,blank=True,null=True)
    other_name = models.CharField(max_length=200,blank=True,null=True)
    sex = models.CharField(max_length=20,blank=True,null=True,choices=GENDER)
    dob = models.DateField(blank=True,null=True)
    country = models.ForeignKey("administrator.Country",on_delete=models.DO_NOTHING,null=True)
    state = models.ForeignKey("administrator.State",on_delete=models.DO_NOTHING,null=True)
    lga = models.CharField(max_length=200,null=True,blank=True)
    # lga = models.ForeignKey("administrator.Lga",on_delete=models.DO_NOTHING,null=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    religion = models.CharField(max_length=20,blank=True,null=True, choices=RELIGION)
    blood_group = models.CharField(max_length=20,blank=True,null=True,choices=BLOODGROUP)
    phone = models.CharField(max_length=20,blank=True,null=True)
    profile_image = models.ImageField(default='default_img.png',null=True,blank=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True)
    class_admitted = models.ForeignKey("administrator.StudentClass",on_delete=models.DO_NOTHING,null=True)
    session_admitted = models.ForeignKey("administrator.Session",on_delete=models.DO_NOTHING,null=True)
    term_admitted = models.ForeignKey("administrator.Term",on_delete=models.DO_NOTHING,null=True)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user.first_name

# class Customer(models.Model):
#     #user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
#     name = models.CharField(max_length=200,null=True,blank=True)
#     phone = models.CharField(max_length=200,blank=True,null=True)
#     address = models.CharField(max_length=200,null=True,blank=True)
#     email = models.CharField(max_length=100,blank=True,null=True)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return self.name

# class Tag(models.Model):
#         #user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
#         name = models.CharField(max_length=20,null=True,blank=True)

#         def __str__(self):
#             return self.name


# class Product(models.Model):
#     CATEGORY = (
#             ('Indoor','Indoor'),
#             ('Outdoor','Outdoor'),
#             )
#     #user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
#     name = models.CharField(max_length=20,null=True,blank=True)
#     description = models.CharField(max_length=200,blank=True,null=True)
#     price = models.FloatField(null=True)
#     category = models.CharField(max_length=100,blank=True,null=True, choices=CATEGORY)
#     date_created = models.DateTimeField(auto_now_add=True, null=True,blank=True)
#     # tags = models.ManyToManyField(Tag)

#     def __str__(self):
#         return self.name


# class Order(models.Model):
#     STATUS = (
#             ('Delivered','Delivered'),
#             ('Pending','Pending'),
#             ('Out for delivery','Out for delivery'),
#             )
#     # customer = models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
#     # product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#     status = models.CharField(max_length=200,null=True,choices=STATUS)
#     def __str__(self):
#         return self.product.name
