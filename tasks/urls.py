from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/edit/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('categories/', views.task_category_list, name='task_category_list'),
    path('categories/create/', views.task_category_create, name='task_category_create'),
    path('priorities/', views.task_priority_list, name='task_priority_list'),
    path('priorities/create/', views.task_priority_create, name='task_priority_create'),
    path('statuses/', views.task_status_list, name='task_status_list'),
    path('statuses/create/', views.task_status_create, name='task_status_create'),
]
