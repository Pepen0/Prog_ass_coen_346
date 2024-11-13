# Prog_ass_coen_346

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Testing](#testing)
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

#### Test Cases

* **GET /accounts**: Verify that the server returns a list of accounts.
* **GET /accounts/{account_id}**: Verify that the server returns the details of a specific account.
* **POST /transfer**: Verify that the server can handle a transfer request and update the account balances accordingly.

### Example Commands

* `curl http://localhost:8000`
* `curl http://localhost:8000/accounts`
* `curl http://localhost:8000/accounts/{account_id}`
* `curl -X POST -H "Content-Type: application/json" -d '{"fromAccount": "{account_id}", "toAccount": "{account_id}", "amount": {amount}}' http://localhost:8000/transfer`

## Contributing

* Submit pull requests with clear descriptions of changes.
* Report issues and bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.