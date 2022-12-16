package com.example.cc;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.example.cc.communication.Sender;
import com.example.cc.communication.TCPSender;
import com.example.cc.coordinates.CoordinateGenerator;
import com.example.cc.coordinates.ImpCoordinateGenerator;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputLayout;

import java.util.HashMap;
import java.util.regex.Pattern;

public class SelectActivity extends AppCompatActivity {
    //Initialize variable
    TextInputLayout tilDistance, tilIp;

    HashMap<String, String> locations;

    EditText etLen, etIp;
    MaterialButton button, button2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_select);

        CoordinateGenerator coordinateGenerator = new ImpCoordinateGenerator();

        //Assign variable
        tilDistance = findViewById(R.id.til_len);
        etLen = findViewById(R.id.et_len);

        tilIp = findViewById(R.id.til_ip);
        etIp = findViewById(R.id.et_ip);
        etLen = findViewById(R.id.et_len);

        Intent intent = getIntent();

        locations = (HashMap<String, String>)intent.getSerializableExtra("locations");

        String startCoordinate = locations.get("start_coordinate").substring(10, locations.get("start_coordinate").length()-1);
        String endCoordinate = locations.get("end_coordinate").substring(10, locations.get("end_coordinate").length()-1);
        String dumpsterCoordinate = locations.get("dumpster_coordinate").substring(10, locations.get("dumpster_coordinate").length()-1);

        TextView startLocation = (TextView)findViewById(R.id.til_startloc);

        startLocation.setText(startCoordinate);

        TextView endLocation = (TextView)findViewById(R.id.til_endloc);
        endLocation.setText(endCoordinate);

        TextView dumpsterLocation = (TextView)findViewById(R.id.til_dumpsterloc);
        dumpsterLocation.setText(dumpsterCoordinate);

        //EditText
        button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v){
                String ip = etIp.getText().toString();
                String gap = etLen.getText().toString();
                String data = coordinateGenerator.generate(startCoordinate, dumpsterCoordinate, endCoordinate, gap);

                // IP Address format check
                if(!Pattern.matches("([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})", ip)){
                    Toast.makeText(SelectActivity.this, "Check the format of the IP Address", Toast.LENGTH_SHORT).show();
                    etIp.setText("");
                } else if(gap.length() < 1) {
                    Toast.makeText(SelectActivity.this, "Check the format of gap", Toast.LENGTH_SHORT).show();
                    etLen.setText("");
                } else if(!Pattern.matches("[0-9]{1,3}", gap)) {
                    Toast.makeText(SelectActivity.this, "Indicate the gap", Toast.LENGTH_SHORT).show();
                }
                else{
                    BackGroundTask sending = new BackGroundTask(ip, data);
                    sending.execute();
                    goStart();
                }
            }

        });

        button2 = findViewById(R.id.back_button);
        button2.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v){
                goPrev();
            }

        });
    }
    public void goPrev(){
        Intent intent = new Intent(SelectActivity.this, MainActivity.class);
        startActivity(intent);
        finish();
    }

    class BackGroundTask extends AsyncTask<String, Void, Void> {
        String host;
        String data;

        BackGroundTask(String host, String data){
            this.host = host;
            this.data = data;
        }

        Handler h = new Handler();
        @Override
        protected Void doInBackground(String... voids) {
            Sender sender = new TCPSender();
            sender.send(host, data);
            return null;
        }
    }

    public void goStart(){
        Intent intent = new Intent(this, SplashActivity.class);
        startActivity(intent);
    }
}