from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('output/<int:pk>', views.output, name='output'),
    path('download/<int:pk>', views.download_file, name='download_file'),
]
