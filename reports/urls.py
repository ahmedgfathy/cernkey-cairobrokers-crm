from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_dashboard, name='reports_dashboard'),
    path('leads/', views.report_leads, name='report_leads'),
    path('properties/', views.report_properties, name='report_properties'),
    path('opportunities/', views.report_opportunities, name='report_opportunities'),
    path('tasks/', views.report_tasks, name='report_tasks'),
    path('agents/', views.report_agents, name='report_agents'),
    path('pipeline/', views.report_pipeline, name='report_pipeline'),
    path('revenue/', views.report_revenue, name='report_revenue'),
]
