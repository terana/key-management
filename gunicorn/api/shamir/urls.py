from django.urls import path

from . import views

urlpatterns = [
    path('UploadShare', views.upload_share, name='upload_share'),
]
