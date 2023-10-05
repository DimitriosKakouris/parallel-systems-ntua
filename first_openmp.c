#include <stdio.h>
#include <omp.h>

int main() {
    // omp_set_num_threads(4);
    int sum=0;
    int array[5]={2,3,2,10,11};
    #pragma omp parallel for schedule(dynamic, 1)
    for (int i = 0; i < 5; i++) {
        int ID=omp_get_thread_num();
        #pragma omp critical
        {
             sum += array[i];
        }
        
        printf("ID = %d, sum = %d\n", ID, sum);
    }
    printf("sum = %d\n", sum);
    return 0;
}
