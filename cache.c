#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sched.h>

// returns the size of the L3 cache in bytes, otherwise -1 on error.
// if there're two NUMA nodes, then the return value is only for one
int cache_size() {
	// return the cache size from cpu 0
	// assuming that all cpu caches having the same size
	const char* cache_size_path = "/sys/devices/system/cpu/cpu0/cache/index3/size";

	FILE *cache_size_fd;
	if (!(cache_size_fd = fopen(cache_size_path, "r"))) {
		perror("could not open cache size file");
		return -1;
	}

	char line[512];
	if(!fgets(line, 512, cache_size_fd)) {
		fclose(cache_size_fd);
		perror("could not read from cache size file");
		return -1;
	}

	// strip newline
	const int newline_pos = strlen(line) - 1;
	if (line[newline_pos] == '\n') {
		line[newline_pos] = '\0';
	}

	// get multiplier
	int multiplier = 1;
	const int multiplier_pos = newline_pos - 1;
	switch (line[multiplier_pos]) {
		case 'K':
			multiplier = 1024;
		break;
		case 'M':
			multiplier = 1024 * 1024;
		break;
		case 'G':
			multiplier = 1024 * 1024 * 1024;
		break;
	}

	// remove multiplier
	if (multiplier != 1) {
		line[multiplier_pos] = '\0';
	}

	// line should now be clear of non-numeric characters
	int value = atoi(line);
	int cache_size = value * multiplier;

	fclose(cache_size_fd);
	return cache_size;
}

int main(int argc, char **argv) {
	char* volatile block_src;
	char* volatile block_dst;

	// Usage: ./l3_cache <duration in sec> <intensity>
    // e.g., ./l3_cache 10 1000000 50
	if (argc < 2) {
		printf("Usage: ./l3_cache <duration in sec> <interval in microsecond> <percentage of llc>\n");
		exit(0);
	}

	int CACHE_SIZE = cache_size();
	printf("Detected L3 cache size: %d bytes\n", CACHE_SIZE);

	// create a mapping to memory
	block_src = (char*)mmap(NULL, CACHE_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
	block_dst = (char*)mmap(NULL, CACHE_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
	if (block_src == (char *) -1 || block_dst == (char *) -1) {
		perror("error - cannot mmap");
		exit(1);
	};

	int usr_timer = atoi(argv[1]);
    int interval = atoi(argv[2]);
	int percentage = atoi(argv[3]);
	double time_spent = 0.0;
  	clock_t begin, end;

	int target_cache_size = (int) CACHE_SIZE*percentage/100;

	while (time_spent < usr_timer) {
  		begin = clock();
		memcpy(block_dst, block_src, target_cache_size);
        // yielding the cpu and give other threads a chance to run their workloads
		sched_yield();
		end = clock();
  		time_spent += (double)(end - begin) / CLOCKS_PER_SEC;
        // printf("time spent: %f\n", time_spent);

		// intensity adjuster
		usleep(interval);
	}
	return 0;
}
