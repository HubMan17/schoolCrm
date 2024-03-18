from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta, datetime
from django.utils import timezone

class StudentBoard(models.Model):
    name = models.CharField(max_length=150)
    position = models.IntegerField()
    color = models.CharField(max_length=100, null=True)

class User(models.Model): 
    name = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    role = models.BooleanField(default=False)
    token = models.CharField(max_length=150, null=True)
    timeLiveToken = models.DateTimeField(null=True)

class Specialties(models.Model): 
    name = models.CharField(max_length=200)
    price = models.IntegerField()

class Education(models.Model): 
    name = models.CharField(max_length=200)

class Document(models.Model): 
    passport = models.ImageField(upload_to='images/', default="")
    copyPassport = models.ImageField(upload_to='images/', default="")
    documentOfEducation = models.ImageField(upload_to='images/', default="")
    photo_3_x_4 = models.ImageField(upload_to='images/', default="")
    medicalDoc_086_y = models.ImageField(upload_to='images/', default="")
    medicalDoc_29_H = models.ImageField(upload_to='images/', default="")
    copySNILS = models.ImageField(upload_to='images/', default="")
    medicalInsurance = models.ImageField(upload_to='images/', default="")

class EnrolleeProfile(models.Model):
    email = models.EmailField(default="")
    code = models.IntegerField(default=None, null=True)
    status = models.BooleanField(default=False) # активен, неактивен
    password = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="", null=True)

class Enrollee(models.Model): 
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    middleName = models.CharField(max_length=200, default="", null=True)
    birthDate = models.DateField(null=True)
    idSpecialties = models.ForeignKey(Specialties, on_delete=models.PROTECT)
    typeOfEducation = models.ForeignKey(Education, on_delete=models.PROTECT)
    idDocument = models.ForeignKey(Document, on_delete=models.PROTECT)
    idEnrolleeProfile = models.ForeignKey(EnrolleeProfile, on_delete=models.CASCADE)
    
class StudentCard(models.Model):
    idStage = models.ForeignKey(StudentBoard, on_delete=models.PROTECT)
    idEnrollee = models.ForeignKey(Enrollee, on_delete=models.CASCADE)
    date = models.DateField(_("Date"), auto_now_add=True)

class CardHistory(models.Model): 
    idCard = models.ForeignKey(StudentCard, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.PROTECT, default=0)
    changeData = models.TextField(null=True)
    changeDate = models.DateTimeField(auto_now_add=True)
    field = models.CharField(max_length=200, null=True)
    comment = models.BooleanField(default=False, null=True)
    

class Group(models.Model): 
    idSpecialties = models.ForeignKey(Specialties, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    course = models.IntegerField()
    subCourse = models.IntegerField()
    
class Student(models.Model): 
    idGroup = models.ForeignKey(Group, on_delete=models.PROTECT)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    middleName = models.CharField(max_length=200)
    birthDate = models.DateField()
    typeOfEducation = models.ForeignKey(Education, on_delete=models.PROTECT)
    idDocument = models.ForeignKey(Document, on_delete=models.PROTECT)
    idEnrolleeProfile = models.ForeignKey(EnrolleeProfile, on_delete=models.PROTECT)
    
    


# print(list(data))