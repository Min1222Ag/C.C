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
import com.google.android.gms.location.FusedLocationProviderClient;
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

public class MainActivity extends FragmentActivity implements OnMapReadyCallback, GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, GoogleMap.OnMarkerClickListener, GoogleMap.OnMarkerDragListener {
    // initialize variable
    private Button button; // button for moving to the next activity
    private Button fab; // button for updating current location
    boolean isPermissionGranted; // check permission

    GoogleMap mGoogleMap;
    HashMap<String, String>locations; // hashmap for locations <"name", "(latitude, longitude)">

    private FusedLocationProviderClient mLocationClient; // the main entry point for interacting with the Fused Location Provider
    private int GPS_REQUEST_CODE = 9001;

    private final Map<String, MarkerOptions> mMarkers = new ConcurrentHashMap<String, MarkerOptions>(); // hashmap for markers <"name", marker>

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        locations = new HashMap<String, String>();

        checkMyPermission(); // permission check

        initMap(); // initialize the map

        mLocationClient = new FusedLocationProviderClient(this);

        fab = findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener(){
            // current location button: move start marker to current location
            @Override
            public void onClick(View view){
                getCurrLoc();
            }
        });

        button = (Button) findViewById(R.id.button);
        button.setOnClickListener(new View.OnClickListener(){
            // select button: move to Select Activity
            @Override
            public void onClick(View v){
                openSelect();
            }
        });

    }

    public void openSelect(){
        // send locations hashmap data to Select Activity
        Intent intent = new Intent(MainActivity.this, SelectActivity.class);

        locations.put("time", "");
        locations.put("meter", "");
        intent.putExtra("locations", locations);
        startActivity(intent);
    }

    private void initMap() {
        if(isPermissionGranted){
            if(isGPSenable()){
                SupportMapFragment supportMapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.fragment); // map component
                supportMapFragment.getMapAsync(this); // set a callback object
            }
        }
    }

    private boolean isGPSenable(){
        LocationManager locationManager = (LocationManager) getSystemService(LOCATION_SERVICE); // check the GPS

        boolean providerEnable = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);

        if(providerEnable){ // GPS enable
            return true;
        } else{ // if GPS is not able, redirect to the settings app to enable GPS manually
            AlertDialog alertDialog = new AlertDialog.Builder(this) // alert view
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
                Location location = task.getResult(); // get latitude and longitude as a result
                LatLng LatLng = new LatLng(location.getLatitude(), location.getLongitude());

                CameraUpdate cameraUpdate = CameraUpdateFactory.newLatLngZoom(LatLng, 20); // camera view
                mGoogleMap.moveCamera(cameraUpdate);
                mGoogleMap.setMapType(GoogleMap.MAP_TYPE_NORMAL);

                add("Start", LatLng); // add start marker to current location
                if(!locations.containsKey("End") || !locations.containsKey("Dumpster")){
                    // aligned end, dumpster marker next to the start marker
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
            public void onPermissionGranted(PermissionGrantedResponse permissionGrantedResponse) { // permission granted
                Toast.makeText(MainActivity.this, "Permission Granted", Toast.LENGTH_SHORT).show();
                isPermissionGranted = true;
            }

            @Override
            public void onPermissionDenied(PermissionDeniedResponse permissionDeniedResponse) {
                Intent intent = new Intent();
                intent.setAction(Settings.ACTION_APPLICATION_DETAILS_SETTINGS); // if permission denied, redirect to settings app to change the settings
                Uri uri = Uri.fromParts("package", getPackageName(), "");
                intent.setData(uri);
                startActivity(intent);
            }

            @Override
            public void onPermissionRationaleShouldBeShown(PermissionRequest permissionRequest, PermissionToken permissionToken) {
                permissionToken.continuePermissionRequest(); // show permission token to continue permission method
            }
        }).check();
    }

    @SuppressLint("MissingPermission")
    @Override
    public void onMapReady(GoogleMap googleMap) {

        mGoogleMap = googleMap; // initialize google map
        mGoogleMap.setMyLocationEnabled(true); // get user current location
        mGoogleMap.getUiSettings().setMyLocationButtonEnabled(false); // hide current location button

        getCurrLoc(); // load current location

        mGoogleMap.setOnMarkerClickListener(this); // set marker to get click action
        mGoogleMap.setOnMarkerDragListener(this); // set marker to get drag action

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

            // show toast message of GPS state
            if(providerEnable){
                Toast.makeText(this, "GPS is enable", Toast.LENGTH_SHORT).show();
            } else{
                Toast.makeText(this, "GPS is not enable", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void add(String name, LatLng Latlng) {
        final MarkerOptions marker = new MarkerOptions().position(Latlng).title(name); // initialize individual marker

        if(name == "Start"){
            locations.put("start_coordinate", String.valueOf(Latlng)); // put start_coordinate information into hashmap
        }
        else if(name == "End"){
            marker.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_BLUE)); // change marker color(Blue)
            locations.put("end_coordinate", String.valueOf(Latlng)); // put end_coordinate information into hashmap
        } else if(name == "Dumpster"){
            marker.icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN)); // change marker color(Green)
            locations.put("dumpster_coordinate", String.valueOf(Latlng)); // put dumpster_coordinate information into hashmap
        }

        if(mMarkers.size() != 0){
            remove(marker.getTitle()); // prevent create duplicate marker
        }

        mMarkers.put(name, marker); // add marker in marker hashmap

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                marker.draggable(true); // give marker draggable condition
                mGoogleMap.addMarker(marker).showInfoWindow(); // visualize marker on map
            }
        });
    }

    private void remove(String name) {
        mMarkers.remove(name); // remove marker in marker hashmap

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                mGoogleMap.clear(); // clear google map

                for (MarkerOptions item : mMarkers.values()) {
                    mGoogleMap.addMarker(item); // visualize markers in mMarkers hashmap on google map
                }
            }
        });
    }

    @Override
    public boolean onMarkerClick(Marker marker) {
        return false;
    }

    @Override
    public void onMarkerDragStart(Marker marker) { // marker drag start
        marker.setTitle(marker.getTitle());
        marker.showInfoWindow();
    }

    @Override
    public void onMarkerDrag(Marker marker) { // marker drag
        marker.setTitle(marker.getTitle());
        marker.showInfoWindow();
        marker.setAlpha(0.5f); // change opacity while dragging the marker
    }

    @Override
    public void onMarkerDragEnd(Marker marker) { // marker drag end
        marker.setTitle(marker.getTitle());
        marker.showInfoWindow();

        Toast.makeText(getApplicationContext(), String.valueOf(marker.getPosition()), Toast.LENGTH_SHORT).show(); // show the coordinate of the marker
        putMarkerLocation(marker); // update marker coordinate in hashmap
    }

    public void putMarkerLocation(Marker marker){
        if(marker.getTitle().equals("Start")){
            if(locations.containsKey("start_coordinate")){ // check locations hashmap contains start_coordinate
                locations.remove("start_coordinate"); // remove previous location data
            }
            locations.put("start_coordinate", String.valueOf(marker.getPosition())); // add start_coordinate data into locations hashmap
            add("Start", marker.getPosition()); // add start marker in mMarkers hashmap
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