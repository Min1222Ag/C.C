package com.example.cc.communication;

/*
 interface of sender to send data to driving control unit
 */
public interface Sender {
    public void send(String host, String data); // send data to host ip address
}