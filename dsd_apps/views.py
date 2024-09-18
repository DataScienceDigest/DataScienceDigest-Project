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

def all_compilers(request):
    return render(request,'all_compilers.html')
def python_index(request):
    return render(request, 'python.html')

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


def javascript_index(request):
    return render(request, 'javascript.html')

def cpp_index(request):
    return render(request,'cpp_compiler.html')
# 
def c_index(request):
    return render(request,'c_compiler.html')
#  java editor 
def java_index(request):
    return render(request, 'java.html')

def r_index(request):
    return render(request, 'r.html')
# r compiler 
@csrf_exempt
def run_r_code(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body.decode('utf-8'))
            code = data.get('code')
            inputs = data.get('inputs', [])
            # Create an R script with the provided code
            script_file = 'script.R'
            with open(script_file, 'w') as file:
                file.write(code)

            # Prepare the R environment to handle inputs
            input_file = 'inputs.txt'
            with open(input_file, 'w') as file:
                for user_input in inputs:
                    file.write(user_input + '\n')

            # Run the R script
            result = subprocess.run(
                ['Rscript', '--vanilla', script_file],
                input='\n'.join(inputs),  # Provide inputs to the R script
                text=True,
                capture_output=True
            )

            # Read the output from the R script
            output = result.stdout
            error = result.stderr if result.stderr else None

            # Return the output and error (if any) as JSON
            return JsonResponse({'output': output, 'error': error})
        except Exception as e:
            # Log the exception to the console or to a file
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=400)

def php_index(request):
    return render(request, 'php.html')

def csharp_index(request):
    return render(request, 'csharp.html')

def sql_index(request):
    return render(request, 'sql.html')
# html code editor
def html_index(request):
    return render(request, 'html.html')

# swift compiler
def swift_index(request):
    return render(request, 'swift_compiler.html')

# swift code 

@csrf_exempt
def run_swift_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code')
            user_input = data.get('input', '')  # Default to empty if not provided
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        # Save the Swift code to a temporary file
        file_path = "/tmp/user_code.swift"
        with open(file_path, 'w') as file:
            file.write(code)

         # Ensure Swift is available in PATH
        os.environ["PATH"] += os.pathsep + "/usr/local/swift/usr/bin"

        try:
            # Run swift compiler
            if "readLine()" in code:
                # If the code expects input, provide it using subprocess
                result = subprocess.run(
                    ['swift', file_path],
                    input=user_input,  # Pass user input to the Swift code
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
            else:
                # If no input is expected
                result = subprocess.run(
                    ['swift', file_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

            return JsonResponse({
                'output': result.stdout or result.stderr
            })
        except Exception as e:
            return JsonResponse({'output': str(e)})

    return JsonResponse({'error': 'Invalid request method.'})

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
        user_input = data.get('input', '')

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

                # Run the Java program and pass the user input
                run_process = subprocess.run(
                    ['java', '-cp', temp_dir, 'Main'],
                    input=user_input,  # Pass user input to the program
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
    
# go index
def go_index(request):
    return render(request, 'go.html')
# go compiler
@csrf_exempt
def go_run_code(request):
    if request.method == 'POST':
        try:
            # Extract Go code and optional input from the JSON request body
            data = json.loads(request.body)
            go_code = data.get('code', '')
            user_input = data.get('inputs', '')
            print(go_code,'===-=-=-==')
            # Save the Go code to a temporary file
            file_path = "/tmp/user_code.go"
            with open(file_path, 'w') as file:
                file.write(go_code)

            try:
                # Compile and run the Go code
                result = subprocess.run(
                    ['/usr/bin/go', 'run', file_path],
                    input=user_input,  # Pass user input if needed
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                # Send back the output (or error) in JSON format
                return JsonResponse({
                    'output': result.stdout or result.stderr
                })
            except Exception as e:
                return JsonResponse({'output': str(e)})

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON input.'})
    return JsonResponse({'error': 'Invalid request method.'})
# rust index
def rust_index(request):
    return render(request, 'rust.html')
# rust editor
@csrf_exempt
def compile_rust(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rust_code = data.get('code')  # Get the Rust code from JSON
            user_input = data.get('input')  # Get user input for the Rust program
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        # Write the Rust code to a file
        file_path = '/tmp/user_code.rs'
        with open(file_path, 'w') as rust_file:
            rust_file.write(rust_code)

        try:
            # Compile the Rust code
            compile_result = subprocess.run(
                ['rustc', file_path, '-o', '/tmp/user_code'], 
                capture_output=True, text=True, timeout=10
            )

            # If there are compilation errors, return them
            if compile_result.returncode != 0:
                return JsonResponse({'status': 'error', 'output': compile_result.stderr})

            # Run the compiled code, providing the user input
            execution_result = subprocess.run(
                ['/tmp/user_code'], 
                input=user_input, capture_output=True, text=True, timeout=10
            )

            # Return the output of the program
            if execution_result.returncode == 0:
                return JsonResponse({'status': 'success', 'output': execution_result.stdout})
            else:
                return JsonResponse({'status': 'error', 'output': execution_result.stderr})

        except subprocess.TimeoutExpired:
            return JsonResponse({'status': 'error', 'output': 'Execution timed out'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'output': str(e)})

    return JsonResponse({'status': 'error', 'output': 'Invalid request method'})

# php editor 
@csrf_exempt
def php_run_code(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload from request body
            data = json.loads(request.body.decode('utf-8'))
            code = data.get('code', '')
            inputs = data.get('inputs', [])

            # Create temporary PHP file
            file_path = "/tmp/temp_code.php"
            with open(file_path, 'w') as php_file:
                php_file.write(code)

            # Execute PHP code with inputs (if any)
            try:
                result = subprocess.run(
                    ['php', file_path], 
                    input="\n".join(inputs), 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True, 
                    timeout=10
                )
                output = result.stdout
                error = result.stderr
            except subprocess.TimeoutExpired:
                return JsonResponse({"output": "", "error": "Code execution timed out."})

            # Clean up the temporary file
            os.remove(file_path)

            # Return output or error as JSON
            return JsonResponse({"output": output, "error": error})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)
