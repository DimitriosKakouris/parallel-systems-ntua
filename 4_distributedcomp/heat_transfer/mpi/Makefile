CC=mpicc
CFLAGS=-O3 -lm -Wall
RES=-DPRINT_RESULTS
CONV=-DTEST_CONV

all: jacobi jacobi_conv gs gs_conv rb rb_conv

jacobi: mpi_jacobi.c utils.c
	
	$(CC) $(CFLAGS) mpi_jacobi.c utils.c -o jacobi

jacobi_conv: mpi_jacobi.c utils.c
	
	$(CC) $(CFLAGS) $(CONV) mpi_jacobi.c utils.c -o jacobi_conv

gs: mpi_gs.c utils.c
	
	$(CC) $(CFLAGS) mpi_gs.c utils.c -o gs

gs_conv: mpi_gs.c utils.c
	
	$(CC) $(CFLAGS) $(CONV) mpi_gs.c utils.c -o gs_conv

rb: mpi_rb.c utils.c
	
	$(CC) $(CFLAGS) mpi_rb.c utils.c -o rb

rb_conv: mpi_rb.c utils.c
	
	$(CC) $(CFLAGS) $(CONV) mpi_rb.c utils.c -o rb_conv

clean:
	rm jacobi jacobi_conv gs gs_conv rb rb_conv