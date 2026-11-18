-- ============================================================================
-- DATABASE TRIGGERS, STORED PROCEDURES, AND VIEWS
-- PROJECT: Public Transport Management and Passenger Travel Analysis System
-- INSTITUTION: Velalar College of Engineering and Technology, Erode - 12
-- STUDENT: Jeffrin (Reg No: 732925ITR040) | CLASS: 25IT3A
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. VIEW: vw_route_revenue_summary
-- Provides consolidated financial metrics per corridor
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_route_revenue_summary AS
SELECT 
    r.route_id,
    r.source_city,
    r.destination_city,
    r.source_city || ' - ' || r.destination_city AS route_name,
    r.distance_km,
    COUNT(DISTINCT b.booking_id) AS total_confirmed_bookings,
    COUNT(t.ticket_id) AS total_passengers_booked,
    COALESCE(SUM(t.seat_fare), 0.00) AS total_revenue_generated
FROM routes r
LEFT JOIN schedules s ON r.route_id = s.route_id
LEFT JOIN bookings b ON s.schedule_id = b.schedule_id AND b.status = 'CONFIRMED'
LEFT JOIN tickets t ON b.booking_id = t.booking_id AND t.status = 'CONFIRMED'
GROUP BY r.route_id, r.source_city, r.destination_city, r.distance_km;

-- ----------------------------------------------------------------------------
-- 2. VIEW: vw_schedule_occupancy
-- Real-time seat occupancy and load factor view
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_schedule_occupancy AS
SELECT 
    s.schedule_id,
    b.bus_number,
    b.bus_type,
    r.source_city,
    r.destination_city,
    s.travel_date,
    s.departure_time,
    s.arrival_time,
    s.base_fare,
    b.total_capacity,
    (b.total_capacity - s.available_seats) AS occupied_seats,
    s.available_seats,
    ROUND(((b.total_capacity - s.available_seats)::numeric / b.total_capacity) * 100, 2) AS occupancy_percentage
FROM schedules s
JOIN buses b ON s.bus_id = b.bus_id
JOIN routes r ON s.route_id = r.route_id;

-- ----------------------------------------------------------------------------
-- 3. TRIGGER FUNCTION: trg_update_seats_on_booking()
-- Enforces capacity constraint and prevents overbooking
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trg_update_seats_on_booking()
RETURNS TRIGGER AS $$
DECLARE
    current_avail INT;
BEGIN
    -- Check available seats on the schedule
    SELECT available_seats INTO current_avail 
    FROM schedules 
    WHERE schedule_id = NEW.schedule_id;

    IF current_avail <= 0 THEN
        RAISE EXCEPTION 'OVERBOOKING ERROR: No seats remaining for schedule ID %', NEW.schedule_id;
    END IF;

    -- Decrement available seats by 1
    UPDATE schedules 
    SET available_seats = available_seats - 1 
    WHERE schedule_id = NEW.schedule_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ----------------------------------------------------------------------------
-- 4. TRIGGER FUNCTION: trg_release_seats_on_cancellation()
-- Restores available seat inventory when booking is cancelled
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trg_release_seats_on_cancellation()
RETURNS TRIGGER AS $$
DECLARE
    ticket_count INT;
BEGIN
    IF OLD.status = 'CONFIRMED' AND NEW.status = 'CANCELLED' THEN
        -- Count how many tickets belong to this booking
        SELECT COUNT(*) INTO ticket_count 
        FROM tickets 
        WHERE booking_id = NEW.booking_id AND status = 'CONFIRMED';

        -- Update tickets to CANCELLED
        UPDATE tickets 
        SET status = 'CANCELLED' 
        WHERE booking_id = NEW.booking_id;

        -- Return seats to the schedule
        UPDATE schedules 
        SET available_seats = available_seats + ticket_count 
        WHERE schedule_id = NEW.schedule_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to bookings table for cancellations
DROP TRIGGER IF EXISTS trigger_booking_cancellation ON bookings;
CREATE TRIGGER trigger_booking_cancellation
AFTER UPDATE OF status ON bookings
FOR EACH ROW
EXECUTE FUNCTION trg_release_seats_on_cancellation();
