from django.contrib import admin
from django.urls import path, include
from myapi import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapi.urls')),
]
