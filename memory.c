#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <time.h>
#include <math.h>
#include <float.h>
#include <assert.h>

#include <pthread.h>
#include <inttypes.h>

#ifndef N
#define N 2000000
#endif
#ifndef NTIMES
#define NTIMES 100
#endif
#ifndef OFFSET
#define OFFSET 0
#endif

#define USEC 1000000

static double bwData[N+OFFSET];

unsigned int bwStreamSize = N; // 2*N


void *memory_intensive_function(void *args){
    uint64_t duration = (uint64_t) args;
	double scalar = 3.0;
	double time_spent = 0.0;


	while (time_spent < duration) {
		double *mid = bwData + (bwStreamSize/2);
		clock_t begin = clock();

		for (int i = 0; i < bwStreamSize/2; i++) {
			bwData[i] = scalar*mid[i];
		}

		for (int i = 0; i < bwStreamSize/2; i++) {
			mid[i] = scalar*bwData[i];
		}

		clock_t end = clock(); 
		time_spent += (double)(end - begin) / CLOCKS_PER_SEC;

		// intensity adjuster
		usleep(USEC);
	}
}

int main (int argc, char **argv) { 
	// Usage: ./memory <duration in sec> <num_threads> 
	if (argc < 3) { 
		printf("Usage: ./memory <duration in sec> <num_threads>\n"); 
		exit(0);
	}

	uint64_t duration = atoi(argv[1]);
	uint32_t num_threads = atoi(argv[2]);

	pthread_t* threads = (pthread_t*) calloc(num_threads, sizeof(pthread_t));

	for (int i = 0; i < num_threads; i++) { 
		int ret = pthread_create(&threads[i], NULL, memory_intensive_function, (void *) duration);
        assert(ret == 0);
	}


    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }


	return 0;
}
