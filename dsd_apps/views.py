from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import re

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        inputs = request.POST.getlist('inputs[]', [])
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
