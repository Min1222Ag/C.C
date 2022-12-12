package com.example.cc;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputLayout;

import org.w3c.dom.Text;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Pattern;

public class SelectActivity extends AppCompatActivity {
    //Initialize variable
    TextInputLayout tilDistance, tilIp;

    HashMap<String, String> locations;


    EditText etLen, etIp;
    MaterialButton button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_select);

        //Assign variable
        tilDistance = findViewById(R.id.til_len);
        etLen = findViewById(R.id.et_len);

        tilIp = findViewById(R.id.til_ip);
        etIp = findViewById(R.id.et_ip);


        Intent intent = getIntent();

        locations = (HashMap<String, String>)intent.getSerializableExtra("locations");
        Toast.makeText(getApplicationContext(), "length of received data:" + locations, Toast.LENGTH_SHORT).show();



        TextView startLocation = (TextView)findViewById(R.id.til_startloc);
        startLocation.setText(locations.get("start_coordinate").substring(10, locations.get("start_coordinate").length()-1));

        TextView endLocation = (TextView)findViewById(R.id.til_endloc);
        endLocation.setText(locations.get("end_coordinate").substring(10, locations.get("end_coordinate").length()-1));

        TextView dumpsterLocation = (TextView)findViewById(R.id.til_dumpsterloc);
        dumpsterLocation.setText(locations.get("dumpster_coordinate").substring(10, locations.get("dumpster_coordinate").length()-1));


        //EditText
        button = findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v){
                String ip = etIp.getText().toString();

                // IP Address format check
                if(!Pattern.matches("([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})\\.([0-9]{1,3})", ip)){
                    Toast.makeText(SelectActivity.this, "Check your IP Address", Toast.LENGTH_SHORT).show();
                    etIp.setText("");
                } else {
                    openTracking();
                }
            }

        });
    }

    public void openTracking(){
        Intent intent = new Intent(this, TrackingActivity.class);

        intent.putExtra("locations", locations);
        startActivity(intent);
    }
}