from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('all-courses/',views.all_courses,name='all_courses'), #done
    path('all-compilers/',views.all_compilers,name='all_compilers'),
    # ________________javascript Compiler __________________
    path('javascript-tutorial/', views.javascript_index, name='javascript-tutorial'), #done
    path('java-tutorial/', views.java_index, name='java-tutorial'),     # done 
    path('run_java_code/', views.run_java_code, name='run_java_code'),
    path('r-tutorial/', views.r_index, name='r-tutorial'),  # 'R' should be lowercase for the URL
    path('run_r_code/',views.run_r_code,name='run_r_code'),
    path('php-tutorial/', views.php_index, name='php-tutorial'),
    path('php_run_code/',views.php_run_code,name='php_run_code'),
    path('csharp-tutorial/', views.csharp_index, name='csharp-tutorial'),  # Avoid special characters in URLs
    path('csharp_run_code/',views.csharp_run_code,name='csharp_run_code'),
    path('sql-tutorial/', views.sql_index, name='sql-tutorial'),
     path('execute_sql/', views.execute_sql, name='execute_sql'),
    path('html-tutorial/', views.html_index, name='html-tutorial'),   # done
    # ____________________c compiler __________________________
    path('c-tutorial/',views.c_index,name='c-tutorial'), #done
    path('c_run_code/', views.c_run_code, name='c_run_code'),  #done
    # _________________cpp compiler ______________________________
    path('cpp-tutorial/',views.cpp_index,name='cpp-tutorial'), #done
    path('cpp_run_code/',views.cpp_run_code,name='cpp_run_code'), #done
    
    # _______________python section ____________________
    path('python-tutorial/', views.python_index, name='python-tutorial'),  #done
    path('run/', views.run_python, name='run_code'), #done
    # _______________swift section _______________________
    path('swift-tutorial/', views.swift_index, name='swift-tutorial'),  #done
    path('run_swift_code/', views.run_swift_code, name='run_swift_code'),
    # _______________go section _______________________
    path('go-tutorial/', views.go_index, name='go-tutorial'), #done
    path('go_run_code/', views.go_run_code, name='go_run_code'),
    # _______________rust section _______________________
    path('rust-tutorial/', views.rust_index, name='rust-tutorial'),
    path('compile_rust/',views.compile_rust,name='compile_rust'),
    # ______________perl section ___________________________
    path('perl-tutorial/',views.perl_index, name='perl-tutorial'),
    path('run_perl_code/',views.run_perl_code,name='run_perl_code'),
    # ______________ruby section __________________________
    path('ruby-tutorial/',views.ruby_index, name='ruby-tutorial'),
    path('run_ruby_code/', views.run_ruby_code, name='run_ruby_code'),
    # _______________julis section _______________________
    path('julia-tutorial/',views.julia_index,name='julia-tutorial'),
    path('run_julia_code/',views.run_julia_code,name='run_julia_code'),
    # _________________scala section _____________________
    path('scala-tutorial/',views.scala_index,name='scala-tutorial'),
    path('run_scala_code/',views.run_scala_code,name='run_scala_code'),
    # ________________kotlin Section _______________________
    path('kotlin-tutorial/',views.kotlin_index,name='kotlin-tutorial'),
    path('run_kotlin_code/',views.run_kotlin_code,name='run_kotlin_code'),
    
]
