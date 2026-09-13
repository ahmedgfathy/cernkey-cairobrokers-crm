from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('create/', views.property_create, name='property_create'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('<int:pk>/edit/', views.property_update, name='property_update'),
    path('<int:pk>/delete/', views.property_delete, name='property_delete'),

    path('export/csv/', views.property_export_csv, name='property_export_csv'),
    path('export/excel/', views.property_export_excel, name='property_export_excel'),
    path('import/', views.property_import, name='property_import'),
    path('import/map/', views.property_import_map, name='property_import_map'),
    path('cleanup/', views.property_cleanup, name='property_cleanup'),

    path('<int:property_pk>/unit/create/', views.property_unit_create, name='property_unit_create'),
    path('unit/<int:pk>/update/', views.property_unit_update, name='property_unit_update'),
    path('unit/<int:pk>/delete/', views.property_unit_delete, name='property_unit_delete'),

    path('<int:property_pk>/viewing/create/', views.property_viewing_create, name='property_viewing_create'),
    path('viewing/<int:pk>/delete/', views.property_viewing_delete, name='property_viewing_delete'),

    path('<int:property_pk>/offer/create/', views.property_offer_create, name='property_offer_create'),
    path('offer/<int:pk>/update/', views.property_offer_update, name='property_offer_update'),
    path('offer/<int:pk>/delete/', views.property_offer_delete, name='property_offer_delete'),

    path('<int:property_pk>/note/create/', views.property_note_create, name='property_note_create'),
    path('note/<int:pk>/delete/', views.property_note_delete, name='property_note_delete'),

    path('types/', views.property_type_list, name='property_type_list'),
    path('types/create/', views.property_type_create, name='property_type_create'),
    path('types/<int:pk>/edit/', views.property_type_update, name='property_type_update'),
    path('types/<int:pk>/delete/', views.property_type_delete, name='property_type_delete'),

    path('statuses/', views.property_status_list, name='property_status_list'),
    path('statuses/create/', views.property_status_create, name='property_status_create'),
    path('statuses/<int:pk>/edit/', views.property_status_update, name='property_status_update'),
    path('statuses/<int:pk>/delete/', views.property_status_delete, name='property_status_delete'),
]
