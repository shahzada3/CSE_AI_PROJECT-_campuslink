from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.file_upload, name='file_upload'),
    path('download/<int:file_id>/', views.file_download, name='file_download'),
    path('delete/<int:file_id>/', views.file_delete, name='file_delete'),
]