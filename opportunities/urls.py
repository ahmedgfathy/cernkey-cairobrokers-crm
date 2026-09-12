from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('create/', views.opportunity_create, name='opportunity_create'),
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('<int:pk>/edit/', views.opportunity_update, name='opportunity_update'),
    path('<int:pk>/delete/', views.opportunity_delete, name='opportunity_delete'),
    path('stages/', views.opportunity_stage_list, name='opportunity_stage_list'),
    path('stages/create/', views.opportunity_stage_create, name='opportunity_stage_create'),
    path('stages/<int:pk>/edit/', views.opportunity_stage_update, name='opportunity_stage_update'),
    path('stages/<int:pk>/delete/', views.opportunity_stage_delete, name='opportunity_stage_delete'),
]
