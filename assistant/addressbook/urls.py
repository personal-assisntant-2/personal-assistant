
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'addressbook'
urlpatterns = [
    path('add_contact/', views.add_contact, name = 'add-contact'),
    path('home/', views.home, name = 'home'),
    path('detail/<int:pk>/', views.AbonentDetailView.as_view(), name='detail'),
    path('edit_contact/<int:pk>/', views.edit_contact, name='edit-contact'),
    path('birthdays/', views.birthdays, name = 'birthdays'),
]

