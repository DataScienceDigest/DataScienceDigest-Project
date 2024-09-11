from django.urls import path
from .views import index,docs,run_code
urlpatterns = [
    path('',index),
    path('docs',docs),
    path('run/', run_code, name='run_code'),
]
