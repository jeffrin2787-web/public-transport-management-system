package com.vcet.transport.repository;

import com.vcet.transport.model.Schedule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface ScheduleRepository extends JpaRepository<Schedule, Long> {

    @Query("SELECT s FROM Schedule s WHERE LOWER(s.route.sourceCity) = LOWER(:source) " +
           "AND LOWER(s.route.destinationCity) = LOWER(:destination) " +
           "AND s.travelDate >= :date AND s.status = 'SCHEDULED' " +
           "ORDER BY s.travelDate ASC, s.departureTime ASC")
    List<Schedule> searchSchedules(
            @Param("source") String source,
            @Param("destination") String destination,
            @Param("date") LocalDate date
    );

    List<Schedule> findByTravelDateGreaterThanEqualOrderByTravelDateAscDepartureTimeAsc(LocalDate date);
}
