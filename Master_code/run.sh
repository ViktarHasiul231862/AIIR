#!/bin/bash
`./copy.sh`
if [ $# -ne 3 ]
then
	mpirun.openmpi -n 3 -machinefile .mpi_hostfile python3 madelbrot.py
else
	mpirun.openmpi -n 3 -machinefile .mpi_hostfile python3 madelbrot.py $1 $2 $3
fi
