from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import json
import os
import tempfile
import sqlite3
from django.conf import settings 
from django.http import FileResponse
import re

def ads_txt_view(request):
    ads_path = settings.BASE_DIR / 'static/ads.txt'
    with open(ads_path) as f:
        return HttpResponse(f.read(), content_type="text/plain")


def sitemap_view(request):
    # Assuming the file is in a folder named 'static/sitemaps/' in your project root
    file_path = os.path.join(settings.BASE_DIR, 'static/sitemaps/sitemap.xml')
    return FileResponse(open(file_path, 'rb'), content_type='application/xml')

def index(request):
    return render(request, 'index.html')

def single(request):
    return render(request,'htmltest.html')

def all_courses(request):
    return render(request, 'all_courses.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def user_login(request):
    return render(request,'login.html')
def signup(request):
    return render(request,'signup.html')

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

# @csrf_exempt
# def run_r_code(request):
#     if request.method == 'POST':
#         try:
#             # Parse JSON data from the request body
#             data = json.loads(request.body)
#             code = data.get('code', '')
            
#             # Combine inputs into a single string separated by newlines
#             inputs = "\n".join(data.get('inputs', []))
#             print(f"Inputs received: {inputs}")  # Debugging log for input received
            
#             # Create a temporary R script file
#             with tempfile.TemporaryDirectory() as temp_dir:
#                 script_file = os.path.join(temp_dir, 'script.R')
#                 with open(script_file, 'w') as file:
#                     file.write(code)

#                 result = subprocess.run(
#                     ['Rscript', '--vanilla', script_file],
#                     input=inputs,  # Provide inputs directly to R script via stdin
#                     text=True,  # Handle input and output as strings
#                     capture_output=True,  # Capture stdout and stderr for easier debugging
#                     timeout=10  # Optional: timeout to prevent infinite execution
#                 )

#                 # Check if the command was successful
#                 if result.returncode == 0:
#                     print("Output:", result.stdout)  # Print the output of the R script
#                 else:
#                     print("Error:", result.stderr) 
                
#                 output = result.stdout
#                 error = result.stderr
#                 print(result,'--==-=-=-=')

#                 # Capture the output and error (if any) from the R script execution
#                 output = result.stdout
#                 error = result.stderr if result.stderr else None

#             # Return the output and error (if any) as JSON
#             return JsonResponse({'output': output, 'error': error})
        
#         except Exception as e:
#             # Log the exception to the console or to a file
#             print(f"Error: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Only POST method is allowed'}, status=400)

@csrf_exempt
def run_r_code(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            code = data.get('code', '')
            # inputs = "\n".join(data.get('inputs', [])) # Expected as a list of input values
            inputs = data.get('inputs', [])  # Expected as a list of input values
            print(f"Inputs received: {inputs}")  # Debugging log for input received

            # Create a temporary R script file
            with tempfile.TemporaryDirectory() as temp_dir:
                script_file = os.path.join(temp_dir, 'script.R')
                with open(script_file, 'w') as file:
                    file.write(code)

                # Run the R script with inputs as command-line arguments
                result = subprocess.run(
                    ['Rscript', '--vanilla', script_file] + inputs,  # Add inputs as arguments
                    text=True,  # Handle output as string
                    capture_output=True,  # Capture stdout and stderr for easier debugging
                    timeout=10  # Optional: timeout to prevent infinite execution
                )

                # Check if the command was successful
                if result.returncode == 0:
                    print("Output:", result.stdout)  # Print the output of the R script
                    output = result.stdout.strip()  # Clean up the output
                    error = None  # No error if return code is 0
                else:
                    print("Error:", result.stderr)
                    output = result.stderr.strip()  # Capture the error output
                    error = "An error occurred during execution."

                print(result, '--==-=-=-=')

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

@csrf_exempt  # Bypass CSRF for now (for simplicity)
def execute_sql(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            query = data.get('query', '').strip()

            if not query:
                return JsonResponse({'error': 'No query provided'}, status=400)

            # Path to the database file in your project folder
            db_path = str(settings.BASE_DIR / "db.sqlite3")
            # Ensure the database file exists before proceeding
            if not os.path.exists(db_path):
                return JsonResponse({'error': 'Database file not found'}, status=500)
            # Connect to the SQLite database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            try:
                query_lower = query.lower()

                # Handle SELECT queries separately
                if query_lower.startswith('select'):
                    cursor.execute(query)
                    result = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]  # Extract column names
                    return JsonResponse({
                        'columns': columns,
                        'result': result
                    })

                # Execute other types of queries (INSERT, UPDATE, DELETE, CREATE, etc.)
                cursor.execute(query)
                conn.commit()

                # Determine if we need to fetch data from an affected table
                table_name = None

                if query_lower.startswith('insert into'):
                    table_name = query.split()[2]  # Extract table name after 'insert into'
                elif query_lower.startswith('update'):
                    table_name = query.split()[1]  # Extract table name after 'update'
                elif query_lower.startswith('delete from'):
                    table_name = query.split()[2]  # Extract table name after 'delete from'
                elif query_lower.startswith('create table'):
                    table_name = query.split()[2]  # Extract table name after 'create table'
                elif query_lower.startswith('alter table'):
                    table_name = query.split()[2]  # Extract table name after 'alter table'

                if table_name:
                    # Fetch data from the affected table to show the updated content
                    cursor.execute(f'SELECT * FROM {table_name}')
                    result = cursor.fetchall()

                    # Fetch column names
                    cursor.execute(f'PRAGMA table_info({table_name})')
                    columns = [col[1] for col in cursor.fetchall()]

                    return JsonResponse({
                        'columns': columns,
                        'result': result
                    })
                else:
                    # No table affected; return a success message for other queries
                    return JsonResponse({'result': "Query executed successfully."})

            except Exception as e:
                return JsonResponse({'error': str(e)})

            finally:
                conn.close()

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


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
            user_input = "\n".join(data.get('inputs', []))  # Default to empty if not provided
            print(user_input,'-=-=-=-=-')
            # user_input = data.get('inputs', '')  # Default to empty if not provided
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
            # user_inputs = data.get('inputs', [])  # Get user inputs if any
            user_inputs = "\n".join(data.get('inputs', []))
            print(user_inputs,'-=-=-=-=')
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
            # user_inputs = data.get('inputs', [])  # Get user inputs if any
            user_inputs = "\n".join(data.get('inputs', []))
            print(user_inputs,'_+_+_+_+_')
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
        user_input = "\n".join(data.get('inputs', []))
        # Extract the class name using a regex
        match = re.search(r'class\s+(\w+)', java_code)
        if not match:
            return JsonResponse({'output': 'Error: No valid class found in code.'})
        
        class_name = match.group(1)
        # Create a temporary directory to store the Java file
        with tempfile.TemporaryDirectory() as temp_dir:
            java_file_path = os.path.join(temp_dir, f"{class_name}.java")

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
                    ['java', '-cp', temp_dir,  class_name],
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
            # user_input = data.get('inputs', '')
            user_input = "\n".join(data.get('inputs', []))
            print(user_input,'===-=-=-==')
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
            user_input = "\n".join(data.get('inputs', []))
            print(user_input,'-=-=-=-=')
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

# # php editor 
@csrf_exempt
def php_run_code(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload from the request body
            data = json.loads(request.body.decode('utf-8'))
            code = data.get('code', '')
            inputs = data.get('inputs', [])
            print(f"Inputs received: {inputs}")

            # Create a temporary PHP file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.php') as temp_file:
                temp_file.write(code.encode('utf-8'))
                temp_file_path = temp_file.name

            try:
                # Execute PHP code with inputs (if any)
                result = subprocess.run(
                    ['php', temp_file_path],
                    input="\n".join(inputs),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10
                )
                output = result.stdout
                error = result.stderr

            except subprocess.TimeoutExpired:
                output = ""
                error = "Code execution timed out."

            finally:
                # Clean up the temporary file
                os.remove(temp_file_path)

            # Return output or error as JSON
            return JsonResponse({"output": output, "error": error})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

# c# compiler 

@csrf_exempt
def csharp_run_code(request):
    if request.method == 'POST':
        # Use json.loads() to parse the JSON body from the request
        data = json.loads(request.body)
        code = data.get('code', '')
        inputs = data.get('inputs', [])
        print(code,'-=-=-=',inputs,'=====')

        # Write code to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".cs") as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file_path = temp_file.name

        try:
            # Compile the C# code
            compile_process = subprocess.run(
                ['mcs', temp_file_path],
                capture_output=True, text=True
            )

            if compile_process.returncode == 0:
                # If compilation succeeded, run the compiled executable
                exe_file = temp_file_path.replace(".cs", ".exe")

                # Join inputs with newline characters (to simulate multiple Console.ReadLine calls)
                input_string = "\n".join(inputs)

                run_process = subprocess.run(
                    ['mono', exe_file],
                    input=input_string,  # Pass input to stdin
                    capture_output=True, text=True
                )
                output = run_process.stdout + run_process.stderr
            else:
                output = compile_process.stderr
        finally:
            # Clean up temporary files
            os.remove(temp_file_path)
            exe_file = temp_file_path.replace(".cs", ".exe")
            if os.path.exists(exe_file):
                os.remove(exe_file)

        return JsonResponse({'output': output})

    return JsonResponse({'output': 'Invalid request method'}, status=400)

def perl_index(request):
    return render(request, 'perl.html')

# perl editor 
@csrf_exempt
def run_perl_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Capture JSON data
        code = data.get('code')          # Perl code
        input_data = "\n".join(data.get('inputs', []))  # Input data for Perl code
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.pl', delete=False) as temp_file:
            temp_file.write(code.encode())
            temp_file_path = temp_file.name  # Save the file path

        try:
            # Execute the Perl code, pass input data through stdin
            result = subprocess.run(
                ['perl', temp_file_path],
                input=input_data,               # Pass input data to the Perl script
                capture_output=True, text=True, timeout=5
            )
            output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            output = str(e)
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)

        return JsonResponse({'output': output})
    
# ruby code editor 
def  ruby_index(request):
    return render(request, 'ruby.html')
@csrf_exempt
def run_ruby_code(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data from the request body
            data = json.loads(request.body)
            code = data.get('code', '')
            inputs = data.get('inputs', [])  # List of inputs (if any)
            print(data,'-=-=-=-=')
            # Save the Ruby code to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.pl', delete=False) as temp_file:
                temp_file.write(code.encode())
                temp_file_path = temp_file.name 

            # Convert the input list into a string format (newlines between inputs)
            input_data = "\n".join(inputs)

            try:
                # Execute the Ruby code using subprocess, providing inputs through stdin
                result = subprocess.run(
                    ['ruby', temp_file_path], 
                    input=input_data,  # Send user inputs to the Ruby script
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                output = result.stdout
                error = result.stderr
            except subprocess.TimeoutExpired:
                error = 'Execution timed out'
                output = ''

            # Cleanup: Remove the temporary Ruby file after execution
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

            # Return the output or error back to the frontend
            return JsonResponse({'output': output, 'error': error})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# julia section
def julia_index(request):
    return render(request, 'julia.html')
@csrf_exempt
def run_julia_code(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data from the request body
            data = json.loads(request.body)
            code = data.get('code', '')
            inputs = data.get('inputs', [])  # List of inputs (if any)
            print(code,'---',inputs)
            # Save the Julia code to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.jl', delete=False) as temp_file:
                temp_file.write(code.encode())
                temp_file_path = temp_file.name

            # Prepare the input string, assuming inputs are passed line by line
            input_str = '\n'.join(map(str, inputs))  # Ensure inputs are string formatted

            # Execute the Julia code, passing inputs as stdin
            result = subprocess.run(
                ['julia', temp_file_path],
                input=input_str,  # Pass the input values as standard input
                capture_output=True, 
                text=True, 
                timeout=20  # Increased timeout to 20 seconds
            )

            # Remove the temporary file after execution
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

            # Return the output and any error messages
            return JsonResponse({'output': result.stdout, 'error': result.stderr})
        except subprocess.TimeoutExpired:
            return JsonResponse({'error': 'Execution timed out. Your code might be taking too long to run.'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        

# scala editor
def scala_index(request):
    return render(request,'scala.html')

@csrf_exempt
def run_scala_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            inputs = data.get('inputs', [])  # Optional input handling
            if not code:
                return JsonResponse({'error': 'No Scala code provided'}, status=400)

            # Create a temporary file for the Scala code
            with tempfile.NamedTemporaryFile(suffix='.scala', delete=False) as temp_file:
                temp_file.write(code.encode())
                temp_file_path = temp_file.name

            try:
                # Prepare input string if inputs exist
                input_str = '\n'.join(inputs) if inputs else ''

                # Run the Scala script without compiling
                run_result = subprocess.run(
                    ['/home/ubuntu/.sdkman/candidates/scala/current/bin/scala', temp_file_path],  # Use full path to Scala
                    input=input_str,
                    capture_output=True,
                    text=True,
                )
                # Clean up files
                os.remove(temp_file_path)

                # Return the output or error
                return JsonResponse({
                    'output': run_result.stdout,
                    'error': run_result.stderr
                })

            except Exception as e:
                # Handle exceptions
                return JsonResponse({'error': str(e)}, status=500)

        finally:
            # Ensure the temp file is cleaned up
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# kotlin compiler
def kotlin_index(request):
    return render(request,'kotlin.html')
@csrf_exempt
def run_kotlin_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            inputs = data.get('inputs', [])  # Optional input handling
            print(code,'-=-=-=-=',inputs)
            if not code:
                return JsonResponse({'error': 'No Kotlin code provided'}, status=400)
            # Save the Kotlin code to a file
            file_path = "/tmp/code.kt"
            jar_path = '/tmp/code.jar'
            with open(file_path, 'w') as file:
                file.write(code)
            os.chmod(file_path, 0o755)
            os.chmod(jar_path, 0o755)

            try:

                compile_result = subprocess.run(
                ['/home/ubuntu/.sdkman/candidates/kotlin/current/bin/kotlinc', file_path, '-include-runtime', '-d', jar_path],
                capture_output=True, text=True, timeout=10
                )
                # Check if compilation failed
                if compile_result.returncode != 0:
                    return JsonResponse({
                        'output': compile_result.stdout,
                        'error': compile_result.stderr
                    })
                # Check if the JAR file exists
                if not os.path.exists(jar_path):
                    return JsonResponse({'output': 'Error: JAR file not created'})

                run_result = subprocess.run(
                ['java', '-jar', jar_path],
                input='\n'.join(inputs) if inputs else '',
                capture_output=True, text=True, timeout=20
                )
                # Return the output or error
                return JsonResponse({
                    'output': run_result.stdout,
                    'error': run_result.stderr
                })

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
