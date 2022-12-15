package com.example.cc.coordinates;

import java.text.SimpleDateFormat;
import java.util.Date;

public class ImpCoordinateGenerator implements CoordinateGenerator{
    public String makeCoordinate(String coordinate) {
        String[] latNlon = coordinate.split(",", 2);
        return "{\"latitude\": "+latNlon[0]+", \"longitude\": "+latNlon[1]+"}";
    }

    @Override
    public String generate(String startCoordinate, String dumpsterCoordinate, String endCoordinate, String gap) {

        SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
        Date date = new Date();

        String path_string = "{\"time\": \"" +
                formatter.format(date) +
                "\", \"start_coordinate\": " +
                makeCoordinate(startCoordinate) +
                ", \"end_coordinate\": " +
                makeCoordinate(endCoordinate) +
                ", \"dumpster_coordinate\": " +
                makeCoordinate(dumpsterCoordinate) +
                ", \"meter\": " + gap + "}";

        return path_string;
    }
}
