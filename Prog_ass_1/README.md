# Unix Shell

A simple Unix shell implementation in C.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Building and Running](#building-and-running)
- [Usage](#usage)
- [Notes](#notes)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This is a basic implementation of a Unix shell in C. It includes a command parser, job management system, and supports basic shell grammar.

## Features

- Reads and executes commands from standard input
- Supports basic shell grammar (e.g., piping, redirection)
- Includes a job management system

## Building and Running

1. Clone the repository and navigate to the unix-shell directory.
2. Run `cmake .` to generate the build files.
3. Run `make` to compile the code.
4. Run `./cmake-build-debug/unix_shell` to start the shell.

## Usage

- Type commands at the prompt and press Enter to execute them.
- Use the `exit` command to quit the shell.

## Notes

- This is a basic implementation and may not support all Unix shell features.
- The code is still under development and may contain bugs.

## Directory Structure

- `unix-shell`: Top-level directory
- `cmake-build-debug`: Build directory
- `unix_shell`: Executable file
- `src`: Source code directory
  - `main.c`: Main entry point
  - `parser.c`: Command parsing logic
  - `jobs.c`: Job management logic
  - `utils.c`: Utility functions
- `include`: Header files
  - `parser.h`: Command parsing API
  - `jobs.h`: Job management API
  - `utils.h`: Utility function API

## Contributing

Contributions are welcome! Please submit pull requests with clear descriptions of changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
