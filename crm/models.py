from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

class StudentBoard(models.Model):
    name = models.CharField(max_length=150)
    position = models.IntegerField()
    color = models.CharField(max_length=100)

class User(models.Model): 
    name = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=200)

class Specialties(models.Model): 
    name = models.CharField(max_length=200)
    price = models.IntegerField()

class Education(models.Model): 
    name = models.CharField(max_length=200)

class Document(models.Model): 
    passport = models.ImageField(upload_to='images/')
    copyPassport = models.ImageField(upload_to='images/')
    documentOfEducation = models.ImageField(upload_to='images/')
    photo_3_x_4 = models.ImageField(upload_to='images/')
    medicalDoc_086_y = models.ImageField(upload_to='images/')
    medicalDoc_29_H = models.ImageField(upload_to='images/')
    copySNILS = models.ImageField(upload_to='images/')
    medicalInsurance = models.ImageField(upload_to='images/')

class EnrolleeProfile(models.Model):
    email = models.EmailField()
    code = models.IntegerField()
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

class Enrollee(models.Model): 
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    middleName = models.CharField(max_length=200)
    birthDate = models.DateField()
    idSpecialties = models.ForeignKey(Specialties, on_delete=models.PROTECT)
    typeOfEducation = models.ForeignKey(Education, on_delete=models.PROTECT)
    idDocument = models.ForeignKey(Document, on_delete=models.PROTECT)
    idEnrolleeProfile = models.ForeignKey(EnrolleeProfile, on_delete=models.PROTECT)
    
class StudentCard(models.Model):
    idStage = models.ForeignKey(StudentBoard, on_delete=models.PROTECT)
    idEnrollee = models.ForeignKey(Enrollee, on_delete=models.PROTECT)
    date = models.DateField(_("Date"), auto_now_add=True)

class CardHistory(models.Model): 
    idCard = models.ForeignKey(StudentCard, on_delete=models.CASCADE)
    idUser = models.ForeignKey(User, on_delete=models.PROTECT)
    changeData = models.DateField()
    changeDate = models.DateField()

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