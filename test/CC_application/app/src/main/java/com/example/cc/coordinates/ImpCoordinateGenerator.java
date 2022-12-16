package com.example.cc.coordinates;

import java.text.SimpleDateFormat;
import java.util.Date;

/*
 Coordinates data in json format followed:
    { "time": [time when the coordinates being sent],
      "start_coordinate": {"latitude": [start location latitude], "longitude": [start location longitude]},
      "end_coordinate": {"latitude": [end location latitude], "longitude": [end location longitude]},
      "dumpster_coordinate": {"latitude": [dumpster location latitude], "longitude": [dumpster location longitude]},
      "meter": [gap between subgoals]
    }
 */
public class ImpCoordinateGenerator implements CoordinateGenerator{

    public String makeCoordinate(String coordinate) { // [latitude],[longitude] -> {"latitude": [latitude], "longitude": [longitude]}
        String[] latNlon = coordinate.split(",", 2);
        return "{\"latitude\": "+latNlon[0]+", \"longitude\": "+latNlon[1]+"}";
    }

    @Override
    public String generate(String startCoordinate, String dumpsterCoordinate, String endCoordinate, String gap) {

        // generate date
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
                ", \"meter\": " + gap + "}"; // form json format

        return path_string; // return json string
    }
}
