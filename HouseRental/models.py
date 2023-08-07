from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin  
from .managers import CustomUserManager  
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    customID = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'customID'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.customID
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_student(self):
        return self.role == 'student'
    
class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    RESIDENTIAL_CHOICES = [
        ('Resident', 'Resident'),
        ('Non-resident', 'Non-resident'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    studentName=models.CharField(max_length=50)
    studentPhoneNo=models.CharField(max_length=12)
    studentEmail=models.EmailField(max_length=255)
    studentGender=models.CharField(max_length=6, choices=GENDER_CHOICES)
    residentialStatus=models.CharField(max_length=12, choices=RESIDENTIAL_CHOICES)

    def __str__(self):
        return self.user.customID
    
class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    adminName=models.CharField(max_length=50)
    adminEmail=models.EmailField(max_length=255)

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = ['adminName', 'adminEmail']

    def __str__(self):
        return self.user.customID

class Owner(models.Model):
    ownID=models.AutoField(primary_key=True)
    ownName=models.CharField(max_length=50)
    ownPhoneNo=models.CharField(max_length=12)
    ownEmail=models.EmailField(max_length=255)

    def __int__(self):
        return self.ownID

class Property(models.Model):
    PROPERTY_TYPE = [
        ('Bungalow', 'Bungalow'),
        ('Townhouse', 'Townhouse'),
        ('Terrace', 'Terrace'),
        ('Apartment', 'Apartment'),
        ('Condominium', 'Condominium'),
        ('Flat', 'Flat'),
    ]
    FURNISHINGS = [
        ('Fully Furnished', 'Fully Furnished'),
        ('Partially Furnished', 'Partially Furnished'),
        ('Not Furnished', 'Not Furnished'),
    ]
    PROPERTY_STATUS = [
        ('Available','Available'),
        ('Rented Out','Rented Out'),
    ]
    propID=models.AutoField(primary_key=True)
    ownID=models.ForeignKey(Owner, on_delete=models.CASCADE)
    propImg=models.ImageField(upload_to='images/property')
    propTitle=models.CharField(max_length=50)
    propType=models.CharField(max_length=50, choices=PROPERTY_TYPE)
    propPrice=models.PositiveIntegerField()
    propRange=models.PositiveIntegerField()
    propAddress=models.TextField(max_length=255)
    propFurnishings=models.CharField(max_length=20, choices=FURNISHINGS)
    propDesc=models.TextField()
    propCreateAt=models.DateField(auto_now_add=True)
    propStatus=models.CharField(max_length=10,choices=PROPERTY_STATUS, default= 'Available')

    def __int__(self):
        return self.propID
 
class Room(models.Model):
    ROOM_TYPE = [
        ('Single', 'Single'),
        ('Sharing', 'Sharing'),
    ]
    FURNISHINGS = [
        ('Fully Furnished', 'Fully Furnished'),
        ('Partially Furnished', 'Partially Furnished'),
        ('Not Furnished', 'Not Furnished'),
    ]
    ROOM_STATUS = [
        ('Available','Available'),
        ('Rented Out','Rented Out'),
    ]
    roomID=models.AutoField(primary_key=True)
    studentID=models.ForeignKey(Student, on_delete=models.CASCADE)
    roomImg=models.ImageField(upload_to='images/room')
    roomTitle=models.CharField(max_length=50)
    roomType=models.CharField(max_length=50, choices=ROOM_TYPE, default='Single')
    roomPrice=models.PositiveIntegerField()
    roomRange=models.PositiveIntegerField()
    roomAddress=models.TextField(max_length=255)
    roomFurnishings=models.CharField(max_length=20, choices=FURNISHINGS)
    roomDesc=models.TextField()
    roomCreateAt=models.DateField(auto_now_add=True)
    roomStatus=models.CharField(max_length=10,choices=ROOM_STATUS, default='Available')

    def __int__(self):
        return self.roomID