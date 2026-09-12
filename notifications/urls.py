from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:pk>/', views.notification_detail, name='notification_detail'),
    path('<int:pk>/read/', views.notification_mark_read, name='notification_mark_read'),
    path('<int:pk>/archive/', views.notification_archive, name='notification_archive'),
    path('<int:pk>/delete/', views.notification_delete, name='notification_delete'),
    path('mark-all-read/', views.notification_mark_all_read, name='notification_mark_all_read'),
]
