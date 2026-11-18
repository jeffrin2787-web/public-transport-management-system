package com.vcet.transport.config;

import com.vcet.transport.model.*;
import com.vcet.transport.repository.*;
import com.vcet.transport.service.BookingService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Arrays;
import java.util.List;

/**
 * Auto-seeds realistic Tamil Nadu transit records on application startup.
 * Ensures the 24/7 web app has instant live data for professors & examiners to evaluate.
 */
@Component
public class DataLoader implements CommandLineRunner {

    private final BusRepository busRepository;
    private final RouteRepository routeRepository;
    private final ScheduleRepository scheduleRepository;
    private final BookingService bookingService;

    public DataLoader(
            BusRepository busRepository,
            RouteRepository routeRepository,
            ScheduleRepository scheduleRepository,
            BookingService bookingService) {
        this.busRepository = busRepository;
        this.routeRepository = routeRepository;
        this.scheduleRepository = scheduleRepository;
        this.bookingService = bookingService;
    }

    @Override
    public void run(String... args) {
        if (busRepository.count() > 0) {
            System.out.println("[DataLoader] Database already contains records. Skipping seed.");
            return;
        }

        System.out.println("[DataLoader] Initializing Tamil Nadu Transit Network Data for VCET Scenario 10...");

        // 1. Buses
        Bus bus1 = busRepository.save(new Bus("TN-33-N-2410", BusType.AC_SLEEPER, 30, "Kongu Express Transport"));
        Bus bus2 = busRepository.save(new Bus("TN-33-N-2845", BusType.SEMI_SLEEPER, 36, "Kongu Express Transport"));
        Bus bus3 = busRepository.save(new Bus("TN-38-N-3120", BusType.ULTRA_DELUXE, 40, "Cheran Line Transits"));
        Bus bus4 = busRepository.save(new Bus("TN-27-N-1890", BusType.AC_SLEEPER, 30, "Salem City Express"));
        Bus bus5 = busRepository.save(new Bus("TN-01-AN-6701", BusType.SEMI_SLEEPER, 36, "SETC Platinum Express"));
        Bus bus6 = busRepository.save(new Bus("TN-58-N-4422", BusType.ULTRA_DELUXE, 40, "Pandian Royal Route"));
        Bus bus7 = busRepository.save(new Bus("TN-45-N-5110", BusType.NON_AC_SEATER, 45, "Cholan Intercity Direct"));
        Bus bus8 = busRepository.save(new Bus("TN-43-N-1008", BusType.AC_SLEEPER, 28, "Nilgiri Mountain Rider"));

        // 2. Routes (Hub centered around Erode / VCET)
        Route r1 = routeRepository.save(new Route("Erode", "Chennai Central", 420.0, 450));
        Route r2 = routeRepository.save(new Route("Chennai Central", "Erode", 420.0, 450));
        Route r3 = routeRepository.save(new Route("Erode", "Coimbatore", 100.5, 120));
        Route r4 = routeRepository.save(new Route("Coimbatore", "Erode", 100.5, 120));
        Route r5 = routeRepository.save(new Route("Erode", "Bengaluru", 260.0, 330));
        Route r6 = routeRepository.save(new Route("Bengaluru", "Erode", 260.0, 330));
        Route r7 = routeRepository.save(new Route("Salem", "Chennai Central", 345.0, 380));
        Route r8 = routeRepository.save(new Route("Coimbatore", "Bengaluru", 360.0, 420));
        Route r9 = routeRepository.save(new Route("Erode", "Madurai", 195.0, 240));
        Route r10 = routeRepository.save(new Route("Erode", "Tiruchirappalli", 145.0, 180));
        Route r11 = routeRepository.save(new Route("Coimbatore", "Ooty", 85.0, 180));

        // 3. Schedules (Next 3 days)
        LocalDate today = LocalDate.now();
        LocalDate tmrw = today.plusDays(1);
        LocalDate dayAfter = today.plusDays(2);

        Schedule s1 = scheduleRepository.save(new Schedule(bus1, r1, tmrw, LocalTime.of(21, 30), LocalTime.of(5, 0), 750.0));
        Schedule s2 = scheduleRepository.save(new Schedule(bus2, r1, tmrw, LocalTime.of(22, 15), LocalTime.of(5, 45), 550.0));
        Schedule s3 = scheduleRepository.save(new Schedule(bus3, r3, tmrw, LocalTime.of(7, 0), LocalTime.of(9, 0), 120.0));
        Schedule s4 = scheduleRepository.save(new Schedule(bus4, r5, tmrw, LocalTime.of(23, 0), LocalTime.of(4, 30), 650.0));
        Schedule s5 = scheduleRepository.save(new Schedule(bus5, r2, tmrw, LocalTime.of(22, 0), LocalTime.of(5, 30), 550.0));
        Schedule s6 = scheduleRepository.save(new Schedule(bus6, r9, tmrw, LocalTime.of(14, 30), LocalTime.of(18, 30), 250.0));
        Schedule s7 = scheduleRepository.save(new Schedule(bus7, r10, tmrw, LocalTime.of(8, 0), LocalTime.of(11, 0), 160.0));
        Schedule s8 = scheduleRepository.save(new Schedule(bus8, r11, tmrw, LocalTime.of(6, 30), LocalTime.of(9, 30), 320.0));
        Schedule s9 = scheduleRepository.save(new Schedule(bus1, r1, dayAfter, LocalTime.of(21, 30), LocalTime.of(5, 0), 750.0));
        Schedule s10 = scheduleRepository.save(new Schedule(bus4, r5, dayAfter, LocalTime.of(23, 0), LocalTime.of(4, 30), 650.0));

        // 4. Initial Realistic Bookings
        try {
            bookingService.bookSeats(s1.getId(), Arrays.asList(1, 2), "Jeffrin", 20, "MALE", "9876543210", "jeffrin@vcet.ac.in");
            bookingService.bookSeats(s1.getId(), Arrays.asList(5, 6), "Anand Kumar", 28, "MALE", "9842156789", "anand.k@gmail.com");
            bookingService.bookSeats(s2.getId(), Arrays.asList(3, 4), "Priya Dharshini", 24, "FEMALE", "9789123456", "priya.d@yahoo.com");
            bookingService.bookSeats(s3.getId(), Arrays.asList(7, 8, 9), "Karthik Raja", 32, "MALE", "9443218765", "karthik.r@live.com");
            bookingService.bookSeats(s4.getId(), Arrays.asList(11, 12), "Deepa Mohan", 21, "FEMALE", "9944556677", "deepa.m@outlook.com");
            bookingService.bookSeats(s6.getId(), Arrays.asList(15), "Vigneshwaran S", 26, "MALE", "9629112233", "vignesh.s@gmail.com");
            bookingService.bookSeats(s8.getId(), Arrays.asList(1, 2), "Soundarya Lakshmi", 29, "FEMALE", "9500443322", "soundarya@gmail.com");
        } catch (Exception e) {
            System.err.println("[DataLoader] Booking initialization note: " + e.getMessage());
        }

        System.out.println("[DataLoader] Tamil Nadu Transit Network initialized successfully!");
    }
}
