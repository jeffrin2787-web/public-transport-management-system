package com.vcet.transport.controller;

import com.vcet.transport.model.*;
import com.vcet.transport.repository.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.*;

/**
 * Controller providing raw relational database tables inspection API.
 * Allows viewing all 6 schema tables and live records in the browser.
 */
@RestController
@RequestMapping("/api/db")
@CrossOrigin(origins = "*")
public class DatabaseViewerController {

    private final BusRepository busRepository;
    private final RouteRepository routeRepository;
    private final ScheduleRepository scheduleRepository;
    private final PassengerRepository passengerRepository;
    private final BookingRepository bookingRepository;
    private final TicketRepository ticketRepository;

    public DatabaseViewerController(
            BusRepository busRepository,
            RouteRepository routeRepository,
            ScheduleRepository scheduleRepository,
            PassengerRepository passengerRepository,
            BookingRepository bookingRepository,
            TicketRepository ticketRepository) {
        this.busRepository = busRepository;
        this.routeRepository = routeRepository;
        this.scheduleRepository = scheduleRepository;
        this.passengerRepository = passengerRepository;
        this.bookingRepository = bookingRepository;
        this.ticketRepository = ticketRepository;
    }

    @GetMapping("/all-tables")
    public ResponseEntity<Map<String, Object>> getAllTables() {
        Map<String, Object> result = new LinkedHashMap<>();

        // 1. Buses Table
        List<Map<String, Object>> buses = new ArrayList<>();
        for (Bus b : busRepository.findAll()) {
            Map<String, Object> row = new LinkedHashMap<>();
            row.put("bus_id", b.getId());
            row.put("bus_number", b.getBusNumber());
            row.put("bus_type", b.getBusType().name());
            row.put("total_capacity", b.getCapacity());
            row.put("operator_name", b.getOperatorName());
            buses.add(row);
        }
        result.put("buses", buses);

        // 2. Routes Table
        List<Map<String, Object>> routes = new ArrayList<>();
        for (Route r : routeRepository.findAll()) {
            Map<String, Object> row = new LinkedHashMap<>();
            row.put("route_id", r.getId());
            row.put("source_city", r.getSourceCity());
            row.put("destination_city", r.getDestinationCity());
            row.put("distance_km", r.getDistanceKm());
            row.put("estimated_duration_minutes", r.getEstimatedDurationMinutes());
            routes.add(row);
        }
        result.put("routes", routes);

        // 3. Schedules Table
        List<Map<String, Object>> schedules = new ArrayList<>();
        for (Schedule s : scheduleRepository.findAll()) {
            Map<String, Object> row = new LinkedHashMap<>();
            row.put("schedule_id", s.getId());
            row.put("bus_number", s.getBus().getBusNumber());
            row.put("corridor", s.getRoute().getSourceCity() + " -> " + s.getRoute().getDestinationCity());
            row.put("travel_date", s.getTravelDate().toString());
            row.put("departure_time", s.getDepartureTime().toString());
            row.put("arrival_time", s.getArrivalTime().toString());
            row.put("base_fare", s.getBaseFare());
            row.put("available_seats", s.getAvailableSeats());
            row.put("status", s.getStatus());
            schedules.add(row);
        }
        result.put("schedules", schedules);

        // 4. Passengers Table
        List<Map<String, Object>> passengers = new ArrayList<>();
        for (Passenger p : passengerRepository.findAll()) {
            Map<String, Object> row = new LinkedHashMap<>();
            row.put("passenger_id", p.getId());
            row.put("full_name", p.getFullName());
            row.put("age", p.getAge());
            row.put("gender", p.getGender());
            row.put("phone_number", p.getPhoneNumber());
            row.put("email", p.getEmail() != null ? p.getEmail() : "-");
            passengers.add(row);
        }
        result.put("passengers", passengers);

        // 5. Bookings Table
        List<Map<String, Object>> bookings = new ArrayList<>();
        for (Booking b : bookingRepository.findAll()) {
            Map<String, Object> row = new LinkedHashMap<>();
            row.put("booking_id", b.getId());
            row.put("pnr_number", b.getPnrNumber());
            row.put("schedule_id", b.getSchedule().getId());
            row.put("passenger_id", b.getPassenger().getId());
            row.put("passenger_name", b.getPassenger().getFullName());
            row.put("booking_time", b.getBookingTime().toString());
            row.put("total_amount", b.getTotalAmount());
            row.put("status", b.getStatus().name());
            row.put("payment_status", b.getPaymentStatus());
            bookings.add(row);
        }
        result.put("bookings", bookings);

        // 6. Tickets Table
        List<Map<String, Object>> tickets = new ArrayList<>();
        for (Ticket t : ticketRepository.findAll()) {
            Map<String, Object> row = new LinkedHashMap<>();
            row.put("ticket_id", t.getId());
            row.put("ticket_number", t.getTicketNumber());
            row.put("booking_id", t.getBooking().getId());
            row.put("seat_number", t.getSeatNumber());
            row.put("seat_fare", t.getSeatFare());
            row.put("status", t.getStatus());
            tickets.add(row);
        }
        result.put("tickets", tickets);

        return ResponseEntity.ok(result);
    }
}
