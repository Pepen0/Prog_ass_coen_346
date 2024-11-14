# Prog_ass_coen_346

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Testing](#testing)
* [Running the Simple Clients](#running-the-simple-clients)
* [Contributing](#contributing)
* [License](#license)

## Introduction

This project is a programming assignment for COEN 346. It aims to develop a concurrent web server to handle transfers between bank accounts.

## Features

* Web server
* Client-server architecture
* Account management
* Transfer functionality

## Requirements

* Java 11
* Maven

## Installation

1. Install Java 11 on your machine
2. Install Maven on your machine
3. Clone the repository
4. Navigate to the `Prog_ass_2/webserver` directory
5. Run `mvn clean package` to build the project

## Usage

1. Run `java -jar target/webserver-1.0-SNAPSHOT.jar` to start the server
2. Use a tool like `curl` or a web browser to interact with the server

## Testing

### Testing the Server

1. **Build the project**: Run `mvn clean package` to build the project.
2. **Run the server**: Run `java -jar target/webserver-1.0-SNAPSHOT.jar` to start the server.
3. **Use a tool to test the server**: Use a tool like `curl` or a web browser to test the server.

## Running the Simple Clients

To run the simple clients, navigate to the `Prog_ass_2/webserver` directory and run the following commands:

### SimpleWebClient

```bash
javac -d target src/main/java/ca/concordia/client/SimpleWebClient.java
java -cp target ca.concordia.client.SimpleWebClient
```

This will compile and run the simple client, which will establish a connection to the server at `localhost:8000`.

### SimpleWebClientDeadlock

```bash
javac -d target src/main/java/ca/concordia/client/SimpleWebClientDeadlock.java
java -cp target ca.concordia.client.SimpleWebClientDeadlock
```

This will compile and run the simple client deadlock, which will establish multiple connections to the server at `localhost:8000`.

## Contributing

Contributions are welcome! Please submit pull requests with clear descriptions of changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.