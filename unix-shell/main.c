#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h> //for INT_MAX
#include "parser.h"
#include "utils.h"
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

void execute_single_command(struct cmdline *l) {
    pid_t pid;
    int status;
    char **cmd = l->seq[0];

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
        } else {
            /* Background process, do not wait */
            printf("Process running in background with PID %d\n", pid);
        }
    }
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
                execute_single_command(l);

            }
        }
    }
}