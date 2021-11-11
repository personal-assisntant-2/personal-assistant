from django.urls import include, path
from .views import dashboard, register

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('dashboard/', dashboard, name="dashboard"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', register, name="register"),
]
