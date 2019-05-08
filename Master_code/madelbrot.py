import sys
import os
import array as array
import numpy
from mpi4py import MPI

#variable for computing values in function
_x_and_y = numpy.zeros(4)

#old arguments from file old.txt
old_arguments = numpy.zeros(4)

if len(sys.argv) == 4:
    w = h = int(sys.argv[1])
    maxit = int(sys.argv[2]) 
    argv_3 = int (sys.argv[3])
    arguments = []
    file = open("old.txt", 'r')
    numbers = file.readlines()
    file.close()
    for i in range(len(numbers)):
        arguments.append(float(numbers[i]))
    
    old_arguments[0] = arguments[0]
    old_arguments[1] = arguments[1]
    old_arguments[2] =  arguments[2]
    old_arguments[3] =  arguments[3]
else:
    w = h = 0
    maxit = 0
    argv_3 = 0

def mandelbrot(x,y,maxit):
    c=x+y*1j
    z=0+0j
    it=0
    while abs(z) < 2.75 and it < maxit:
        z = z**2+c
        it+=1
    return it


if argv_3 == 1:
    _x_and_y[0] = (old_arguments[0]+old_arguments[1])/2
    _x_and_y[1] = old_arguments[1]
    _x_and_y[2] = old_arguments[2]
    _x_and_y[3] = (old_arguments[2]+old_arguments[3])/2
elif argv_3 == 2:
    _x_and_y[0] = old_arguments[0]
    _x_and_y[1] = (old_arguments[0]+old_arguments[1])/2
    _x_and_y[2] = old_arguments[2]
    _x_and_y[3] = (old_arguments[2]+old_arguments[3])/2
elif argv_3 == 3:
    _x_and_y[0] = old_arguments[0]
    _x_and_y[1] = (old_arguments[0]+old_arguments[1])/2
    _x_and_y[2] = (old_arguments[2]+old_arguments[3])/2
    _x_and_y[3] = old_arguments[3]
elif argv_3 == 4:
    _x_and_y[0] = (old_arguments[0]+old_arguments[1])/2
    _x_and_y[1] = old_arguments[1]
    _x_and_y[2] = (old_arguments[2]+old_arguments[3])/2
    _x_and_y[3] = old_arguments[3]
else:
    _x_and_y[0], _x_and_y[1] = -1.0, 1.0
    _x_and_y[2], _x_and_y[3] = -1.0, 1.0
    w = h = 400
    maxit = 100

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
#number of rows to copute here
N = h // size + (h%size>rank)
#first row to compute here
start = comm.scan(N)-N

#array to store the result
Cl = numpy.zeros ([N, w], dtype='i')

dx = (_x_and_y[1]-_x_and_y[0])/w
dy = (_x_and_y[3]-_x_and_y[2])/h
counter = 0
for i in range (N):
    y = _x_and_y[2] + (i+start) * dy
    for j in range (w):
        x = _x_and_y[0] + j*dx
        Cl[i,j] = mandelbrot(x,y,maxit)
        counter+=1
    #slave info
    if rank != 0:
        print("Slave"+str(rank)+":: "+str(round(counter/(N*w), 2)))
    else:
        print("Master::", str(round(counter/(N*w), 2)))

counts = comm.gather (N, root=0)
C = None
if rank == 0:
    C = numpy.zeros([h,w], dtype='i')

rowtype = MPI.INT.Create_contiguous(w)
rowtype.Commit()

comm.Gatherv(sendbuf = [Cl, MPI.INT],
        recvbuf=[C, (counts, None), rowtype],
        root=0)

rowtype.Free()

if comm.rank == 0 :
    import matplotlib.image as mtp
    mtp.imsave('out.png',C)

if len(sys.argv) == 4:
    arguments[0] = _x_and_y[0]
    arguments[1] = _x_and_y[1]
    arguments[2] = _x_and_y[2]
    arguments[3] = _x_and_y[3]
    with open('old.txt', 'w') as f:
        for k in range(len(arguments)):
            f.write(str(arguments[k])+'\n')
