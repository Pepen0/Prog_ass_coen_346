cmake_minimum_required(VERSION 3.26)
project(unix_shell C)

set(CMAKE_C_STANDARD 11)

add_executable(unix_shell main.c
        parser.c
        parser.h
        utils.c
        utils.h
        jobs.h
        jobs.c
)
