
/*
 * Measures memory latency from processor A to B
 */

#define _GNU_SOURCE
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sched.h>
#include <pthread.h>

#define PAGESIZE 0x1000


static inline uint64_t
rdtsc(void){
    uint32_t eax,edx;
    asm volatile ("rdtsc" : "=a" (eax), "=d" (edx));
    return ((uint64_t)edx << 32) | eax;
}

static size_t total_trials;

struct worker_args {
    volatile uint64_t *read_addr;
    volatile uint64_t *write_addr;
    uint64_t cpu;
};

static inline int
set_affinity(uint64_t cpu) {
    // Pin ourselves to the correct CPU
    cpu_set_t affinity_set;
    CPU_ZERO(&affinity_set);
    CPU_SET(cpu, &affinity_set);

    return sched_setaffinity(0, sizeof(affinity_set), &affinity_set);
}

static void *leader(void *_args)
{
    int res;
    struct worker_args *args = _args;

    res = set_affinity(args->cpu);
    if (res) {
        return (void*)(int64_t)res;
    }

    uint64_t minimum_latency = ~0ULL;

    size_t trial_no = 0;
    while(trial_no < total_trials) {
        uint64_t start = rdtsc();
        *args->write_addr = 1;
        while(*args->read_addr == 0) {}
        uint64_t end = rdtsc();

        uint64_t latency = end - start;
        if(latency < minimum_latency) {
            minimum_latency = latency;
        }

        trial_no++;

        *args->write_addr = 0;
        while(*args->read_addr != 0) {}
    }

    printf("%lu\n", minimum_latency);

    return (void*)(int64_t)0;
}

static void *follower(void *_args)
{
    int res;
    struct worker_args *args = _args;

    res = set_affinity(args->cpu);
    if (res) {
        return (void*)(int64_t)res;
    }

    while(1) {
        while(*args->read_addr == 0) {}
        *args->write_addr = 1;
        while(*args->read_addr != 0) {}
        *args->write_addr = 0;
    }
}

int
main(int argc, const char **argv)
{
    int res;
    // Get the pair of CPU's we are testing from the args
    if(argc != 4) {
        fprintf(stderr, "Usage: %s [WRITER-CPU] [READER-CPU] [TRIALS]\n", argv[0]);
        exit(-1);
    }
    uint64_t cpu_A, cpu_B;
    cpu_A = atol(argv[1]);
    cpu_B = atol(argv[2]);

    total_trials = atol(argv[3]);

    // Create two shared memory regions
    void *page_A = mmap(NULL,
            PAGESIZE,
            PROT_READ|PROT_WRITE,
            MAP_SHARED|MAP_ANONYMOUS,
            0,
            0);
    if(page_A == MAP_FAILED) {
        exit(-1);
    }
    memset(page_A, 0, PAGESIZE);

    void *page_B = mmap(NULL,
            PAGESIZE,
            PROT_READ|PROT_WRITE,
            MAP_SHARED|MAP_ANONYMOUS,
            0,
            0);
    if(page_A == MAP_FAILED) {
        exit(-1);
    }
    memset(page_B, 0, PAGESIZE);

    pthread_t leader_thread, follower_thread;

    struct worker_args leader_args = {
        .cpu = cpu_A,
        .read_addr = page_A,
        .write_addr = page_B,
    };
    struct worker_args follower_args = {
        .cpu = cpu_B,
        .read_addr = page_B,
        .write_addr = page_A,
    };

    res = pthread_create(&leader_thread, NULL, leader, &leader_args);
    if (res != 0) {
        exit(-1);
    }
    res = pthread_create(&follower_thread, NULL, follower, &follower_args);
    if (res != 0) {
        exit(-1);
    }

    res = pthread_join(leader_thread, NULL);
    if(res != 0) {
        exit(-1);
    }

    // Lock our memory
    // (Swapping seems unlikely but let's just rule it out)
    // This does make our chance of ENOMEM errors rise significantly
    mlockall(MCL_CURRENT|MCL_FUTURE);

    // Technically we should do cleanup but we're exiting anyways
    exit(0);
}

