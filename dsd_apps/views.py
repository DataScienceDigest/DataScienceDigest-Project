from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')
def docs(request):
    return render(request,'docs.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

@csrf_exempt  # Allows POST requests without CSRF token for testing purposes
def run_code(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        try:
            # Execute Python code using subprocess, ensure correct Python path
            result = subprocess.run(
                ['python3', '-c', code],  # Use 'python' or 'python3' based on your setup
                capture_output=True, 
                text=True, 
                timeout=10  # Avoid infinite loops
            )
            output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            output = str(e)
        return JsonResponse({'output': output})
    return JsonResponse({'error': 'Invalid request'}, status=400)