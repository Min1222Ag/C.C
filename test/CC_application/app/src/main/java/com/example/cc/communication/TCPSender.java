package com.example.cc.communication;

import android.util.Log;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class TCPSender implements Sender{
    Socket s; // socket
    PrintWriter writer; // writer to write data at payload

    @Override
    public void send(String host, String data) {
        try {
            s = new Socket(host,6000); // socket open
            writer = new PrintWriter(s.getOutputStream()); // writer to write data at payload

            Log.i("RPi", "Connected! with "+s.toString());

            writer.write(data); // send a set of GPS coordinates
            Log.i("RPi", "sent data: "+data);
            writer.flush(); // initialize

            s.close(); // socket closed
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
