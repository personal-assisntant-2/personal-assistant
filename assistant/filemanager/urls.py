from django.urls import path

from . import views


app_name = 'file_manager'

urlpatterns = [
    path('', views.file_manager_view, name='file'),
    path('download/<int:file_id>/', views.file_download_view, name='download_file'),
    # path('sort/<int:file_id>/', views.sort_by_category_view, name='sort_file'),
    ]
