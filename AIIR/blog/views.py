from PIL import Image
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import paramiko
from django.contrib.auth.models import User
from .models import Request
from .models import Algorithm
from django.contrib.auth import authenticate, login as auth_login
from datetime import datetime
import time
import threading



def home(request):
    return render(request, 'blog/login.html')


def about(request):
    return render(request, 'blog/about.html')


@api_view(['GET', 'POST'])
def registration(request):
    if request.method == "GET":
        return render(request, 'blog/registration.html')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.get(email=email)
            return render(request, 'blog/registration.html', {'msg': "user with this email already exist"})
        except User.DoesNotExist:
            User.objects.create_user(first_name=first_name, last_name=last_name, username=email,
                                     email=email, password=password)
            return render(request, 'blog/login.html', {'msg': "user created successfully"})


@api_view(['POST'])
def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        auth_login(request, user)
        request.GET._mutable = True
        request.GET['user_id'] = user.id
        return task_manager(request._request)
    return render(request, 'blog/login.html', {'msg': "email or password are invalid"})


@api_view(['GET', 'POST'])
def task_manager(request):
    user = User.objects.get(id=request.GET['user_id'])
    data = Request.objects.select_related().filter(user=user)
    return render(request, 'blog/task_manager.html', {'data': data, 'user_id': user.id})


@api_view(['POST'])
def execute_algorithm(request):
    first_param = request.data['firstParam']
    second_param = request.data['secondParam']
    third_param = request.data['thirdParam']
    user_id = int(request.data['user_id'])

    user = User.objects.get(id=user_id)
    algorithm = Algorithm.objects.get(algorithm_name="mandelbrot")
    new_task = Request.objects.create(user=user, algorithm=algorithm, date=datetime.now(), parameter1=first_param,
                                      parameter2=second_param, parameter3=third_param, status="In queue", progress1=0,
                                      progress2=0, progress3=0, image_url="../../static/images/fractal_square.jpg")
    threading.Thread(target=send_task_to_master).start()
    return Response(new_task.id, status.HTTP_200_OK)


master_busy = False


def send_task_to_master():
    global master_busy

    while master_busy:
        time.sleep(10)
    master_busy = True
    for new_task in Request.objects.select_related().filter(status="In queue"):
        host = '192.168.0.109'
        port = 22
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username="vm1", password="wlodek", port=port)
        stdin, stdout, stderr = client.exec_command('./run.sh ' + new_task.first_param
                                                    + ' ' + new_task.second_param + ' ' + new_task.third_param)
        stdin.close()
        progress1 = 0
        progress2 = 0
        progress3 = 0
        count = 0
        for line in iter(lambda: stdout.readline(2048), ""):
            if '::' in line:
                count += 1
                array = line.split(":: ")
                info = array[0]
                progress = array[1].replace('\n', '')
                if info == "Master":
                    progress1 = progress
                elif info == "Slave1":
                    progress2 = progress
                elif info == "Slave2":
                    progress3 = progress
                if count % 50:
                    new_task.progress1 = progress1
                    new_task.progress2 = progress2
                    new_task.progress3 = progress3
                    new_task.save()
        client.close()
        client.close()
        transport = paramiko.Transport(host, port)
        transport.connect(username='vm1', password='wlodek')
        sftp = paramiko.SFTPClient.from_transport(transport)

        remotepath = '/home/vm1/out.png'
        localpath = 'out.png'
        sftp.get(remotepath, localpath)
        sftp.close()
        transport.close()

        image = Image.open('out.png')
        bg = Image.new('RGB', image.size, (255, 255, 255))
        bg.paste(image, (0, 0), image)
        bg.save("./blog/static/images/img" + str(new_task.id) + ".jpg", quality=95)

        new_task.progress1 = progress1
        new_task.progress2 = progress2
        new_task.progress3 = progress3
        new_task.image_url = "../../static/images/img" + str(new_task.id) + ".jpg"
        new_task.status = "Done"
        new_task.save()
    master_busy = False
    return


@api_view(['POST'])
def reset(request):
    print("reset")
    host = '192.168.0.109'
    port = 22

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username="vm1", password="wlodek", port=port)
    client.exec_command('./reset.sh')
    client.close()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def progress_bar(request):
    task_id = int(request.GET['task_id'])
    task_from_db = Request.objects.get(id=task_id)
    data = [float(task_from_db.progress1) * 100, float(task_from_db.progress2) * 100, float(task_from_db.progress3) * 100,
            task_from_db.image_url]
    return Response(data, status.HTTP_200_OK)


def task(request):
    user_id = request.GET['user_id']
    if request.GET['task_id'] is not '0':
        t = Request.objects.get(id=request.GET['task_id'])
        return render(request, 'blog/task.html', {'task': t, 'user_id': user_id})
    else:
        return render(request, 'blog/task.html', {'task': None, 'user_id': user_id})

