from django.urls import path
from . import views
urlpatterns = [
    path('', views.request, name='request'),
    path('command/status', views.command_status, name='command_status')
]
