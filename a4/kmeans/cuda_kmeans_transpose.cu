#include <stdio.h>
#include <stdlib.h>

#include "kmeans.h"
#include "alloc.h"
#include "error.h"

#ifdef __CUDACC__
inline void checkCuda(cudaError_t e) {
    if (e != cudaSuccess) {
        // cudaGetErrorString() isn't always very helpful. Look up the error
        // number in the cudaError enum in driver_types.h in the CUDA includes
        // directory for a better explanation.
        error("CUDA Error %d: %s\n", e, cudaGetErrorString(e));
    }
}

inline void checkLastCudaError() {
    checkCuda(cudaGetLastError());
}
#endif

__device__ int get_tid(){

	int globalID = threadIdx.x + blockDim.x * blockIdx.x;
	return globalID; /* TODO: copy me from naive version... */
}

/* square of Euclid distance between two multi-dimensional points using column-base format */
__host__ __device__ inline static
double euclid_dist_2_transpose(int numCoords,
                    int    numObjs,
                    int    numClusters,
                    double *objects,     // [numCoords][numObjs]
                    double *clusters,    // [numCoords][numClusters]
                    int    objectId,
                    int    clusterId)
{
    int i;
    double ans=0.0;

	/* TODO: Calculate the euclid_dist of elem=objectId of objects from elem=clusterId from clusters, but for column-base format!!! */
    for (i=0; i<numCoords; i++){
        ans += (objects[i*numObjs + objectId] - clusters[i*numClusters + clusterId]) * (objects[i*numObjs + objectId] - clusters[i*numClusters + clusterId]);
     }
    return(ans);
}

__global__ static
void find_nearest_cluster(int numCoords,
                          int numObjs,
                          int numClusters,
                          double *objects,           //  [numCoords][numObjs]
                          double *deviceClusters,    //  [numCoords][numClusters]
                          int *membership,          //  [numObjs]
                          double *devdelta)
{
	/* TODO: copy me from naive version... */
    /* Get the global ID of the thread. */
    int tid = get_tid(); 

	/* TODO: Maybe something is missing here... should all threads run this? */
    if (tid<numObjs) {
        int   index, i;
        double dist, min_dist;

        /* find the cluster id that has min distance to object */
        index = 0;
        /* TODO: call min_dist = euclid_dist_2(...) with correct objectId/clusterId */
        min_dist = euclid_dist_2_transpose(numCoords,numObjs,numClusters,objects,deviceClusters,tid,index);

        for (i=1; i<numClusters; i++) {
            /* TODO: call dist = euclid_dist_2(...) with correct objectId/clusterId */
            dist = euclid_dist_2_transpose(numCoords,numObjs,numClusters,objects,deviceClusters,tid, i);
 
            /* no need square root */
            if (dist < min_dist) { /* find the min and its array index */
                min_dist = dist;
                index = i;
            }
        }

        if (membership[tid] != index) {
        	/* TODO: Maybe something is missing here... is this write safe? */
            atomicAdd(devdelta,1.0);
            /*(*devdelta)+= 1.0;*/
        }

        /* assign the deviceMembership to object objectId */
        membership[tid] = index;
    }
}

//
//  ----------------------------------------
//  DATA LAYOUT
//
//  objects         [numObjs][numCoords]
//  clusters        [numClusters][numCoords]
//  dimObjects      [numCoords][numObjs]
//  dimClusters     [numCoords][numClusters]
//  newClusters     [numCoords][numClusters]
//  deviceObjects   [numCoords][numObjs]
//  deviceClusters  [numCoords][numClusters]
//  ----------------------------------------
//
/* return an array of cluster centers of size [numClusters][numCoords]       */            
void kmeans_gpu(double *objects,      /* in: [numObjs][numCoords] */
		        int     numCoords,    /* no. features */
		        int     numObjs,      /* no. objects */
		        int     numClusters,  /* no. clusters */
		        double   threshold,    /* % objects change membership */
		        long    loop_threshold,   /* maximum number of iterations */
		        int    *membership,   /* out: [numObjs] */
				double *clusters,   /* out: [numClusters][numCoords] */
				int blockSize)  
{
    double timing = wtime(), timing_internal, timer_min = 1e42, timer_max = 0; 
    // double tmp_timer;
    // double CG_timer=0, GC_timer=0, G_timer=0, C_timer=0;
	// int    loop_iterations = 0; 
    int      i, j, index, loop=0;
    int     *newClusterSize; /* [numClusters]: no. objects assigned in each
                                new cluster */
    double  delta = 0, *dev_delta_ptr;          /* % of objects change their clusters */
    
    /* TODO: Transpose dims */
    double  **dimObjects = (double **)calloc_2d(numCoords, numObjs, sizeof(double));//calloc_2d(...) -> [numCoords][numObjs]
    double  **dimClusters = (double **)calloc_2d(numCoords, numClusters, sizeof(double));  //calloc_2d(...) -> [numCoords][numClusters]
    double  **newClusters = (double **)calloc_2d(numCoords, numClusters, sizeof(double));  //calloc_2d(...) -> [numCoords][numClusters]
    
    double *deviceObjects;
    double *deviceClusters;
    int *deviceMembership;

    printf("\n|-----------Transpose GPU Kmeans------------|\n\n");
    
    //  TODO: Copy objects given in [numObjs][numCoords] layout to new
   
	
//     for (j = 0; j < numObjs; j++) {
//         for (i = 0; i < numCoords; i++) {
//         dimObjects[i][j] = objects[j * numCoords + i];
//     }
// }
  for (i = 0; i < numCoords; i++) {
        for (j = 0; j < numObjs; j++) {
            dimObjects[i][j] = objects[j*numCoords + i];
        }
    }
	
    /* pick first numClusters elements of objects[] as initial cluster centers*/
    for (i = 0; i < numCoords; i++) {
        for (j = 0; j < numClusters; j++) {
            dimClusters[i][j] = dimObjects[i][j];
        }
    }

    
	
    /* initialize membership[] */
    for (i=0; i<numObjs; i++) membership[i] = -1;

    /* need to initialize newClusterSize and newClusters[0] to all 0 */
    newClusterSize = (int*) calloc(numClusters, sizeof(int));
    assert(newClusterSize != NULL); 
    
    timing = wtime() - timing;
    printf("t_alloc: %lf ms\n\n", 1000*timing);
    timing = wtime(); 

    const unsigned int numThreadsPerClusterBlock = (numObjs > blockSize)? blockSize: numObjs;
    const unsigned int numClusterBlocks = (numObjs + numThreadsPerClusterBlock - 1) / numThreadsPerClusterBlock; /* TODO: Calculate Grid size, e.g. number of blocks. */
    const unsigned int clusterBlockSharedDataSize = 0;
       
    checkCuda(cudaMalloc(&deviceObjects, numObjs*numCoords*sizeof(double)));
    checkCuda(cudaMalloc(&deviceClusters, numClusters*numCoords*sizeof(double)));
    checkCuda(cudaMalloc(&deviceMembership, numObjs*sizeof(int)));
    checkCuda(cudaMalloc(&dev_delta_ptr, sizeof(double)));
    timing = wtime() - timing;
    printf("t_alloc_gpu: %lf ms\n\n", 1000*timing);
    timing = wtime(); 
    
    checkCuda(cudaMemcpy(deviceObjects, dimObjects[0],
              numObjs*numCoords*sizeof(double), cudaMemcpyHostToDevice));
    checkCuda(cudaMemcpy(deviceMembership, membership,
              numObjs*sizeof(int), cudaMemcpyHostToDevice));
    timing = wtime() - timing;
    printf("t_get_gpu: %lf ms\n\n", 1000*timing);
    timing = wtime();   


    #ifdef TIMING_ANALYSIS
    double gpu_time, gpu_cpu_time, cpu_time, cpu_gpu_time;
    double gpu_time_arr[10];
    double gpu_time_total = 0.0, gpu_cpu_time_total = 0.0, cpu_time_total = 0.0, cpu_gpu_time_total = 0.0;
    double gpu_time_min = __DBL_MAX__, gpu_cpu_time_min = __DBL_MAX__, cpu_time_min = __DBL_MAX__, cpu_gpu_time_min = __DBL_MAX__;
    double gpu_time_max = 0.0, gpu_cpu_time_max = 0.0, cpu_time_max = 0.0, cpu_gpu_time_max = 0.0;
    double time_start, time_end;
    #endif  
    
    do {
    	timing_internal = wtime();


        #ifdef TIMING_ANALYSIS
        time_start = wtime();
        #endif

		/* GPU part: calculate new memberships */
		        
        //tmp_timer=wtime();
        /* TODO: Copy clusters to deviceClusters */
        checkCuda(cudaMemcpy(deviceClusters,dimClusters[0],numClusters*numCoords*sizeof(double), cudaMemcpyHostToDevice));
        
        checkCuda(cudaMemset(dev_delta_ptr, 0, sizeof(double))); 

        #ifdef TIMING_ANALYSIS
        time_end = wtime();
        cpu_gpu_time = time_end - time_start;
        time_start = wtime();
        #endif   


        //CG_timer += wtime()-tmp_timer;
        //tmp_timer=wtime();
		//printf("Launching find_nearest_cluster Kernel with grid_size = %d, block_size = %d, shared_mem = %d KB\n", numClusterBlocks, numThreadsPerClusterBlock, clusterBlockSharedDataSize/1000);
        find_nearest_cluster<<< numClusterBlocks, numThreadsPerClusterBlock, clusterBlockSharedDataSize >>>(numCoords, numObjs, numClusters,deviceObjects, deviceClusters, deviceMembership, dev_delta_ptr);

        cudaDeviceSynchronize(); checkLastCudaError();

        #ifdef TIMING_ANALYSIS
        time_end = wtime();
        gpu_time = time_end - time_start;
        time_start = wtime();
        #endif

        //G_timer += wtime() - timing_internal;
		//printf("Kernels complete for itter %d, updating data in CPU\n", loop);
		
        //tmp_timer=wtime();
		/* TODO: Copy deviceMembership to membership*/
        checkCuda(cudaMemcpy(membership,deviceMembership,numObjs*sizeof(int), cudaMemcpyDeviceToHost));
    
    	/* TODO: Copy dev_delta_ptr to &delta*/
        checkCuda(cudaMemcpy(&delta,dev_delta_ptr, sizeof(double),cudaMemcpyDeviceToHost));
        //GC_timer += wtime()-tmp_timer;
        //tmp_timer=wtime();

        #ifdef TIMING_ANALYSIS
        time_end = wtime();
        gpu_cpu_time = time_end - time_start;
        time_start = wtime();
        #endif

		/* CPU part: Update cluster centers*/
  		
        for (i=0; i<numObjs; i++) {
            /* find the array index of nestest cluster center */
            index = membership[i];
			
            /* update new cluster centers : sum of objects located within */
            newClusterSize[index]++;
            for (j=0; j<numCoords; j++)
                newClusters[j][index] += objects[i*numCoords + j];
        }
 
        /* average the sum and replace old cluster centers with newClusters */
        for (i=0; i<numClusters; i++) {
            for (j=0; j<numCoords; j++) {
                if (newClusterSize[i] > 0)
                    dimClusters[j][i] = newClusters[j][i] / newClusterSize[i];
                newClusters[j][i] = 0.0;   /* set back to 0 */
            }
            newClusterSize[i] = 0;   /* set back to 0 */
        }

        //C_timer += wtime() - tmp_timer;

        

        delta /= numObjs;
       	//printf("delta is %f - ", delta);
        loop++; 




        #ifdef TIMING_ANALYSIS
        time_end = wtime();
        cpu_time = time_end - time_start;
        gpu_time_arr[loop] = gpu_time;

        gpu_time_total += gpu_time;
        gpu_cpu_time_total += gpu_cpu_time;
        cpu_time_total += cpu_time;
        cpu_gpu_time_total += cpu_gpu_time;
        if (gpu_time < gpu_time_min) gpu_time_min = gpu_time;
        if (gpu_time > gpu_time_max) gpu_time_max = gpu_time;
        if (gpu_cpu_time < gpu_cpu_time_min) gpu_cpu_time_min = gpu_cpu_time;
        if (gpu_cpu_time > gpu_cpu_time_max) gpu_cpu_time_max = gpu_cpu_time;
        if (cpu_time < cpu_time_min) cpu_time_min = cpu_time;
        if (cpu_time > cpu_time_max) cpu_time_max = cpu_time;
        if (cpu_gpu_time < cpu_gpu_time_min) cpu_gpu_time_min = cpu_gpu_time;
        if (cpu_gpu_time > cpu_gpu_time_max) cpu_gpu_time_max = cpu_gpu_time;
        #endif


        //printf("completed loop %d\n", loop);
		timing_internal = wtime() - timing_internal; 
		if ( timing_internal < timer_min) timer_min = timing_internal; 
		if ( timing_internal > timer_max) timer_max = timing_internal; 
	} while (delta > threshold && loop < loop_threshold);
    
    /*TODO: Update clusters using dimClusters. Be carefull of layout!!! clusters[numClusters][numCoords] vs dimClusters[numCoords][numClusters] */ 
// 	for (int i = 0; i < numClusters; i++) {
//     for (int j = 0; j < numCoords; j++) {
//         clusters[i*numCoords + j] = dimClusters[j][i];
//     }
// }
 for (i = 0; i < numCoords; i++) {
        for (j = 0; j < numClusters; j++) {
            clusters[j*numCoords + i] = dimClusters[i][j];
        }
    }
	
    timing = wtime() - timing;
    printf("nloops = %d  : total = %lf ms\n\t-> t_loop_avg = %lf ms\n\t-> t_loop_min = %lf ms\n\t-> t_loop_max = %lf ms\n\n|-------------------------------------------|\n", 
    	loop, 1000*timing, 1000*timing/loop, 1000*timer_min, 1000*timer_max);

    // printf("t_GPU->CPU = %lf ms\n", 1000*GC_timer); 
   	// printf("t_CPU->GPU = %lf ms\n", 1000*CG_timer); 
   	// printf("t_GPU = %lf ms\n", 1000*G_timer); 
   	// printf("t_CPU = %lf ms\n", 1000*C_timer); 

      // print timing information (avg, min, max) in each line
    #ifdef TIMING_ANALYSIS
    printf("GPU time: %lf ms\n\t-> t_loop_avg = %lf ms\n\t-> t_loop_min = %lf ms\n\t-> t_loop_max = %lf ms\n\n", 
    	1000*gpu_time_total, 1000*gpu_time_total/loop, 1000*gpu_time_min, 1000*gpu_time_max);
    printf("GPU-CPU time: %lf ms\n\t-> t_loop_avg = %lf ms\n\t-> t_loop_min = %lf ms\n\t-> t_loop_max = %lf ms\n\n",
        1000*gpu_cpu_time_total, 1000*gpu_cpu_time_total/loop, 1000*gpu_cpu_time_min, 1000*gpu_cpu_time_max);
    printf("CPU time: %lf ms\n\t-> t_loop_avg = %lf ms\n\t-> t_loop_min = %lf ms\n\t-> t_loop_max = %lf ms\n\n",
        1000*cpu_time_total, 1000*cpu_time_total/loop, 1000*cpu_time_min, 1000*cpu_time_max);
    printf("CPU-GPU time: %lf ms\n\t-> t_loop_avg = %lf ms\n\t-> t_loop_min = %lf ms\n\t-> t_loop_max = %lf ms\n\n",
        1000*cpu_gpu_time_total, 1000*cpu_gpu_time_total/loop, 1000*cpu_gpu_time_min, 1000*cpu_gpu_time_max);
    #endif


	char outfile_name[1024] = {0}; 
	sprintf(outfile_name, "Execution_logs/silver1-V100_Sz-%lu_Coo-%d_Cl-%d.csv", numObjs*numCoords*sizeof(double)/(1024*1024), numCoords, numClusters);
	FILE* fp = fopen(outfile_name, "a+");
	if(!fp) error("Filename %s did not open succesfully, no logging performed\n", outfile_name); 

    #ifndef TIMING_ANALYSIS
	fprintf(fp, "%s,%d,%lf,%lf,%lf,%lf\n", "Transpose", blockSize, timing/loop, timer_min, timer_max,timing);
    #endif
    
    #ifdef TIMING_ANALYSIS
    fprintf(fp, "%s,%d,%lf,%lf,%lf,%lf,%lf,%lf,%lf,%lf \n", "Transpose", blockSize, timing/loop, timer_min, timer_max,timing,1000*gpu_cpu_time_total, 1000*cpu_gpu_time_total, 1000*gpu_time_total,1000*cpu_time_total);
    #endif

	fclose(fp); 
	
    checkCuda(cudaFree(deviceObjects));
    checkCuda(cudaFree(deviceClusters));
    checkCuda(cudaFree(deviceMembership));

    free(dimObjects[0]);
    free(dimObjects);
    free(dimClusters[0]);
    free(dimClusters);
    free(newClusters[0]);
    free(newClusters);
    free(newClusterSize);

    return;
}

