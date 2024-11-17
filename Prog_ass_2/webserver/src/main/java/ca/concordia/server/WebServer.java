package ca.concordia.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URLDecoder;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.locks.ReentrantLock;
import java.util.List;
import java.util.ArrayList;

//create the WebServer class to receive connections on port 5000. Each connection is handled by a master thread that puts the descriptor in a bounded buffer. A pool of worker threads take jobs from this buffer if there are any to handle the connection.
public class WebServer {

    // Create a HashMap to store the accounts
    private static Map<Integer, Account> accounts = new HashMap<>();

    // Create a HashMap to store the locks
    private static Map<Integer, ReentrantLock> locks = new HashMap<>();
    
    // Create a list to store the successful transactions
    private static List<String> successfulTransactions = new ArrayList<>();
    
    // Counter for transaction numbers
    private static int transactionCounter = 0;

    // Method to initialize the accounts
    private static void initializeAccounts() {
        accounts.put(123, new Account(4000, 123));
        accounts.put(321, new Account(5000, 321));
        accounts.put(432, new Account(2000, 432));
        accounts.put(345, new Account(4000, 345));
    }

    // Method to start the server
    public void start() throws java.io.IOException {
        // Initialize the accounts
        initializeAccounts();

        //Create a server socket and an executor service to handle client requests
        try(ServerSocket serverSocket = new ServerSocket(8000)) {
            ExecutorService threadPool = Executors.newCachedThreadPool();
            while (true) {
                System.out.println("Waiting for a client to connect...");
                //Accept a connection from a client
                final Socket clientSocket = serverSocket.accept();
                System.out.println("New client...");
                // Submit the client request to the executor service
                threadPool.submit(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            // Handle the client request
                            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                            OutputStream out = clientSocket.getOutputStream();

                            String request = in.readLine();
                            if (request != null) {
                                if (request.startsWith("GET")) {
                                    // Handle GET request
                                    handleGetRequest(out);
                                } else if (request.startsWith("POST")) {
                                    // Handle POST request
                                    handlePostRequest(in, out);
                                }
                            }

                            // Close the streams and the socket
                            in.close();
                            out.close();
                            clientSocket.close();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                });
            }
        }
    }

   // Method to handle the GET request
    private static void handleGetRequest(OutputStream out) throws IOException {
        // Respond with a basic HTML page
        System.out.println("Handling GET request");
        String response = "HTTP/1.1 200 OK\r\n\r\n" +
                "<!DOCTYPE html>\n" +
                "<html>\n" +
                "<head>\n" +
                "<title>Concordia Transfers</title>\n" +
                "</head>\n" +
                "<body>\n" +
                "\n" +
                "<h1>Welcome to Concordia Transfers</h1>\n" +
                "<h2>Select the account and amount to transfer</h2>\n" +
                "\n" +
                "<form action=\"/submit\" method=\"post\">\n" +
                "        <label for=\"account\">Account:</label>\n" +
                "        <input type=\"text\" id=\"account\" name=\"account\"><br><br>\n" +
                "\n" +
                "        <label for=\"value\">Value:</label>\n" +
                "        <input type=\"text\" id=\"value\" name=\"value\"><br><br>\n" +
                "\n" +
                "        <label for=\"toAccount\">To Account:</label>\n" +
                "        <input type=\"text\" id=\"toAccount\" name=\"toAccount\"><br><br>\n" +
                "\n" +
                "        <input type=\"submit\" value=\"Submit\">\n" +
                "    </form>\n" +
                "<h2>Current Account Balance: </h2>\n" +
                "<table>\n" +
                "<tr><th>Account ID</th><th>Account Balance</th></tr>\n" +
                displayAccounts() +
                "</table>\n" +
                "<h2>Successful Transactions: </h2>\n" +
                "<table>\n" +
                "<tr><th>Transaction No.</th><th>From Account</th><th>To Account</th><th>Value</th></tr>\n" +
                displayTransactions() +
                "</table>\n" +
                "</body>\n" +
                "</html>\n";
        out.write(response.getBytes());
        out.flush();
    }

    // Method to handle the POST request
    private static void handlePostRequest(BufferedReader in, OutputStream out) throws IOException {
        System.out.println("Handling post request");
        StringBuilder requestBody = new StringBuilder();
        int contentLength = 0;
        String line;

        // Read headers to get content length
        while ((line = in.readLine()) != null && !line.isEmpty()) {
            if (line.startsWith("Content-Length")) {
                contentLength = Integer.parseInt(line.substring(line.indexOf(' ') + 1));
            }
        }

        // Read the request body based on content length
        for (int i = 0; i < contentLength; i++) {
            requestBody.append((char) in.read());
        }

        System.out.println(requestBody.toString());
        // Parse the request body as URL-encoded parameters
        String[] params = requestBody.toString().split("&");
        Integer account = null, value = null, toAccount = null;

        // Decode the parameters
        for (String param : params) {
            String[] parts = param.split("=");
            if (parts.length == 2) {
                String key = URLDecoder.decode(parts[0], "UTF-8");
                String val = URLDecoder.decode(parts[1], "UTF-8");

                switch (key) {
                    case "account":
                        account = Integer.parseInt(val);
                        break;
                    case "value":
                        value = Integer.parseInt(val);
                        break;
                    case "toAccount":
                        toAccount = Integer.parseInt(val);
                        break;
                }
            }
        }

        // Process the transfer
        boolean success = processTransfer(account, toAccount, value);

        // Create the response
        String responseContent = "<html><body><h1>Thank you for using Concordia Transfers</h1>";
        if (success) {
            responseContent += "<h2>Transfer Successful!</h2>"+
                "<p>Account: " + account + "</p>" +
                "<p>Value: " + value + "</p>" +
                "<p>To Account: " + toAccount + "</p>";
        } else {
            responseContent += "<h2>Transfer Failed!</h2>"+
                "<p>Account: " + account + "</p>" +
                "<p>Value: " + value + "</p>" +
                "<p>To Account: " + toAccount + "</p>";
        }
        responseContent += "<h2>Current Account Balance: </h2>\n" +
            "<table>\n" +
            "<tr><th>Account ID</th><th>Account Balance</th></tr>\n" +
            displayAccounts() +
            "</table>\n" +
            "<h2>Successful Transactions: </h2>\n" +
            "<table>\n" +
            "<tr><th>Transaction No.</th><th>From Account</th><th>To Account</th><th>Value</th></tr>\n" +
            displayTransactions() +
            "</table>\n"+"</body></html>";

        // Respond with the received form inputs
        String response = "HTTP/1.1 200 OK\r\n" +
                "Content-Length: " + responseContent.length() + "\r\n" +
                "Content-Type: text/html\r\n\r\n" +
                responseContent;

        out.write(response.getBytes());
        out.flush();
    }

    // Method to process the transfer
    private static boolean processTransfer(int fromAccount, int toAccount, int value) {
        // Critical Section: Accessing and modifying account balances
        // Potential Deadlock: Accessing two accounts simultaneously
        
        // Prevent Deadlock and race condition by locking the accounts in a specific order
        int firstLock, secondLock;
        if (fromAccount < toAccount) {
            firstLock = fromAccount;
            secondLock = toAccount;
        } else {
            firstLock = toAccount;
            secondLock = fromAccount;
        }

        ReentrantLock firsLockObj = getLock(firstLock);
        ReentrantLock secondLockObj = getLock(secondLock);

        firsLockObj.lock(); // Lock the first account
        try {
            secondLockObj.lock(); // Lock the second account
            try {
                Account source = accounts.get(fromAccount);
                Account destination = accounts.get(toAccount);
    
                if (source != null && destination != null && source.getBalance() >= value) {
                    source.withdraw(value);
                    destination.deposit(value);
                    recordTransaction(fromAccount, toAccount, value);
                    return true;
                }
                return false;
            } finally {
                secondLockObj.unlock(); // Unlock the second account
            }
            
        } finally {
            firsLockObj.unlock(); // Unlock the first account
        }
    }

    // Method to get the lock for a specific account
    private static ReentrantLock getLock(int account) {
        ReentrantLock lock = locks.get(account);
        if (lock == null) {
            lock = new ReentrantLock();
            locks.put(account, lock);
        }
        return lock;
    }

    // Method to record a successful transaction
    private static void recordTransaction(int fromAccount, int toAccount, int value) {
        transactionCounter++;
        successfulTransactions.add("<tr><td>" + transactionCounter + "</td><td>" + fromAccount + "</td><td>" + toAccount + "</td><td>" + value + "</td></tr>");
    }

    // Method to display the accounts for debugging
    private static String displayAccounts(){
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<Integer, Account> entry : accounts.entrySet()) {
            sb.append("<tr><td>").append(entry.getKey()).append("</td><td>").append(entry.getValue().getBalance()).append("</td></tr>");
        }
        return sb.toString();
    }

    // Method to display the transactions for debugging
    private static String displayTransactions() {
        StringBuilder sb = new StringBuilder();
        for (String transaction : successfulTransactions) {
            sb.append(transaction);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        //Start the server, if an exception occurs, print the stack trace
        WebServer server = new WebServer();
        try {
            server.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

