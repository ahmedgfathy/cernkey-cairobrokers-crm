from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('create/', views.lead_create, name='lead_create'),
    path('<int:pk>/', views.lead_detail, name='lead_detail'),
    path('<int:pk>/edit/', views.lead_update, name='lead_update'),
    path('<int:pk>/delete/', views.lead_delete, name='lead_delete'),

    path('export/csv/', views.lead_export_csv, name='lead_export_csv'),
    path('export/excel/', views.lead_export_excel, name='lead_export_excel'),
    path('import/', views.lead_import, name='lead_import'),
    path('import/map/', views.lead_import_map, name='lead_import_map'),
    path('filters/save/', views.lead_save_filter, name='lead_save_filter'),
    path('filters/<int:pk>/delete/', views.lead_delete_filter, name='lead_delete_filter'),

    path('<int:lead_pk>/task/create/', views.lead_task_create, name='lead_task_create'),
    path('task/<int:pk>/update/', views.lead_task_update, name='lead_task_update'),
    path('task/<int:pk>/complete/', views.lead_task_complete, name='lead_task_complete'),
    path('task/<int:pk>/delete/', views.lead_task_delete, name='lead_task_delete'),

    path('<int:lead_pk>/call/create/', views.lead_call_create, name='lead_call_create'),
    path('call/<int:pk>/delete/', views.lead_call_delete, name='lead_call_delete'),

    path('<int:lead_pk>/meeting/create/', views.lead_meeting_create, name='lead_meeting_create'),
    path('meeting/<int:pk>/delete/', views.lead_meeting_delete, name='lead_meeting_delete'),

    path('<int:lead_pk>/email/create/', views.lead_email_create, name='lead_email_create'),
    path('email/<int:pk>/delete/', views.lead_email_delete, name='lead_email_delete'),

    path('<int:lead_pk>/note/create/', views.lead_note_create, name='lead_note_create'),
    path('note/<int:pk>/delete/', views.lead_note_delete, name='lead_note_delete'),

    path('sources/', views.lead_source_list, name='lead_source_list'),
    path('sources/create/', views.lead_source_create, name='lead_source_create'),
    path('sources/<int:pk>/edit/', views.lead_source_update, name='lead_source_update'),
    path('sources/<int:pk>/delete/', views.lead_source_delete, name='lead_source_delete'),

    path('statuses/', views.lead_status_list, name='lead_status_list'),
    path('statuses/create/', views.lead_status_create, name='lead_status_create'),
    path('statuses/<int:pk>/edit/', views.lead_status_update, name='lead_status_update'),
    path('statuses/<int:pk>/delete/', views.lead_status_delete, name='lead_status_delete'),
]
