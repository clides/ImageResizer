from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('check-processing/', views.check_processing_status, name='check_processing'),
    path('result/', views.result_page, name='result_page'),
]