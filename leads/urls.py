from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('create/', views.lead_create, name='lead_create'),
    path('<int:pk>/', views.lead_detail, name='lead_detail'),
    path('<int:pk>/edit/', views.lead_update, name='lead_update'),
    path('<int:pk>/delete/', views.lead_delete, name='lead_delete'),
    path('sources/', views.lead_source_list, name='lead_source_list'),
    path('sources/create/', views.lead_source_create, name='lead_source_create'),
    path('sources/<int:pk>/edit/', views.lead_source_update, name='lead_source_update'),
    path('sources/<int:pk>/delete/', views.lead_source_delete, name='lead_source_delete'),
    path('statuses/', views.lead_status_list, name='lead_status_list'),
    path('statuses/create/', views.lead_status_create, name='lead_status_create'),
    path('statuses/<int:pk>/edit/', views.lead_status_update, name='lead_status_update'),
    path('statuses/<int:pk>/delete/', views.lead_status_delete, name='lead_status_delete'),
]
