package com.example.cc;


import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.cc.communication.Sender;
import com.example.cc.communication.TCPSender;
import com.google.android.material.button.MaterialButton;

import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity {

    MaterialButton forwardButton, rightButton, leftButton, backButton, stopButton, pathButton;
    EditText etIp;

    SharedPreferences sharedPreferences;
    Editor editor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sharedPreferences = getSharedPreferences("IPAddress", MODE_PRIVATE);
        editor = sharedPreferences.edit();

        String existedIp = sharedPreferences.getString("ip", null);
        if (existedIp != null) {
            etIp.setText(existedIp);
        }

        forwardButton = findViewById(R.id.forward_button);
        forwardButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                makeOrder("forward");
            }
        });

        leftButton = findViewById(R.id.left_button);
        leftButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                makeOrder("left");
            }
        });

        rightButton = findViewById(R.id.right_button);
        rightButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                makeOrder("right");
            }
        });

        backButton = findViewById(R.id.back_button);
        backButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                makeOrder("back");
            }
        });

        stopButton = findViewById(R.id.stop_button);
        stopButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                makeOrder("stop");
            }
        });

        pathButton = findViewById(R.id.path_button);
        pathButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                etIp = findViewById(R.id.et_ip);
                String ip = etIp.getText().toString();

                // IP Address format check
                if(validAddress(etIp, ip)){
                    editor.putString("ip", ip);
                    editor.commit();
                    goGPS();
                }
            }
        });
    }
    public void goGPS(){
        Intent intent = new Intent(MainActivity.this, GpsActivity.class);
        startActivity(intent);
        finish();
    }

    public void makeOrder(String order){

        etIp = findViewById(R.id.et_ip);
        String ip = etIp.getText().toString();

        // IP Address format check
        if(validAddress(etIp, ip)){
            BackGroundTask sending = new BackGroundTask(ip, order);
            sending.execute();
            Log.i("order: ", order);
        }
    }

    public boolean validAddress(EditText etIp, String ip){
        if (!Pattern.matches("([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})", ip)){
            Toast.makeText(MainActivity.this, "Check the format of the IP Address", Toast.LENGTH_SHORT).show();
            etIp.setText("");
            return false;
        }
        else {
            return true;
        }
    }

    class BackGroundTask extends AsyncTask<String, Void, Void> {
        String host;
        String data;

        BackGroundTask(String host, String data){
            this.host = host;
            this.data = data;
        }

        @Override
        protected Void doInBackground(String... voids) {
            Sender sender = new TCPSender();
            sender.send(host, data);
            return null;
        }
    }
}