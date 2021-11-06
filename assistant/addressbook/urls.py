
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'addressbook'
urlpatterns = [
    path('add-contact/', views.add_contact, name='add-contact'),
    path('home/', views.home, name='home'),
    path('find-contacts/', views.find_contacts, name='find-contacts')
]
