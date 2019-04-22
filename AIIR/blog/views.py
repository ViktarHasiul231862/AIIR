from random import randint
import time
from threading import Thread
from PIL import Image
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import paramiko


def home(request):
    return render(request, 'blog/index.html')

def about(request):
    return render(request, 'blog/about.html')


@api_view(['POST'])
def setParams (request):

    print(request.data['firstParam'])  #rozdzielczosc
    print(request.data['secondParam']) #liczba iter
    print(request.data['thirdParam']) #czwiartka

    #Use data from clusters instead of "counter" variable
    #Put this into place, where this data can be recieved
    for counter in range(101):
        global progress1
        global progress2
        progress1 = counter
        progress2 = counter
        time.sleep(.1)

    host = '192.168.0.105'
    port = 22

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username="vm1", password="wlodek", port=port)
    stdin, stdout, stderr = client.exec_command('./run.sh ' + request.data['firstParam']
                                                + ' ' + request.data['secondParam'] + ' ' + request.data['thirdParam'])
    data = stdout.read() + stderr.read()
    print(data)
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
    return render(request, 'blog/index.html')

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

@api_view(['GET'])
def progress_bar(request):
    global progress1
    global progress2
    data = [float(progress1), float(progress2)]
    return Response(data, status.HTTP_200_OK)