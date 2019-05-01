from PIL import Image
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import paramiko
from .models import User

def home(request):
    return render(request, 'blog/login.html')

def about(request):
    return render(request, 'blog/about.html')

@api_view(['GET', 'POST'])
def registration(request):
    if request.method == "GET":
     return render(request, 'blog/registration.html')
    else:
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.get(email=email)
            return render(request, 'blog/registration.html', {'msg': "user with this email already exist"})
        except User.DoesNotExist:
            User.objects.create(name=name, surname=surname, email=email, password=password)
            return render(request, 'blog/login.html', {'msg': "user created successfully"})

@api_view(['POST'])
def setParams (request):

    global progress1
    global progress2
    global progress3

    host = '192.168.0.105'
    port = 22

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username="vm1", password="wlodek", port=port)
    stdin, stdout, stderr = client.exec_command('./run.sh ' + request.data['firstParam']
                                                + ' ' + request.data['secondParam'] + ' ' + request.data['thirdParam'])
    stdin.close()
    for line in iter(lambda: stdout.readline(2048), ""):
        info, progress = line.split(": ", 1)
        if info == "Master":
            progress1 = progress
        elif info == "Slave1":
            progress2 = progress
        elif info == "Slave2":
            progress3 = progress

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
    bg.save("./blog/static/images/fractal_square.jpg", quality=95)
    return render(request, 'blog/login.html')

@api_view(['POST'])
def reset(request):
    print("reset")
    host = '192.168.0.105'
    port = 22

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username="vm1", password="wlodek", port=port)
    stdin, stdout, stderr = client.exec_command('./reset.sh')
    data = stdout.read() + stderr.read()
    print(data)
    client.close()
    return Response(status=status.HTTP_200_OK)


progress1 = 0
progress2 = 0
progress3 = 0

@api_view(['POST'])
def login(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        user = User.objects.get(email=email)
        if user.password == password:
            print("valid user")
            # redirect to task manager
    except User.DoesNotExist:
        print("user does not exist")
    return render(request, 'blog/login.html', {'msg': "email or password are invalid"})



@api_view(['GET'])
def progress_bar(request):
    global progress1
    global progress2
    global progress3
    data = [progress1 * 100, progress2 * 100, progress3 * 100]
    return Response(data, status.HTTP_200_OK)

