from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('create/', views.property_create, name='property_create'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('<int:pk>/edit/', views.property_update, name='property_update'),
    path('<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('types/', views.property_type_list, name='property_type_list'),
    path('types/create/', views.property_type_create, name='property_type_create'),
    path('types/<int:pk>/edit/', views.property_type_update, name='property_type_update'),
    path('types/<int:pk>/delete/', views.property_type_delete, name='property_type_delete'),
    path('statuses/', views.property_status_list, name='property_status_list'),
    path('statuses/create/', views.property_status_create, name='property_status_create'),
    path('statuses/<int:pk>/edit/', views.property_status_update, name='property_status_update'),
    path('statuses/<int:pk>/delete/', views.property_status_delete, name='property_status_delete'),
]
