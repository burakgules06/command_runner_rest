import os.path
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Command
from threading import Thread
import subprocess


import os.path
import subprocess
from django.utils import timezone
from .models import Command


def command_run(command):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    date_now = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f'{date_now}_{command}.log')
    print(log_file)

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status = 1

    file = Command(command=command, output_file=log_file, command_start_date=timezone.now(), status=status)
    file.save()

    while process.poll() is None:
        time.sleep(1)

    stdout, stderr = process.communicate()

    if process.returncode == 0:
        status = 0
    elif process.returncode is not None and process.returncode != 0:
        status = 2

    with open(log_file, 'w') as f:
        f.write(stdout.decode())

    file.status = status
    file.command_end_date = timezone.now()
    file.save()

    return status, log_file


def command_run_threaded(command):
    def run_command(command):
        status, log_file = command_run(command)
        results.append((status, log_file))

    results = []
    thread = Thread(target=run_command, args=(command,))
    thread.start()

    return thread


def request(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        thread = command_run_threaded(command)
        return JsonResponse({'status': 'success', 'message': f'Command "{command}" is being executed.'})

    else:
        return render(request, 'index.html')


def command_status(request):
    status = request.GET.get('status')
    if status is None:
        return JsonResponse({'status': 'error', 'message': 'Please provide a status parameter.'})

    if status == '0':
        commands = Command.objects.filter(status=0).values()
    elif status == '1':
        commands = Command.objects.filter(status=1).values()
    elif status == '2':
        commands = Command.objects.filter(status=2).values()
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid status parameter.'
})

    return JsonResponse({'commands': list(commands)})


