package com.example.cc.coordinates;

/*
 interface of generator of valid json format of coordinates to send them to driving control unit
 */
public interface CoordinateGenerator {
    String generate(String startCoordinate, String dumpsterCoordinate, String endCoordinate, String gap);
}
