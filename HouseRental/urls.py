from django.urls import path
from . import views
from .views import *

urlpatterns =  [ 
    #student login/signup
    path("student", views.student, name='student'),
    #admin login/signup
    path("admin",views.admin, name="admin"),
    #admin-panel
    path("admin_panel",views.admin_panel, name="admin_panel"),
    #admin view student
    path("admin_student_list",admin_student_list.as_view(), name="admin_student_list"),
    path("admin_student_detail/<pk>",admin_student_detail.as_view(), name="admin_student_detail"),
    #admin view room
    path("admin_room_list",admin_room_list.as_view(), name="admin_room_list"),
    path("admin_room_detail/<pk>",admin_room_detail.as_view(), name="admin_room_detail"),
    #admin manage property
    path("admin_property_list",admin_property_list.as_view(), name="admin_property_list"),
    path("admin_property_detail/<pk>",admin_property_detail.as_view(), name="admin_property_detail"),
    path("admin_property_update/<pk>",admin_property_update.as_view(), name="admin_property_update"),
    path("admin_property_delete/<pk>",admin_property_delete.as_view(), name="admin_property_delete"),
    path("admin_property_add",admin_property_add.as_view(), name="admin_property_add"),
    #admin manage owner
    path("admin_owner_list",admin_owner_list.as_view(), name="admin_owner_list"),
    path("admin_owner_detail/<pk>",admin_owner_detail.as_view(), name="admin_owner_detail"),
    path("admin_owner_update/<pk>",admin_owner_update.as_view(), name="admin_owner_update"),
    path("admin_owner_delete/<pk>",admin_owner_delete.as_view(), name="admin_owner_delete"),
    path("admin_owner_add",admin_owner_add.as_view(), name="admin_owner_add"),
    #index
    path("index",views.index, name="index"),
    #view property
    path("property_list",property_list.as_view(), name="property_list"),
    path("property_list/<pk>/",property_detail.as_view(), name='property_detail'),
    #manage room
    path("room_list",room_list.as_view(), name="room_list"),
    path("room_detail/<pk>",room_detail.as_view(), name='room_detail'),
    path("room_update/<pk>",views.room_update, name="room_update"),
    path("room_delete/<pk>",views.room_delete, name="room_delete"),
    path("room_form",views.room_form, name="room_form"),
    #logout
    path('logout', views.logout_view, name='logout'),

    path("user_profile",views.user_profile, name="user_profile"),
]