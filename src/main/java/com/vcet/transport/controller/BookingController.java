package com.vcet.transport.controller;

import com.vcet.transport.model.Booking;
import com.vcet.transport.model.Schedule;
import com.vcet.transport.service.BookingService;
import com.vcet.transport.service.RouteService;
import com.vcet.transport.service.ScheduleService;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class BookingController {

    private final BookingService bookingService;
    private final ScheduleService scheduleService;
    private final RouteService routeService;

    public BookingController(BookingService bookingService, ScheduleService scheduleService, RouteService routeService) {
        this.bookingService = bookingService;
        this.scheduleService = scheduleService;
        this.routeService = routeService;
    }

    @GetMapping("/cities")
    public ResponseEntity<Map<String, List<String>>> getCities() {
        Map<String, List<String>> response = new HashMap<>();
        response.put("sources", routeService.getSourceCities());
        response.put("destinations", routeService.getDestinationCities());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/schedules/search")
    public ResponseEntity<List<Schedule>> searchSchedules(
            @RequestParam(required = false) String source,
            @RequestParam(required = false) String destination,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date) {
        List<Schedule> schedules = scheduleService.searchSchedules(source, destination, date);
        return ResponseEntity.ok(schedules);
    }

    @GetMapping("/schedules/{id}")
    public ResponseEntity<Schedule> getSchedule(@PathVariable Long id) {
        return scheduleService.getScheduleById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/schedules/{id}/seats")
    public ResponseEntity<Map<String, Object>> getSeatStatus(@PathVariable Long id) {
        Schedule schedule = scheduleService.getScheduleById(id)
                .orElseThrow(() -> new IllegalArgumentException("Schedule not found with ID: " + id));

        List<Integer> bookedSeats = bookingService.getBookedSeats(id);

        Map<String, Object> response = new HashMap<>();
        response.put("scheduleId", id);
        response.put("busType", schedule.getBus().getBusType());
        response.put("totalCapacity", schedule.getBus().getCapacity());
        response.put("availableSeatsCount", schedule.getAvailableSeats());
        response.put("bookedSeats", bookedSeats);
        response.put("baseFare", schedule.getBaseFare());
        return ResponseEntity.ok(response);
    }

    public static class BookingRequest {
        public Long scheduleId;
        public List<Integer> seatNumbers;
        public String fullName;
        public int age;
        public String gender;
        public String phoneNumber;
        public String email;
    }

    @PostMapping("/bookings")
    public ResponseEntity<Booking> createBooking(@RequestBody BookingRequest request) {
        Booking booking = bookingService.bookSeats(
                request.scheduleId,
                request.seatNumbers,
                request.fullName,
                request.age,
                request.gender,
                request.phoneNumber,
                request.email
        );
        return new ResponseEntity<>(booking, HttpStatus.CREATED);
    }

    @PostMapping("/bookings/cancel/{pnr}")
    public ResponseEntity<Map<String, Object>> cancelBooking(@PathVariable String pnr) {
        Booking cancelled = bookingService.cancelBooking(pnr);
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Booking cancelled successfully. Seats released back to inventory.");
        response.put("pnr", cancelled.getPnrNumber());
        response.put("status", cancelled.getStatus());
        response.put("refundAmount", cancelled.getTotalAmount());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/bookings/{pnr}")
    public ResponseEntity<Booking> getBookingDetails(@PathVariable String pnr) {
        return bookingService.getBookingByPnr(pnr)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
