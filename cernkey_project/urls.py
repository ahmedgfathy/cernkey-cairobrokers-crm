from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('leads/', include('leads.urls')),
    path('properties/', include('properties.urls')),
    path('opportunities/', include('opportunities.urls')),
    path('notifications/', include('notifications.urls')),
    path('tasks/', include('tasks.urls')),
    path('reports/', include('reports.urls')),
    path('documents/', include('documents.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
