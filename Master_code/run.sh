#!/bin/bash
`./copy.sh`
if [ $# -ne 3 ]
then
	mpirun.openmpi -n 4 -machinefile .mpi_hostfile python3 madelbrot.py $1 $2
else
	mpirun.openmpi -n 4 -machinefile .mpi_hostfile python3 madelbrot.py $1 $2 $3
fi
