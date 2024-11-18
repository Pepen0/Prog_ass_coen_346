package ca.concordia.server;

import java.util.concurrent.atomic.AtomicInteger;

//class to represent a bank account
public class Account {
    //represent a bank account with a balance and withdraw and deposit methods
    private AtomicInteger balance;
    private int id;

    public Account(int balance, int id){

        this.balance = new AtomicInteger(balance); // Allow atomic opperations on the balance
        this.id = id;
    }

    // Method to get the balance
    public int getBalance(){
        return balance.get();
    }

    // Method to withdraw
    public void withdraw(int amount){
        //use compareAndSet to ensure that the balance is updated atomically
        int currentBalance = balance.get();
        balance.compareAndSet(currentBalance, currentBalance - amount);
    }

    // Method to deposit
    public void deposit(int amount){
        //use addAndGet to ensure that the balance is updated atomically
        balance.addAndGet(amount);
    }
}

