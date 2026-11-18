package com.vcet.transport.controller;

import com.vcet.transport.model.*;
import com.vcet.transport.service.*;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@RestController
@RequestMapping("/api/admin")
@CrossOrigin(origins = "*")
public class AdminController {

    private final BusService busService;
    private final RouteService routeService;
    private final ScheduleService scheduleService;
    private final BookingService bookingService;

    public AdminController(
            BusService busService,
            RouteService routeService,
            ScheduleService scheduleService,
            BookingService bookingService) {
        this.busService = busService;
        this.routeService = routeService;
        this.scheduleService = scheduleService;
        this.bookingService = bookingService;
    }

    // ------------------------------------------------------------------------
    // Bus Fleet Endpoints
    // ------------------------------------------------------------------------
    @GetMapping("/buses")
    public ResponseEntity<List<Bus>> getAllBuses() {
        return ResponseEntity.ok(busService.getAllBuses());
    }

    public static class BusCreateRequest {
        public String busNumber;
        public String busType;
        public int capacity;
        public String operatorName;
    }

    @PostMapping("/buses")
    public ResponseEntity<Bus> createBus(@RequestBody BusCreateRequest req) {
        BusType type = BusType.valueOf(req.busType);
        Bus bus = busService.registerBus(req.busNumber, type, req.capacity, req.operatorName);
        return new ResponseEntity<>(bus, HttpStatus.CREATED);
    }

    // ------------------------------------------------------------------------
    // Route Corridors Endpoints
    // ------------------------------------------------------------------------
    @GetMapping("/routes")
    public ResponseEntity<List<Route>> getAllRoutes() {
        return ResponseEntity.ok(routeService.getAllRoutes());
    }

    public static class RouteCreateRequest {
        public String sourceCity;
        public String destinationCity;
        public double distanceKm;
        public int estimatedDurationMinutes;
    }

    @PostMapping("/routes")
    public ResponseEntity<Route> createRoute(@RequestBody RouteCreateRequest req) {
        Route route = routeService.createRoute(
                req.sourceCity,
                req.destinationCity,
                req.distanceKm,
                req.estimatedDurationMinutes
        );
        return new ResponseEntity<>(route, HttpStatus.CREATED);
    }

    // ------------------------------------------------------------------------
    // Schedule Endpoints
    // ------------------------------------------------------------------------
    @GetMapping("/schedules")
    public ResponseEntity<List<Schedule>> getAllSchedules() {
        return ResponseEntity.ok(scheduleService.getAllUpcomingSchedules());
    }

    public static class ScheduleCreateRequest {
        public Long busId;
        public Long routeId;
        public String travelDate;     // YYYY-MM-DD
        public String departureTime;  // HH:MM
        public String arrivalTime;    // HH:MM
        public double baseFare;
    }

    @PostMapping("/schedules")
    public ResponseEntity<Schedule> createSchedule(@RequestBody ScheduleCreateRequest req) {
        LocalDate date = LocalDate.parse(req.travelDate);
        LocalTime dep = LocalTime.parse(req.departureTime);
        LocalTime arr = LocalTime.parse(req.arrivalTime);

        Schedule schedule = scheduleService.createSchedule(
                req.busId,
                req.routeId,
                date,
                dep,
                arr,
                req.baseFare
        );
        return new ResponseEntity<>(schedule, HttpStatus.CREATED);
    }

    // ------------------------------------------------------------------------
    // Master Bookings List
    // ------------------------------------------------------------------------
    @GetMapping("/bookings")
    public ResponseEntity<List<Booking>> getAllBookings() {
        return ResponseEntity.ok(bookingService.getAllBookings());
    }
}
