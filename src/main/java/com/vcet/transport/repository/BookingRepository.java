package com.vcet.transport.repository;

import com.vcet.transport.model.Booking;
import com.vcet.transport.model.BookingStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {
    Optional<Booking> findByPnrNumber(String pnrNumber);
    List<Booking> findByScheduleIdAndStatus(Long scheduleId, BookingStatus status);

    @Query("SELECT b FROM Booking b ORDER BY b.bookingTime DESC")
    List<Booking> findAllRecentBookings();
}
