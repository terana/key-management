from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('secret/', include('api.secrets.urls')),
]
