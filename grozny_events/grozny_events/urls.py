from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls', namespace='events')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about'))
]

handler404 = 'core.views.page_not_found'
handler403 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
