from django.urls import path

from . import views

urlpatterns = [
    path('GetSecret', views.get_secret, name='get_secret'),
    path('CreateSecret', views.create_secret, name='create_secret'),
    path('GetLogs', views.get_logs, name='get_logs')
]
