from django.contrib import admin
from .models import Student, Admin, Owner, Property, Room, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Owner)
admin.site.register(Property)
admin.site.register(Room)