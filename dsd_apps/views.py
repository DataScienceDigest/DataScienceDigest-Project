from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import json
import os
import tempfile

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


@csrf_exempt
def c_run_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data['code']

        # Create a temporary file to store the C code
        with tempfile.NamedTemporaryFile(suffix='.c', delete=False) as temp_c_file:
            temp_c_file.write(code.encode())
            temp_c_file_name = temp_c_file.name

        # Path to gcc.exe
        # gcc_path = r'C:\Users\hp\Documents\DataScienceDigest_mainProject\DataScienceDigest-Project\gcc\bin\gcc.exe'
        gcc_path= '/usr/bin/gcc'

        try:
            # Compile the C code using gcc.exe
            compile_process = subprocess.run(
                [gcc_path, temp_c_file_name, '-o', temp_c_file_name[:-2], '-Wl,-subsystem,console'],
                capture_output=True, text=True
            )

            # Print the stderr and stdout for debugging
            print("Compilation STDOUT:", compile_process.stdout)
            print("Compilation STDERR:", compile_process.stderr)

            if compile_process.returncode != 0:
                return JsonResponse({'output': compile_process.stderr})

            # Run the compiled C program
            run_process = subprocess.run(
                [temp_c_file_name[:-2]], capture_output=True, text=True
            )

            # Print the stderr and stdout for debugging
            print("Execution STDOUT:", run_process.stdout)
            print("Execution STDERR:", run_process.stderr)

            # Clean up the temp file
            os.remove(temp_c_file_name)

            return JsonResponse({'output': run_process.stdout if run_process.returncode == 0 else run_process.stderr})

        except FileNotFoundError as e:
            return JsonResponse({'output': f'GCC executable not found: {str(e)}'})

        except Exception as e:
            return JsonResponse({'output': f'Error: {str(e)}'})

    return JsonResponse({'output': 'Invalid request'})