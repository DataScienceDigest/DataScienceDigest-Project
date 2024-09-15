from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('all_courses/',views.all_courses,name='all_courses'),
    # ________________javascript Compiler __________________
    path('javascript/', views.javascript_index, name='javascript'),
    
    path('java/', views.java_index, name='java'),
    path('r/', views.r_index, name='r'),  # 'R' should be lowercase for the URL
    path('php/', views.php_index, name='php'),
    path('csharp/', views.csharp_index, name='csharp'),  # Avoid special characters in URLs
    path('sql/', views.sql_index, name='sql'),
    path('html/', views.html_index, name='html'),
    # path('c/',views.c_cpp_index,name='c_cpp_index'),
    # path('c_run_code/', views.c_run_code, name='c_run_code'),
    path('css/', views.css_index, name='css'),
    # _______________python section ____________________
    path('python/', views.python_index, name='python'),
    path('run/', views.run_python, name='run_code'),
]
