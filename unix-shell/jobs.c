#include "jobs.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>

static struct job *job_list = NULL;

/* Function impletation */
void add_job(pid_t pid, char *cmdline);
void update_jobs();
void print_jobs();
void remove_jobs(pid_t pid);
void free_jobs();