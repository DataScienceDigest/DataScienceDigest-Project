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

def cpp_index(request):
    return render(request,'cpp_compiler.html')

def c_index(request):
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


# c and c++ compilers 


@csrf_exempt
def c_run_code(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            code = data.get('code', '')
            user_inputs = data.get('inputs', [])  # Get user inputs if any
            # Path to gcc on Ubuntu
            gcc_path = '/usr/bin/gcc'
            # Create a temporary file to store the C code
            with tempfile.NamedTemporaryFile(suffix='.c', delete=False) as temp_c_file:
                temp_c_file.write(code.encode())
                temp_c_file_name = temp_c_file.name

            # Compile the C code using gcc
            compiled_output = temp_c_file_name[:-2]  # Remove .c to get the executable name
            compile_process = subprocess.run(
                [gcc_path, temp_c_file_name, '-o', compiled_output],
                capture_output=True, text=True
            )

            # Check if compilation was successful
            if compile_process.returncode != 0:
                return JsonResponse({'output': compile_process.stderr})

            # Give execute permission to the compiled binary
            os.chmod(compiled_output, 0o755)

            # Prepare the input for the C program (join all inputs with newlines)
            input_data = '\n'.join(user_inputs) if user_inputs else None

            # Run the compiled C program with user inputs
            run_process = subprocess.run(
                [compiled_output],
                input=input_data, text=True, capture_output=True
            )

            # Clean up the temp files
            os.remove(temp_c_file_name)
            os.remove(compiled_output)

            # Return the program output or error
            return JsonResponse({'output': run_process.stdout if run_process.returncode == 0 else run_process.stderr})

        except FileNotFoundError:
            return JsonResponse({'output': 'gcc not found. Please check the path.'})

        except Exception as e:
            return JsonResponse({'output': f'Error: {str(e)}'})

    return JsonResponse({'output': 'Invalid request method'})

# cpp code compiler
@csrf_exempt
def cpp_run_code(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            code = data.get('code', '')
            user_inputs = data.get('inputs', [])  # Get user inputs if any
            # Path to g++ on Ubuntu
            gpp_path = '/usr/bin/g++'
            # Create a temporary file to store the C++ code
            with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False) as temp_cpp_file:
                temp_cpp_file.write(code.encode())
                temp_cpp_file_name = temp_cpp_file.name

            # Compile the C++ code using g++
            compiled_output = temp_cpp_file_name[:-4]  # Remove .cpp to get the executable name
            compile_process = subprocess.run(
                [gpp_path, temp_cpp_file_name, '-o', compiled_output],
                capture_output=True, text=True
            )

            # Check if compilation was successful
            if compile_process.returncode != 0:
                return JsonResponse({'output': compile_process.stderr})

            # Give execute permission to the compiled binary
            os.chmod(compiled_output, 0o755)

            # Prepare the input for the C++ program (join all inputs with newlines)
            input_data = '\n'.join(user_inputs) if user_inputs else None

            # Run the compiled C++ program with user inputs
            run_process = subprocess.run(
                [compiled_output],
                input=input_data, text=True, capture_output=True
            )

            # Clean up the temp files
            os.remove(temp_cpp_file_name)
            os.remove(compiled_output)

            # Return the program output or error
            return JsonResponse({'output': run_process.stdout if run_process.returncode == 0 else run_process.stderr})

        except FileNotFoundError:
            return JsonResponse({'output': 'g++ not found. Please check the path.'})

        except Exception as e:
            return JsonResponse({'output': f'Error: {str(e)}'})

    return JsonResponse({'output': 'Invalid request method'})

# java compiler code 
@csrf_exempt
def run_java_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        java_code = data.get('code', '')

        # Create a temporary directory to store the Java file
        with tempfile.TemporaryDirectory() as temp_dir:
            java_file_path = os.path.join(temp_dir, "Main.java")
            
            # Write the Java code to a file
            with open(java_file_path, "w") as java_file:
                java_file.write(java_code)

            try:
                # Compile the Java code
                compile_process = subprocess.run(
                    ['javac', java_file_path],
                    capture_output=True,
                    text=True
                )

                if compile_process.returncode != 0:
                    return JsonResponse({
                        'output': 'Compilation Error:\n' + compile_process.stderr
                    })

                # Run the Java program
                run_process = subprocess.run(
                    ['java', '-cp', temp_dir, 'Main'],
                    capture_output=True,
                    text=True
                )

                if run_process.returncode == 0:
                    return JsonResponse({
                        'output': run_process.stdout
                    })
                else:
                    return JsonResponse({
                        'output': 'Runtime Error:\n' + run_process.stderr
                    })

            except Exception as e:
                return JsonResponse({
                    'output': 'Error executing Java code:\n' + str(e)
                })
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
