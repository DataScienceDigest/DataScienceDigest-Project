from django.urls import path
from .views import index,run_code
urlpatterns = [
    path('',index),
    path('run/', run_code, name='run_code'),
]
