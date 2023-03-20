from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bx24_testing/events/', include('eventsapp.urls')),
    # path('testingevents/api/v1/', include('api_v1.urls')),

]
