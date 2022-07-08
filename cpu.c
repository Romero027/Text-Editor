#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <omp.h>
#include <assert.h>
#include <sched.h>
#include <inttypes.h>
#include <sys/types.h>
#include <unistd.h>

#define NS_PER_S (1000000000L)

uint64_t getNs() {
	struct timespec ts;
	clock_gettime(CLOCK_REALTIME, &ts);
	return ts.tv_sec*NS_PER_S + ts.tv_nsec;
}

void *cpu_intensive_function(void *args){
    uint64_t endNs = (uint64_t) args;
    while (getNs() < endNs);
}

int main(int argc, const char** argv) {
	// Usage: ./cpu <duration in sec> <core1,core2,...>
	if (argc < 3) { 
		printf("Usage: ./cpu <duration in sec> <core1,core2,...>\n"); 
		exit(0);
	}

    uint32_t total_cores = omp_get_num_procs();
	printf("Total number of (logical) cores: %" PRIu32 "\n", total_cores);

    int num_cores = argc - 2;
    int* cores = (int*)malloc((argc - 2) * sizeof(int));
    for (int i = 0; i < num_cores; i++) {
		int core = atoi(argv[i+2]);
        if (core <= 1 && core >= total_cores) {
            perror("input cores invalid");
            exit(EXIT_FAILURE);
        }
        cores[i] = core;
	}
    printf("Running interference workload on cores: ");
    for(int i = 0; i < num_cores; i++) {
        printf("%d ", cores[i]);
    }
      
    printf("\n");

    // time management
	uint64_t nsTotal = NS_PER_S*atoi(argv[1]); // ns
	uint64_t endNs = nsTotal > 0 ? getNs() + nsTotal : 0;
    assert(endNs > 0);

    pthread_t* threads = (pthread_t*) calloc(num_cores, sizeof(pthread_t));

	for (int i = 0; i < num_cores; i++) {
		int core = cores[i];

        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(core - 1, &cpuset);

        pthread_attr_t attr;
        pthread_attr_init(&attr);
        pthread_attr_setaffinity_np(&attr, sizeof(cpu_set_t), &cpuset);

        int ret = pthread_create(&threads[i], &attr, cpu_intensive_function, (void *) endNs);
        pthread_attr_destroy(&attr);
        assert(ret == 0);
        
	}

    for (int i = 0; i < num_cores; i++) {
        pthread_join(threads[i], NULL);
    }

    free(threads);
	return 0;
}

// gcc cpu.c -fopenmp -lpthread