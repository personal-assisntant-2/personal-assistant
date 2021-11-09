from django.conf.urls import url, include
from .views import dashboard, register

urlpatterns = [
    url('dashboard/', dashboard, name="dashboard"),
    # url('', dashboard, name="dashboard"),
    url('accounts/', include("django.contrib.auth.urls")),
    url('register/', register, name="register"),
]
