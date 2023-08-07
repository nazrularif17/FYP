from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Student, Property, Room, Owner, CustomUser
from .forms import AdminSignupForm, StudentSignupForm, CustomUserForm, RoomForm, RoomUpdate, OwnerForm, PropertyForm, UserProfileForm
from django.urls import reverse_lazy
from django.shortcuts import Http404

# Student Login or Registration
def student(request):
    if request.method=='POST':
        if request.POST.get('submit') == 'studentsignup':
            Userform = CustomUserForm(request.POST)
            Studentform = StudentSignupForm(request.POST)
            if Userform.is_valid() and Studentform.is_valid():
                user = Userform.save(commit=False)
                user.role = 'student'
                user.is_staff = False
                user.is_superuser = False
                user.save()
                student = Studentform.save(commit=False)
                student.user = user
                student.save()
                login(request, user)
                return redirect('index')
                
        elif request.POST.get('submit') == 'studentlogin':
            ID = request.POST['ID']
            password = request.POST['password']
            user = authenticate(request, customID=ID, password=password)
            if user is not None and not user.is_staff:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'student.html', {'error': 'Enter correct ID and password'})
    else:
        Userform = CustomUserForm()
        Studentform = StudentSignupForm()
    return render (request,"student.html", {'Userform': Userform, 'Studentform': Studentform})

# Admin Login or Registration
def admin(request):
    if request.method=='POST':
        if request.POST.get('submit') == 'adminsignup':
            Userform = CustomUserForm(request.POST)
            Adminform = AdminSignupForm(request.POST)
            if Userform.is_valid() and Adminform.is_valid():
                user = Userform.save(commit=False)
                user.role = 'admin'
                user.is_staff = True
                user.is_superuser = True
                user.save()
                admin = Adminform.save(commit=False)
                admin.user = user
                admin.save()
                login(request, user)
                return redirect('admin_panel')
        elif request.POST.get('submit') == 'adminlogin':
            ID = request.POST['ID']
            password = request.POST['password']
            user = authenticate(request, customID=ID, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_panel')
            else:
                return render(request, 'admin.html', {'error': 'Enter correct ID and password'})
    else:
        Userform = CustomUserForm()
        Adminform = AdminSignupForm()
    return render (request,"admin.html", {'Userform': Userform, 'Adminform': Adminform})

# Homepage
@login_required(login_url='student')
def index(request):
    currentuser = request.user.student
    room_exists = Room.objects.filter(studentID=currentuser).exists()
    context = {
        'room_exists': room_exists,
    }
    return render (request,"index.html", context)

# Property List
class property_list(ListView):
    model = Property
    template_name = 'prop_list.html'
    context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currentuser = self.request.user.student
        room_exists = Room.objects.filter(studentID=currentuser).exists()
        context['room_exists'] = room_exists
        return context
    # Only display property with propStatus='Available'
    def get_queryset(self):
        return Property.objects.filter(propStatus='Available')
    
# Property detail
class property_detail(DetailView):
    model = Property
    template_name = 'prop_detail.html'
    context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property = self.get_object()
        context['owner'] = property.ownID
        currentuser = self.request.user.student
        room_exists = Room.objects.filter(studentID=currentuser).exists()
        context['room_exists'] = room_exists
        return context

# Room list
class room_list(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'
    # Only display room with roomStatus='Available'
    def get_queryset(self):
        return Room.objects.filter(roomStatus='Available')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currentuser = self.request.user.student
        room_exists = Room.objects.filter(studentID=currentuser).exists()
        context['room_exists'] = room_exists
        return context

# Room detail
class room_detail(DetailView):
    model = Room
    template_name = 'room_detail.html'
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        context['student'] = room.studentID
        currentuser = self.request.user.student
        room_exists = Room.objects.filter(studentID=currentuser).exists()
        context['room_exists'] = room_exists
        return context

# Room advertisement form
def room_form(request):
    if request.method == 'POST':
        Roomform = RoomForm(request.POST, request.FILES)
        if Roomform.is_valid():
            student = Student.objects.get(user = request.user)
            room = Roomform.save(commit=False)
            room.studentID = student
            room.roomStatus = 'Available'
            room.save()
            return redirect('room_list')
        else:
            print("Enter correct details")
    else:
        Roomform = RoomForm()
    return render(request, 'room_form.html', {'Roomform': Roomform,})

# Student Room Update
"""class room_update(UpdateView):
    model = Room
    fields = ["roomTitle","roomPrice","roomFurnishings","roomDesc","roomStatus"]
    template_name = "room_update.html"
    success_url = reverse_lazy("room_list")
    
    def get_queryset(self):
        user = Student.object.get(user = self.request.user)
        queryset = Room.objects.get(studentID=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currentuser = self.request.user.student
        room_exists = Room.objects.filter(studentID=currentuser).exists()
        context['room_exists'] = room_exists
        return context"""
def room_update(request, pk):
    user = request.user.student
    room = Room.objects.filter(studentID=user).first()
    
    if not room:
        raise Http404("No room found for the current user.")
    
    if request.method == 'POST':
        form = RoomUpdate(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomUpdate(instance=room)
    
    currentuser = request.user.student
    room_exists = Room.objects.filter(studentID=currentuser).exists()
    context = {
        'form': form,
        'room_exists': room_exists
    }
    
    return render(request, 'room_update.html', context)
# Student Room Delete
def room_delete(request, pk):
    user = request.user.student
    room = Room.objects.filter(studentID=user).first()

    if request.method == 'POST':
        # Display an alert dialog to confirm the deletion
        messages.success(request, 'Are you sure you want to delete this object?')
        room.delete()
        return redirect('room_list')

    context = {
        'room': room
    }

    return render(request, 'room_update.html', context)
# User profile
@login_required(login_url='student')
def user_profile(request):
    profile = request.user.student
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserProfileForm(instance=profile)

    currentuser = request.user.student
    room_exists = Room.objects.filter(studentID=currentuser).exists()
    context = {
        'room_exists': room_exists,
        'form': form,
    }
    return render(request, 'user_profile.html',context)

# Admin Dashboard
@login_required(login_url='admin')
def admin_panel(request):
    return render(request, 'admin_panel.html')

# Admin Student List
class admin_student_list(ListView):
    model = Student
    template_name = 'admin_student_list.html'
    context_object_name = 'entity_list'
# Admin Student Detail
class admin_student_detail(DetailView):
    model = Student
    template_name = 'admin_student_detail.html'
    context_object_name = 'entity_list'

# Admin Room List
class admin_room_list(ListView):
    model = Room
    template_name = 'admin_room_list.html'
    context_object_name = 'entity_list'
# Admin Room Detail
class admin_room_detail(DetailView):
    model = Room
    template_name = 'admin_room_detail.html'
    context_object_name = 'entity_list'

# Admin Property List
class admin_property_list(ListView):
    model = Property
    template_name = 'admin_property_list.html'
    context_object_name = 'entity_list'
# Admin Property Detail
class admin_property_detail(DetailView):
    model = Property
    template_name = 'admin_property_detail.html'
    context_object_name = 'entity_list'
# Admin Property Create
class admin_property_add(CreateView):
    model = Property
    template_name = "admin_property_add.html"
    form_class = PropertyForm
    success_url = reverse_lazy("admin_property_list")
    # Add property
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['propTitle'].widget.attrs['placeholder'] = 'Property title'
        form.fields['propType'].widget.attrs['placeholder'] = 'Type of property'
        form.fields['propPrice'].widget.attrs['placeholder'] = 'Rental price'
        form.fields['propRange'].widget.attrs['placeholder'] = 'Property range to college'
        form.fields['propAddress'].widget.attrs['placeholder'] = 'Property address'
        form.fields['propFurnishings'].widget.attrs['placeholder'] = 'Property furnishing'
        form.fields['propDesc'].widget.attrs['placeholder'] = 'Property description'
        return form
# Admin Property Update
class admin_property_update(UpdateView):
    model = Property
    fields = ["propTitle","propPrice","propFurnishings","propDesc","propStatus"]
    template_name = "admin_property_update.html"
    success_url = reverse_lazy("admin_property_list")
# Admin Property Delete
class admin_property_delete(DeleteView):
    model = Property
    success_url = reverse_lazy("admin_property_list")
    # Alert Dialog
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Are you sure you want to delete this object?')
        return super().delete(request, *args, **kwargs)

# Admin Owner List
class admin_owner_list(ListView):
    model = Owner
    template_name = 'admin_owner_list.html'
    context_object_name = 'entity_list'
# Admin Owner Detail
class admin_owner_detail(DetailView):
    model = Owner
    template_name = 'admin_owner_detail.html'
    context_object_name = 'entity_list'
# Admin Owner Create
class admin_owner_add(CreateView):
    model = Owner
    template_name = "admin_owner_add.html"
    form_class = OwnerForm
    success_url = reverse_lazy("admin_owner_list")
    # Add property's owner
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['ownName'].widget.attrs['placeholder'] = 'Owner name'
        form.fields['ownPhoneNo'].widget.attrs['placeholder'] = 'Owner phone no'
        form.fields['ownEmail'].widget.attrs['placeholder'] = 'Owner email'
        return form
# Admin Owner Update
class admin_owner_update(UpdateView):
    model = Owner
    fields = ["ownPhoneNo","ownEmail"]
    template_name = "admin_owner_update.html"
    success_url = reverse_lazy("admin_owner_list")
# Admin Owner Delete
class admin_owner_delete(DeleteView):
    model = Owner
    success_url = reverse_lazy("admin_owner_list")
    # Alert Dialog
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Are you sure you want to delete this object?')
        return super().delete(request, *args, **kwargs)
    
def logout_view(request):
    logout(request)
    return redirect('student')