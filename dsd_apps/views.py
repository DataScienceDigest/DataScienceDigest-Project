from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import json
import os
def index(request):
    return render(request, 'index.html')
def all_courses(request):
    return render(request, 'all_courses.html')

@csrf_exempt
def run_python(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        inputs = request.POST.getlist('inputs[]', [])
        inputs = inputs[0].split(',')        
        try:
            # Handling input
            process = subprocess.Popen(
                ['python3', '-c', code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Simulate input for the subprocess
            input_data = "\n".join(inputs) + "\n"
            stdout, stderr = process.communicate(input=input_data, timeout=10)
            # Capture and return output or errors
            output = stdout if process.returncode == 0 else stderr
        except subprocess.TimeoutExpired:
            output = "Execution timed out after 10 seconds."
        except Exception as e:
            output = str(e)
        return JsonResponse({'output': output})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def python_index(request):
    return render(request, 'python.html')

def javascript_index(request):
    return render(request, 'javascript.html')

def c_cpp_index(request):
    return render(request,'c_compiler.html')

def java_index(request):
    return render(request, 'java.html')

def r_index(request):
    return render(request, 'r.html')

def php_index(request):
    return render(request, 'php.html')

def csharp_index(request):
    return render(request, 'csharp.html')

def sql_index(request):
    return render(request, 'sql.html')

def html_index(request):
    return render(request, 'html.html')

def css_index(request):
    return render(request, 'css.html')


# c and c++ compilers 
