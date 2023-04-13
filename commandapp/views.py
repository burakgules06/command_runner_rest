import os.path
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Command
from threading import Thread
import subprocess


def command_run(command):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    date_now = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f'{date_now}_{command}.log')
    print(log_file)

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status = None
    while process.poll() is None:
        print('Process is still running.')

    with open(log_file, 'w') as f:
        stdout, stderr = process.communicate()
        f.write(stdout.decode())
    status = 1
    if process.returncode == 0:
        status = 0
    elif process.returncode is not None and process.returncode != 0:
        status = 2
    else:
        status = 1
    print(status)
    file = Command(output_file=log_file, command_start_date=timezone.now(), status=status,
                   command_end_date=timezone.now())
    file.save()
    return status, log_file


def request(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        status, log_file = command_run(command)
        if status == 0:
            return JsonResponse({'status': 'success', 'message': f'Command "{command}" is being executed.'})
        elif status == 1:
            return JsonResponse({'status': 'running', 'message': f'Command "{command}" is still running.'})
        elif status == 2:
            with open(log_file, 'r') as f:
                log_content = f.read()
            return JsonResponse({'status': 'fail', 'message': f'Command "{command}" could not be executed.',
                                 'log_content': log_content})

    else:
        return render(request, 'index.html')
