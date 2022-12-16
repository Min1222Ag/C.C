package com.example.cc;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.FragmentActivity;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
//import com.google.android.gms.common.api.internal.ApiKey;
//import com.google.android.gms.location.CurrentLocationRequest;
import com.google.android.gms.location.FusedLocationProviderClient;
//import com.google.android.gms.location.LastLocationRequest;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.karumi.dexter.Dexter;
import com.karumi.dexter.PermissionToken;
import com.karumi.dexter.listener.PermissionDeniedResponse;
import com.karumi.dexter.listener.PermissionGrantedResponse;
import com.karumi.dexter.listener.PermissionRequest;
import com.karumi.dexter.listener.single.PermissionListener;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class GpsActivity extends FragmentActivity implements OnMapReadyCallback, GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, GoogleMap.OnMarkerClickListener, GoogleMap.OnMarkerDragListener {

    private Button button; // button for moving to the next activity
    private Button fab; // button for updating current location
    boolean isPermissionGranted;

    GoogleMap mGoogleMap;
    HashMap<String, String>locations; // hashmap for locations <"name", "(latitude, longitude)">

    private FusedLocationProviderClient mLocationClient;
    private int GPS_REQUEST_CODE = 9001;

    // hashmap for markers <"name", marker>
    private final Map<String, MarkerOptions> mMarkers = new ConcurrentHashMap<String, MarkerOptions>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gps);

        locations = new HashMap<String, String>();

        checkMyPermission();

        initMap(); // initialize map

        mLocationClient = new FusedLocationProviderClient(this);

        fab = findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener(){ // move to current location
            @Override
            public void onClick(View view){
                getCurrLoc();
            }
        });

        button = (Button) findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener(){ // move to Select Activity
            @Override
            public void onClick(View v){
                openSelect();
            }
        });

    }

    public void openSelect(){ // send hashmap locations data to Select Activity
        Intent intent = new Intent(GpsActivity.this, SelectActivity.class);

        locations.put("time", "");
        locations.put("meter", "");
        intent.putExtra("locations", locations);

        startActivity(intent);
    }

    private void initMap() {
        if(isPermissionGranted){
            if(isGPSenable()){
                SupportMapFragment supportMapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.fragment);
                supportMapFragment.getMapAsync(this);
            }
        }
    }

    private boolean isGPSenable(){
        LocationManager locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);

        boolean providerEnable = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);

        if(providerEnable){
            return true;
        } else{
            AlertDialog alertDialog = new AlertDialog.Builder(this)
                    .setTitle("GPS Permission")
                    .setMessage("GPS is required for this app to work. Please enable GPS")
                    .setPositiveButton("Yes", ((dialogInterface, i) -> {
                        Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
                        startActivityForResult(intent, GPS_REQUEST_CODE);
                    }))
                    .setCancelable(false)
                    .show();
        }
        return false;
    }

    @SuppressLint("MissingPermission")
    private void getCurrLoc() {
        mLocationClient.getLastLocation().addOnCompleteListener(task ->{
            if(task.isSuccessful()){
                Location location = task.getResult();
                LatLng LatLng = new LatLng(location.getLatitude(), location.getLongitude());

                CameraUpdate cameraUpdate = CameraUpdateFactory.newLatLngZoom(LatLng, 20);
                mGoogleMap.moveCamera(cameraUpdate);
                mGoogleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);

                add("Start", LatLng);
                if(!locations.containsKey("End") || !locations.containsKey("Dumpster")){
                    LatLng = new LatLng(location.getLatitude(), location.getLongitude()+0.0001);
                    add("Dumpster", LatLng);
                    LatLng = new LatLng(location.getLatitude(), location.getLongitude()+0.0002);
                    add("End", LatLng);
                }
            }
        });
    }

    private void checkMyPermission() {
        Dexter.withContext(this).withPermission(Manifest.permission.ACCESS_FINE_LOCATION).withListener(new PermissionListener() {
            @Override
            public void onPermissionGranted(PermissionGrantedResponse permissionGrantedResponse) {
                Toast.makeText(GpsActivity.this, "Permission Granted", Toast.LENGTH_SHORT).show();
                isPermissionGranted = true;
            }

            @Override
            public void onPermissionDenied(PermissionDeniedResponse permissionDeniedResponse) {
                Intent intent = new Intent();
                intent.setAction(Settings.ACTION_APPLICATION_DETAILS_SETTINGS);
                Uri uri = Uri.fromParts("package", getPackageName(), "");
                intent.setData(uri);
                startActivity(intent);
            }

            @Override
            public void onPermissionRationaleShouldBeShown(PermissionRequest permissionRequest, PermissionToken permissionToken) {
                permissionToken.continuePermissionRequest();
            }
        }).check();
    }

    @SuppressLint("MissingPermission")
    @Override
    public void onMapReady(GoogleMap googleMap) {

        mGoogleMap = googleMap;
        mGoogleMap.setMyLocationEnabled(true);
        mGoogleMap.getUiSettings().setMyLocationButtonEnabled(false);

        getCurrLoc();

        mGoogleMap.setOnMarkerClickListener(this);
        mGoogleMap.setOnMarkerDragListener(this);

    }

    @Override
    public void onConnected(@Nullable Bundle bundle) {

    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(requestCode == GPS_REQUEST_CODE){
            LocationManager locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);

            boolean providerEnable = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);

            if(providerEnable){
                Toast.makeText(this, "GPS is enable", Toast.LENGTH_SHORT).show();
            } else{
                Toast.makeText(this, "GPS is not enable", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void add(String name, LatLng Latlng) {
        final MarkerOptions marker = new MarkerOptions().position(Latlng).title(name);

        if(name == "Start"){
            locations.put("start_coordinate", String.valueOf(Latlng));
        }
        else if(name == "End"){
            marker.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_BLUE));
            locations.put("end_coordinate", String.valueOf(Latlng));
        } else if(name == "Dumpster"){
            marker.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN));
            locations.put("dumpster_coordinate", String.valueOf(Latlng));
        }

        if(mMarkers.size() != 0){
            remove(marker.getTitle());
        }

        mMarkers.put(name, marker);

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                marker.draggable(true);
                mGoogleMap.addMarker(marker).showInfoWindow();
            }
        });
    }

    private void remove(String name) {
        mMarkers.remove(name);

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                mGoogleMap.clear();

                for (MarkerOptions item : mMarkers.values()) {
                    mGoogleMap.addMarker(item);
                }
            }
        });
    }

    @Override
    public boolean onMarkerClick(Marker marker) {
        return false;
    }

    @Override
    public void onMarkerDragStart(Marker marker) {
        marker.setTitle(marker.getTitle());
        marker.showInfoWindow();
        marker.setAlpha(0.5f);
    }

    @Override
    public void onMarkerDrag(Marker marker) {
        marker.setTitle(marker.getTitle());
        marker.showInfoWindow();
        marker.setAlpha(0.5f);
    }

    @Override
    public void onMarkerDragEnd(Marker marker) {
        marker.setTitle(marker.getTitle());
        marker.showInfoWindow();
        marker.setAlpha(0.5f);

        Toast.makeText(getApplicationContext(), String.valueOf(marker.getPosition()), Toast.LENGTH_SHORT).show();
        putMarkerLocation(marker);
    }

    public void putMarkerLocation(Marker marker){
        if(marker.getTitle().equals("Start")){
            if(locations.containsKey("start_coordinate")){
                locations.remove("start_coordinate");
            }
            locations.put("start_coordinate", String.valueOf(marker.getPosition()));
            add("Start", marker.getPosition());
        } else if(marker.getTitle().equals("End")){
            if(locations.containsKey("end_coordinate")){
                locations.remove("end_coordinate");
            }
            locations.put("end_coordinate", String.valueOf(marker.getPosition()));
            add("End", marker.getPosition());
        } else if(marker.getTitle().equals("Dumpster")){
            if(locations.containsKey("dumpster_coordinate")){
                locations.remove("dumpster_coordinate");
            }
            locations.put("dumpster_coordinate", String.valueOf(marker.getPosition()));
            add("Dumpster", marker.getPosition());
        }
    }
}