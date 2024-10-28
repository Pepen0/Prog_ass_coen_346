#include "jobs.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>

static struct job *job_list = NULL;

/* Function impletation */
void add_job(pid_t pid, char *cmdline){
    struct job *new_job = malloc(sizeof(struct job));
    
    if(!new_job){
        perror("malloc");
        exit(1);
    } else {
        new_job->pid = pid;
        new_job->cmdline = strdup(cmdline);
        new_job->status = 0; /* Running */
        new_job->next = job_list;
        job_list = new_job;
    }

}

void update_jobs(){
    struct job *current = job_list;
    struct job *prev = NULL;
    int status;
    pid_t result;

    while(current != NULL){
        /* Check if the process has finished */
        result = waitpid(current->pid, &status, WNOHANG);
        if (result == -1){
            perror("waitpid");
            current->status = 1;
        } else if (result > 0){
            current->status = 1;
        }

        /* Move to next job */
        prev = current;
        current = current->next;
    }
    
}
void print_jobs(){
    update_jobs();
    struct job *current = job_list;

    while (current != NULL){
        if(current->status == 0){
            printf("[%d]    Running     %s\n",current->pid, current->cmdline);
        } else {
            printf("[%d]    Finished    %s\n",current->pid, current->cmdline);
        }
        current = current->next;

    }
}
void remove_jobs(pid_t pid){
    struct job *current = job_list;
    struct job *prev = NULL;

    while(current != NULL){
        if(current->pid == pid){
            if(prev == NULL){
                job_list = current->next;
            } else {
                prev->next = current->next;
            }
            free(current->cmdline);
            free(current);
            return;
        }
        prev = current;
        current = current->next;
    }
}

void free_jobs(){
    struct job *current = job_list;
    struct job *next_job;

    while(current != NULL){
        next_job = current->next;
        free(current->cmdline);
        free(current);
        current = next_job;
    }
    job_list = NULL;
}