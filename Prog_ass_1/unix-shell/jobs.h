#ifndef JOBS_H
#define JOBS_H

#include <sys/types.h>

struct job{
    pid_t pid;        /*    Process ID                             */
    char *cmdline;    /*    Command line                           */
    int status;       /*    0: running, 1: finished                */
    struct job *next; /*    Pointer to the next jobin the list     */
};

/* Function prototypes */
void add_job(pid_t pid, char *cmdline);
void update_jobs();
void print_jobs();
void remove_jobs(pid_t pid); /* TODO: Allow jobs removal from the list*/
void free_jobs();

#endif // JOBS_H