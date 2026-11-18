package com.vcet.transport.service;

import com.vcet.transport.exception.ResourceNotFoundException;
import com.vcet.transport.exception.SeatNotAvailableException;
import com.vcet.transport.model.*;
import com.vcet.transport.repository.BookingRepository;
import com.vcet.transport.repository.PassengerRepository;
import com.vcet.transport.repository.ScheduleRepository;
import com.vcet.transport.repository.TicketRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

/**
 * Service implementation ensuring thread-safe transactional seat allocations.
 * Demonstrates:
 * - Multithreading & Concurrency Synchronization (Unit 3: 25ITT32)
 * - Streams, Lambdas & Collections (Unit 5: 25ITT32)
 * - Exception Handling (Unit 3: 25ITT32)
 */
@Service
public class BookingServiceImpl implements BookingService {

    private final BookingRepository bookingRepository;
    private final ScheduleRepository scheduleRepository;
    private final PassengerRepository passengerRepository;
    private final TicketRepository ticketRepository;

    private static final AtomicInteger PNR_COUNTER = new AtomicInteger(1000);

    public BookingServiceImpl(
            BookingRepository bookingRepository,
            ScheduleRepository scheduleRepository,
            PassengerRepository passengerRepository,
            TicketRepository ticketRepository) {
        this.bookingRepository = bookingRepository;
        this.scheduleRepository = scheduleRepository;
        this.passengerRepository = passengerRepository;
        this.ticketRepository = ticketRepository;
    }

    @Override
    public List<Integer> getBookedSeats(Long scheduleId) {
        return ticketRepository.findBookedSeatNumbersByScheduleId(scheduleId);
    }

    /**
     * Synchronized method providing thread-safe seat allocation under concurrent requests.
     */
    @Override
    @Transactional
    public synchronized Booking bookSeats(
            Long scheduleId,
            List<Integer> seatNumbers,
            String fullName,
            int age,
            String gender,
            String phone,
            String email) {

        if (seatNumbers == null || seatNumbers.isEmpty()) {
            throw new IllegalArgumentException("At least one seat must be selected for booking.");
        }

        Schedule schedule = scheduleRepository.findById(scheduleId)
                .orElseThrow(() -> new ResourceNotFoundException("Schedule not found with ID: " + scheduleId));

        int busCapacity = schedule.getBus().getCapacity();

        // Validate seats are within bus capacity
        for (int seat : seatNumbers) {
            if (seat < 1 || seat > busCapacity) {
                throw new IllegalArgumentException("Seat " + seat + " is invalid. Bus capacity is " + busCapacity);
            }
        }

        // Fetch currently booked seats using Streams
        List<Integer> alreadyBooked = ticketRepository.findBookedSeatNumbersByScheduleId(scheduleId);
        Set<Integer> bookedSet = new HashSet<>(alreadyBooked);

        // Check for conflicts using Lambdas & Streams
        List<Integer> conflictingSeats = seatNumbers.stream()
                .filter(bookedSet::contains)
                .collect(Collectors.toList());

        if (!conflictingSeats.isEmpty()) {
            throw new SeatNotAvailableException("Seat(s) " + conflictingSeats + " are already booked. Please choose other seats.");
        }

        if (schedule.getAvailableSeats() < seatNumbers.size()) {
            throw new SeatNotAvailableException("Overbooking prevented: Requested " + seatNumbers.size() + 
                    " seat(s), but only " + schedule.getAvailableSeats() + " remain.");
        }

        // Create or find Passenger
        Passenger passenger = passengerRepository.findByPhoneNumber(phone)
                .orElseGet(() -> passengerRepository.save(new Passenger(fullName, age, gender, phone, email)));

        // Generate Unique PNR
        String pnr = "TCK-2026-" + PNR_COUNTER.incrementAndGet();
        double totalAmount = schedule.getBaseFare() * seatNumbers.size();

        Booking booking = new Booking(pnr, schedule, passenger, totalAmount);

        // Create Ticket for each seat
        for (int seat : seatNumbers) {
            String ticketNumber = "T-" + pnr.replace("TCK-", "") + "-S" + String.format("%02d", seat);
            Ticket ticket = new Ticket(ticketNumber, booking, seat, schedule.getBaseFare());
            booking.addTicket(ticket);
        }

        // Decrement available seats atomically
        schedule.setAvailableSeats(schedule.getAvailableSeats() - seatNumbers.size());
        scheduleRepository.save(schedule);

        return bookingRepository.save(booking);
    }

    @Override
    @Transactional
    public synchronized Booking cancelBooking(String pnrNumber) {
        Booking booking = bookingRepository.findByPnrNumber(pnrNumber)
                .orElseThrow(() -> new ResourceNotFoundException("Booking not found for PNR: " + pnrNumber));

        if (booking.getStatus() == BookingStatus.CANCELLED) {
            throw new IllegalStateException("Booking " + pnrNumber + " is already cancelled.");
        }

        booking.setStatus(BookingStatus.CANCELLED);
        booking.setPaymentStatus("REFUNDED");

        // Cancel all tickets and count released seats using Java Streams
        long releasedSeats = booking.getTickets().stream()
                .filter(t -> !"CANCELLED".equals(t.getStatus()))
                .peek(t -> t.setStatus("CANCELLED"))
                .count();

        // Increment schedule's available seats
        Schedule schedule = booking.getSchedule();
        schedule.setAvailableSeats(schedule.getAvailableSeats() + (int) releasedSeats);
        scheduleRepository.save(schedule);

        return bookingRepository.save(booking);
    }

    @Override
    public Optional<Booking> getBookingByPnr(String pnrNumber) {
        return bookingRepository.findByPnrNumber(pnrNumber);
    }

    @Override
    public List<Booking> getAllBookings() {
        return bookingRepository.findAllRecentBookings();
    }
}
