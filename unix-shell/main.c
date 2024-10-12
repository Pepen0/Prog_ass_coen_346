#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h> //for INT_MAX
#include "parser.h"
#include "utils.h"
#include "jobs.h"
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>

void terminate(char *line) {
    if (line)
        free(line); //release memory allocated to line pointer
    printf("bye\n");
    exit(0);
}

/* Read a line from standard input and put it in a char[] */
char* readline(const char *prompt)
{
    size_t buf_len = 16;
    char *buf = xmalloc(buf_len * sizeof(char));

    printf("%s", prompt);
    if (fgets(buf, buf_len, stdin) == NULL) {
        free(buf);
        return NULL;
    }

    do {
        size_t l = strlen(buf);
        if ((l > 0) && (buf[l-1] == '\n')) {
            l--;
            buf[l] = 0;
            return buf;
        }
        if (buf_len >= (INT_MAX / 2)) memory_error();
        buf_len *= 2;
        buf = xrealloc(buf, buf_len * sizeof(char));
        if (fgets(buf + l, buf_len - l, stdin) == NULL) return buf;
    } while (1);
}

/* Function prototypes */
void execute_single_command(struct cmdline *l);
void execute_piped_commands(struct cmdline *l);

int main(void) {
    while (1) {
        struct cmdline *l;
        char *line=0;
        int i, j;
        char *prompt = "myshell>";

        /* Readline use some internal memory structure that
           can not be cleaned at the end of the program. Thus
           one memory leak per command seems unavoidable yet */
        line = readline(prompt); // line is a pointer to char (string)
        if (line == 0 || ! strncmp(line,"exit", 4)) {
            terminate(line);
        }
        else if (strcmp(line, "jobs") == 0){
            /* handles the built "jobs" command */
            print_jobs();
            free(line);
            continue;
        } 
        else {
            /* parsecmd, free line, and set it up to 0 */
            l = parsecmd( & line);

            /* If input stream closed, normal termination */
            if (l == 0) {

                terminate(0);
            } 
            else if (l->err != 0) {
                /* Syntax error, read another command */
                printf("error: %s\n", l->err);
                continue;
            } 
            else {
                /* there is a command to execute, let's print the sequence */
                if(l->in !=0) printf("in: %s\n", l->in);
                if(l->out != 0) printf("out: %s\n", l->out);
                printf("bg: %d\n", l->bg);

                /* Display each command of the pipe */
                for (i=0; l->seq[i]!=0; i++) {
                    char **cmd = l->seq[i];
                    printf("seq[%d]: ", i);
                    for (j=0; cmd[j]!=0; j++) {
                        printf("'%s' ", cmd[j]);
                    }
                    printf("\n");
                }

                /* Execute the command(s) */
                if (l->seq[1] == NULL) {
                    /* Only one command, no pipes */
                    execute_single_command(l);
                } else {
                    /* Multiple commands (pipes) */
                    execute_piped_commands(l);
                }

            }
        }

        /* Update the status of background jobs */
        update_jobs();
    }

    /* Free any remaining jobs on exit */
    free_jobs();
    return 0;
}

void execute_single_command(struct cmdline *l) {
    pid_t pid;
    int status;
    char **cmd = l->seq[0];

    /* reconstruct the command line for storage */
    char *cmdline = strdup(cmd[0]);
    for(int i = 1; cmd[i]!=NULL; i++){
        cmdline = realloc(cmdline,strlen(cmdline) + strlen(cmd[i]) + 2);
        strcat(cmdline, " ");
        strcat(cmdline,cmd[i]);
    }

    pid = fork();
    if (pid == -1) {
        perror("fork");
        exit(1);
    } else if (pid == 0) {
        /* Child process */

        /* Handle input redirection */
        if (l->in != NULL) {
            int fd_in = open(l->in, O_RDONLY);
            if (fd_in < 0) {
                perror(l->in);
                exit(1);
            }
            dup2(fd_in, STDIN_FILENO);
            close(fd_in);
        }

        /* Handle output redirection */
        if (l->out != NULL) {
            int fd_out = open(l->out, O_WRONLY | O_CREAT | O_TRUNC, 0666);
            if (fd_out < 0) {
                perror(l->out);
                exit(1);
            }
            dup2(fd_out, STDOUT_FILENO);
            close(fd_out);
        }

        /* Execute the command */
        execvp(cmd[0], cmd);
        /* If execvp returns, an error occurred */
        perror(cmd[0]);
        exit(1);
    } else {
        /* Parent process */
        if (!l->bg) {
            /* Wait for the child process to finish */
            waitpid(pid, &status, 0);
            free(cmdline);
        } else {
            /* Background process, do not wait */
            printf("Process running in background with PID %d\n", pid);
            add_job(pid, cmdline);
        }
    }
}

void execute_piped_commands(struct cmdline *l) {
    int i, j;
    int num_cmds = 0;

    /* Count the number of commands */
    while (l->seq[num_cmds] != NULL) {
        num_cmds++;
    }

    /* Create the necessary number of pipes */
    int pipefds[2 * (num_cmds - 1)];
    for (i = 0; i < (num_cmds - 1); i++) {
        if (pipe(pipefds + i * 2) < 0) {
            perror("pipe");
            exit(1);
        }
    }

    pid_t pids[num_cmds];

    for (i = 0; i < num_cmds; i++) {
        pid_t pid = fork();
        if (pid == -1) {
            perror("fork");
            exit(1);
        } else if (pid == 0) {
            /* Child process */

            /* Redirect input if not first command */
            if (i > 0) {
                if (dup2(pipefds[(i - 1) * 2], STDIN_FILENO) < 0) {
                    perror("dup2");
                    exit(1);
                }
            } else if (l->in != NULL) {
                /* Handle input redirection for the first command */
                int fd_in = open(l->in, O_RDONLY);
                if (fd_in < 0) {
                    perror(l->in);
                    exit(1);
                }
                if (dup2(fd_in, STDIN_FILENO) < 0) {
                    perror("dup2");
                    exit(1);
                }
                close(fd_in);
            }

            /* Redirect output if not last command */
            if (i < num_cmds - 1) {
                if (dup2(pipefds[i * 2 + 1], STDOUT_FILENO) < 0) {
                    perror("dup2");
                    exit(1);
                }
            } else if (l->out != NULL) {
                /* Handle output redirection for the last command */
                int fd_out = open(l->out, O_WRONLY | O_CREAT | O_TRUNC, 0666);
                if (fd_out < 0) {
                    perror(l->out);
                    exit(1);
                }
                if (dup2(fd_out, STDOUT_FILENO) < 0) {
                    perror("dup2");
                    exit(1);
                }
                close(fd_out);
            }

            /* Close all pipe file descriptors */
            for (j = 0; j < 2 * (num_cmds - 1); j++) {
                close(pipefds[j]);
            }

            /* Execute the command */
            execvp(l->seq[i][0], l->seq[i]);
            perror(l->seq[i][0]);
            exit(1);
        }else{
            /* Parent process */
            pids[i] = pid;
        }
    }

    /* Parent process closes all pipe file descriptors */
    for (i = 0; i < 2 * (num_cmds - 1); i++) {
        close(pipefds[i]);
    }

    /* Reconstruct the command line for storage */
    char *cmdline = strdup(l->seq[0][0]);
    for ( i = 0; i < num_cmds; i++)
    {
        cmdline = realloc(cmdline, strlen(cmdline) + strlen(l->seq[i][0]) + 4);
        strcat(cmdline," | ");
        strcat(cmdline, l->seq[i][0]);
    }
    
    /* Background execution */
    if (!l->bg) {
        /* Wait for all child processes */
        for (i = 0; i < num_cmds; i++) {
            waitpid(pids[i],NULL,0);
        }
        free(cmdline);
    } else {
        printf("Piped commands running in background\n");
        add_job(pids[num_cmds - 1], cmdline);
    }
}