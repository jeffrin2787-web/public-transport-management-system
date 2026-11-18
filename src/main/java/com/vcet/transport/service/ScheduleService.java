package com.vcet.transport.service;

import com.vcet.transport.model.Bus;
import com.vcet.transport.model.Route;
import com.vcet.transport.model.Schedule;
import com.vcet.transport.repository.BusRepository;
import com.vcet.transport.repository.RouteRepository;
import com.vcet.transport.repository.ScheduleRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;
import java.util.Optional;

@Service
public class ScheduleService {

    private final ScheduleRepository scheduleRepository;
    private final BusRepository busRepository;
    private final RouteRepository routeRepository;

    public ScheduleService(ScheduleRepository scheduleRepository, BusRepository busRepository, RouteRepository routeRepository) {
        this.scheduleRepository = scheduleRepository;
        this.busRepository = busRepository;
        this.routeRepository = routeRepository;
    }

    public List<Schedule> getAllUpcomingSchedules() {
        return scheduleRepository.findByTravelDateGreaterThanEqualOrderByTravelDateAscDepartureTimeAsc(LocalDate.now());
    }

    public List<Schedule> searchSchedules(String source, String destination, LocalDate date) {
        if (date == null) {
            date = LocalDate.now();
        }
        if (source == null || source.trim().isEmpty() || destination == null || destination.trim().isEmpty()) {
            return getAllUpcomingSchedules();
        }
        return scheduleRepository.searchSchedules(source.trim(), destination.trim(), date);
    }

    public Optional<Schedule> getScheduleById(Long id) {
        return scheduleRepository.findById(id);
    }

    public Schedule createSchedule(Long busId, Long routeId, LocalDate travelDate, LocalTime departureTime, LocalTime arrivalTime, double baseFare) {
        Bus bus = busRepository.findById(busId)
                .orElseThrow(() -> new IllegalArgumentException("Bus not found with ID: " + busId));
        Route route = routeRepository.findById(routeId)
                .orElseThrow(() -> new IllegalArgumentException("Route not found with ID: " + routeId));

        Schedule schedule = new Schedule(bus, route, travelDate, departureTime, arrivalTime, baseFare);
        return scheduleRepository.save(schedule);
    }
}
