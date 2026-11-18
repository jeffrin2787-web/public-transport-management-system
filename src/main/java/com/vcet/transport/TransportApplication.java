package com.vcet.transport;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Main Application Bootstrapper
 * Public Transport Management and Passenger Travel Analysis System
 * Velalar College of Engineering and Technology (VCET), Erode - 12
 * Student: Jeffrin (Reg No: 732925ITR040) | Class: 25IT3A
 */
@SpringBootApplication
public class TransportApplication {

    public static void main(String[] args) {
        SpringApplication.run(TransportApplication.class, args);
        System.out.println("==================================================================");
        System.out.println("  PUBLIC TRANSPORT MANAGEMENT & PASSENGER TRAVEL ANALYSIS SYSTEM  ");
        System.out.println("  VELALAR COLLEGE OF ENGINEERING AND TECHNOLOGY, ERODE - 12       ");
        System.out.println("  AUTHOR: JEFFRIN | REG NO: 732925ITR040 | CLASS: 25IT3A          ");
        System.out.println("  SERVER RUNNING AT: http://localhost:8080                        ");
        System.out.println("==================================================================");
    }
}
