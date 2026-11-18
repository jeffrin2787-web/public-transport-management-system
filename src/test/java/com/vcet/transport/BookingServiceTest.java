package com.vcet.transport;

import com.vcet.transport.exception.SeatNotAvailableException;
import com.vcet.transport.model.*;
import com.vcet.transport.repository.BusRepository;
import com.vcet.transport.repository.RouteRepository;
import com.vcet.transport.repository.ScheduleRepository;
import com.vcet.transport.service.BookingService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class BookingServiceTest {

    @Autowired
    private BookingService bookingService;

    @Autowired
    private BusRepository busRepository;

    @Autowired
    private RouteRepository routeRepository;

    @Autowired
    private ScheduleRepository scheduleRepository;

    private Schedule testSchedule;

    @BeforeEach
    void setUp() {
        Bus bus = busRepository.save(new Bus("TN-TEST-001", BusType.AC_SLEEPER, 20, "Test Travels"));
        Route route = routeRepository.save(new Route("Test Origin", "Test Dest", 100.0, 120));
        testSchedule = scheduleRepository.save(new Schedule(bus, route, LocalDate.now().plusDays(5), LocalTime.of(10, 0), LocalTime.of(12, 0), 300.0));
    }

    @Test
    @DisplayName("TC-BOOK-01: Successful single seat reservation")
    void testSuccessfulBooking() {
        int initialSeats = testSchedule.getAvailableSeats();
        Booking booking = bookingService.bookSeats(
                testSchedule.getId(),
                Collections.singletonList(1),
                "Jeffrin",
                20,
                "MALE",
                "9876543210",
                "jeffrin@vcet.ac.in"
        );

        assertNotNull(booking);
        assertNotNull(booking.getPnrNumber());
        assertEquals(BookingStatus.CONFIRMED, booking.getStatus());

        Schedule updated = scheduleRepository.findById(testSchedule.getId()).orElseThrow();
        assertEquals(initialSeats - 1, updated.getAvailableSeats());
    }

    @Test
    @DisplayName("TC-BOOK-02: Double booking prevention on same seat")
    void testDoubleBookingPrevention() {
        bookingService.bookSeats(
                testSchedule.getId(),
                Collections.singletonList(5),
                "Passenger A",
                25,
                "MALE",
                "9123456780",
                "a@gmail.com"
        );

        assertThrows(SeatNotAvailableException.class, () -> {
            bookingService.bookSeats(
                    testSchedule.getId(),
                    Collections.singletonList(5),
                    "Passenger B",
                    30,
                    "FEMALE",
                    "9123456781",
                    "b@gmail.com"
            );
        });
    }

    @Test
    @DisplayName("TC-CANC-01: Cancellation releases seat back to schedule")
    void testCancellationReleasesSeat() {
        Booking booking = bookingService.bookSeats(
                testSchedule.getId(),
                Collections.singletonList(10),
                "Jeffrin",
                20,
                "MALE",
                "9876543210",
                "jeffrin@vcet.ac.in"
        );

        Schedule afterBooking = scheduleRepository.findById(testSchedule.getId()).orElseThrow();
        int availableAfterBooking = afterBooking.getAvailableSeats();

        Booking cancelled = bookingService.cancelBooking(booking.getPnrNumber());
        assertEquals(BookingStatus.CANCELLED, cancelled.getStatus());

        Schedule afterCancellation = scheduleRepository.findById(testSchedule.getId()).orElseThrow();
        assertEquals(availableAfterBooking + 1, afterCancellation.getAvailableSeats());
    }

    @Test
    @DisplayName("TC-CONC-01: Multithreaded concurrent requests prevent overbooking")
    void testMultithreadedConcurrentOverbookingPrevention() throws InterruptedException {
        // Create a bus schedule with only 1 seat remaining
        Bus bus = busRepository.save(new Bus("TN-RACE-001", BusType.NON_AC_SEATER, 1, "Race Travels"));
        Route route = routeRepository.save(new Route("Race Start", "Race End", 50.0, 60));
        Schedule tightSchedule = scheduleRepository.save(new Schedule(bus, route, LocalDate.now().plusDays(6), LocalTime.of(9, 0), LocalTime.of(10, 0), 200.0));
        tightSchedule.setAvailableSeats(1);
        scheduleRepository.save(tightSchedule);

        final int NUM_THREADS = 8;
        ExecutorService executor = Executors.newFixedThreadPool(NUM_THREADS);
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch finishLatch = new CountDownLatch(NUM_THREADS);

        AtomicInteger successCount = new AtomicInteger(0);
        AtomicInteger rejectedCount = new AtomicInteger(0);

        for (int i = 0; i < NUM_THREADS; i++) {
            final int threadIdx = i;
            executor.submit(() -> {
                try {
                    startLatch.await(); // wait for gun shot
                    bookingService.bookSeats(
                            tightSchedule.getId(),
                            Collections.singletonList(1),
                            "User " + threadIdx,
                            22,
                            "MALE",
                            "900000000" + threadIdx,
                            "user" + threadIdx + "@test.com"
                    );
                    successCount.incrementAndGet();
                } catch (SeatNotAvailableException | IllegalArgumentException e) {
                    rejectedCount.incrementAndGet();
                } catch (Exception e) {
                    rejectedCount.incrementAndGet();
                } finally {
                    finishLatch.countDown();
                }
            });
        }

        startLatch.countDown(); // Release all threads at once
        finishLatch.await(10, TimeUnit.SECONDS);
        executor.shutdown();

        assertEquals(1, successCount.get(), "Only 1 thread should successfully reserve the single available seat!");
        assertEquals(NUM_THREADS - 1, rejectedCount.get(), "All other concurrent attempts must be rejected to prevent overbooking!");
    }
}
