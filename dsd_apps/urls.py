from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('all_courses/',views.all_courses,name='all_courses'), #done
    # ________________javascript Compiler __________________
    path('javascript/', views.javascript_index, name='javascript'), #done
    path('java/', views.java_index, name='java'),
    path('run_java_code/', views.run_java_code, name='run_java_code'),
    path('r/', views.r_index, name='r'),  # 'R' should be lowercase for the URL
    path('php/', views.php_index, name='php'),
    path('csharp/', views.csharp_index, name='csharp'),  # Avoid special characters in URLs
    path('sql/', views.sql_index, name='sql'),
    path('html/', views.html_index, name='html'),   # done
    # ____________________c compiler __________________________
    path('c/',views.c_index,name='c'), #done
    path('c_run_code/', views.c_run_code, name='c_run_code'),  #done
    # _________________cpp compiler ______________________________
    path('cpp/',views.cpp_index,name='cpp'), #done
    path('cpp_run_code/',views.cpp_run_code,name='cpp_run_code'), #done
    
    # _______________python section ____________________
    path('python/', views.python_index, name='python'),  #done
    path('run/', views.run_python, name='run_code'), #done
    # _______________swift section _______________________
    path('swift/', views.swift_index, name='swift'),  #done
    path('run_swift_code/', views.run_swift_code, name='run_swift_code'),
]
