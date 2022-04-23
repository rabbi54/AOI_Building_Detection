from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('output/<int:pk>', views.output, name='output'),
]
