from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/join/', views.join_project, name='join_project'),
    path('task/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
]