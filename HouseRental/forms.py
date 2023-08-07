
from .models import Room, Admin, Student, CustomUser, Owner, Property
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    class Meta:
        model = CustomUser
        fields = ('customID', 'password1', 'password2')
        widgets = {
            'customID': forms.TextInput(attrs={'placeholder': 'ID'}),
        }

class AdminSignupForm(forms.ModelForm):

    class Meta:
        model = Admin
        fields = ['adminName', 'adminEmail']
        widgets = {
            'adminName': forms.TextInput(attrs={'placeholder': 'Name'}),
            'adminEmail': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

class StudentSignupForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    RESIDENTIAL_CHOICES = [
        ('Resident', 'Resident'),
        ('Non-resident', 'Non-resident'),
    ]
    studentGender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class' : 'child-option-gender'}), choices=GENDER_CHOICES)
    residentialStatus = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class' : 'child-option-status'}), choices=RESIDENTIAL_CHOICES)
      
    class Meta:
        model = Student
        fields = ['studentName', 'studentPhoneNo', 'studentEmail', 'studentGender', 'residentialStatus']
        widgets = {
            'studentName': forms.TextInput(attrs={'placeholder': 'Name'}),
            'studentPhoneNo': forms.NumberInput(attrs={'placeholder': 'Phone Number'}),
            'studentEmail': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

class RoomForm(forms.ModelForm):
    roomImg = forms.ImageField()

    class Meta:  
        model = Room  
        fields = ['roomImg', 'roomTitle', 'roomType', 'roomPrice', 'roomRange', 'roomAddress', 'roomFurnishings', 'roomDesc']

class RoomUpdate(forms.ModelForm):

    class Meta:  
        model = Room  
        fields = ["roomTitle","roomPrice","roomFurnishings","roomDesc","roomStatus"]

class OwnerForm(forms.ModelForm):
    
    class Meta:
        model = Owner
        fields = ["ownName","ownPhoneNo","ownEmail"]

class PropertyForm(forms.ModelForm):
    propImg = forms.ImageField()

    class Meta:  
        model = Property
        fields = ['ownID','propImg', 'propTitle', 'propType', 'propPrice', 'propRange', 'propAddress', 'propFurnishings', 'propDesc']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['studentPhoneNo', 'studentEmail', 'residentialStatus']
        widgets = {
            'studentGender': forms.TextInput(attrs={'readonly': 'readonly'}),
            'studentName': forms.TextInput(attrs={'readonly': 'readonly'}),
        }