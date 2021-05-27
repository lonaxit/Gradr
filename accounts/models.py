# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# class User(AbstractUser):
#     is_teacher = models.BooleanField(default=False)
#     is_student = models.BooleanField(default=False)


class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    school_name = models.CharField(max_length=250,null=True,blank=True)
    school_type = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(null=True,blank=True)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.school_name


class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_name = models.CharField(max_length=20,blank=True)
    middle_name = models.CharField(max_length=20,blank=True)
    last_name = models.CharField(max_length=20,blank=True)
    sex = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    academic_qualification = models.CharField(max_length=100)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_name = models.CharField(max_length=20,blank=True)
    middle_name = models.CharField(max_length=20,blank=True)
    last_name = models.CharField(max_length=20,blank=True)
    sex = models.CharField(max_length=20)
    phone = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.first_name

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
