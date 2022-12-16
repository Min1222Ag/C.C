package com.example.cc;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
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
    // initialize variable
    TextInputLayout tilDistance, tilIp;
    HashMap<String, String> locations; // hashmap for locations <"name", "(latitude, longitude)">
    EditText etLen, etIp;
    MaterialButton button, button2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_select);

        CoordinateGenerator coordinateGenerator = new ImpCoordinateGenerator();

        // assign variable
        tilDistance = findViewById(R.id.til_len);
        etLen = findViewById(R.id.et_len);
        tilIp = findViewById(R.id.til_ip);
        etIp = findViewById(R.id.et_ip);

        Intent intent = getIntent();
        locations = (HashMap<String, String>)intent.getSerializableExtra("locations"); // get locations hashmap from MainActivity

        // split the coordinate string to get right format
        String startCoordinate = locations.get("start_coordinate").substring(10, locations.get("start_coordinate").length()-1);
        String endCoordinate = locations.get("end_coordinate").substring(10, locations.get("end_coordinate").length()-1);
        String dumpsterCoordinate = locations.get("dumpster_coordinate").substring(10, locations.get("dumpster_coordinate").length()-1);

        TextView startLocation = (TextView)findViewById(R.id.til_startloc); // start location text view
        startLocation.setText(startCoordinate);

        TextView endLocation = (TextView)findViewById(R.id.til_endloc); // end location text view
        endLocation.setText(endCoordinate);

        TextView dumpsterLocation = (TextView)findViewById(R.id.til_dumpsterloc); // dumpster location text view
        dumpsterLocation.setText(dumpsterCoordinate);

        button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener(){
            // confirm button: send data using TCP socket
            @Override
            public void onClick(View v){
                String ip = etIp.getText().toString(); // get IP address
                String gap = etLen.getText().toString();  // get subgoal distance
                String data = coordinateGenerator.generate(startCoordinate, dumpsterCoordinate, endCoordinate, gap); // generate coordinate generator

                if(!Pattern.matches("([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})", ip)){
                    // IP address format check
                    Toast.makeText(SelectActivity.this, "Check the format of the IP Address", Toast.LENGTH_SHORT).show();
                    etIp.setText("");
                } else if(gap.length() < 1) { // subgoal distance format check
                    Toast.makeText(SelectActivity.this, "Check the format of gap", Toast.LENGTH_SHORT).show();
                    etLen.setText("");
                } else if(!Pattern.matches("[0-9]{1,3}", gap)) {
                    Toast.makeText(SelectActivity.this, "Indicate the gap", Toast.LENGTH_SHORT).show();
                }
                else{ // execute sending
                    BackGroundTask sending = new BackGroundTask(ip, data);
                    sending.execute();
                    goStart();
                }
            }
        });

        button2 = findViewById(R.id.back_button);
        button2.setOnClickListener(new View.OnClickListener(){
            // go back button: move to previous activity
            @Override
            public void onClick(View v){
                goPrev();
            }

        });
    }
    public void goPrev(){ // go back to previous gps activity to choose again
        Intent intent = new Intent(SelectActivity.this, MainActivity.class);
        startActivity(intent);
        finish();
    }

    class BackGroundTask extends AsyncTask<String, Void, Void> {
        String host; // ip address to connect with
        String data; // data to send

        BackGroundTask(String host, String data){ // constructor
            this.host = host;
            this.data = data;
        }

        @Override
        protected Void doInBackground(String... voids) {
            Sender sender = new TCPSender(); // generate TCP class
            sender.send(host, data); // send the data to host ip address
            return null; // end of background task
        }
    }

    public void goStart(){
        // show success message after sending the data
        Toast.makeText(SelectActivity.this, "Sending success", Toast.LENGTH_SHORT).show();
    }
}