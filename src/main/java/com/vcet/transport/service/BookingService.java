package com.vcet.transport.service;

import com.vcet.transport.model.Booking;

import java.util.List;
import java.util.Optional;

/**
 * Interface defining contract for passenger booking operations (Unit 2: 25ITT32).
 */
public interface BookingService {
    List<Integer> getBookedSeats(Long scheduleId);
    Booking bookSeats(Long scheduleId, List<Integer> seatNumbers, String fullName, int age, String gender, String phone, String email);
    Booking cancelBooking(String pnrNumber);
    Optional<Booking> getBookingByPnr(String pnrNumber);
    List<Booking> getAllBookings();
}
