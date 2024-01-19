CC=mpicc
CFLAGS=-O3 -lm -Wall
RES=-DPRINT_RESULTS
CONV=-DTEST_CONV

all: jacobi jacobi_conv

jacobi: mpi_jacobi.c utils.c
	
	$(CC) $(CFLAGS) mpi_jacobi.c utils.c -o jacobi

jacobi_conv: mpi_jacobi.c utils.c
	
	$(CC) $(CFLAGS) $(CONV) mpi_jacobi.c utils.c -o jacobi_conv


clean:
	rm jacobi jacobi_conv