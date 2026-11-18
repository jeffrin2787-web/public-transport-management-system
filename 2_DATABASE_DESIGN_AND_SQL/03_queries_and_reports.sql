-- ============================================================================
-- SQL QUERIES AND REPORT SCRIPTS
-- PROJECT: Public Transport Management and Passenger Travel Analysis System
-- INSTITUTION: Velalar College of Engineering and Technology, Erode - 12
-- STUDENT: Jeffrin (Reg No: 732925ITR040) | CLASS: 25IT3A
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1: Route-Wise Total Revenue Generation (Ranked by Revenue)
-- Demonstrates: Joins, Aggregation (SUM), GROUP BY, ORDER BY
-- ----------------------------------------------------------------------------
SELECT 
    r.route_id,
    r.source_city || ' -> ' || r.destination_city AS route_name,
    r.distance_km,
    COUNT(DISTINCT b.booking_id) AS total_bookings,
    COUNT(t.ticket_id) AS total_passengers_carried,
    COALESCE(SUM(t.seat_fare), 0.00) AS total_revenue_inr
FROM routes r
JOIN schedules s ON r.route_id = s.route_id
JOIN bookings b ON s.schedule_id = b.schedule_id AND b.status = 'CONFIRMED'
JOIN tickets t ON b.booking_id = t.booking_id AND t.status = 'CONFIRMED'
GROUP BY r.route_id, r.source_city, r.destination_city, r.distance_km
ORDER BY total_revenue_inr DESC;

-- ----------------------------------------------------------------------------
-- QUERY 2: Bus Occupancy Rate Analysis per Scheduled Trip
-- Demonstrates: Mathematical calculation, Type casting, Percentages
-- ----------------------------------------------------------------------------
SELECT 
    s.schedule_id,
    b.bus_number,
    b.bus_type,
    r.source_city || ' to ' || r.destination_city AS corridor,
    s.travel_date,
    s.departure_time,
    b.total_capacity,
    (b.total_capacity - s.available_seats) AS booked_seats,
    s.available_seats,
    ROUND(((b.total_capacity - s.available_seats)::numeric / b.total_capacity) * 100, 2) AS occupancy_percentage
FROM schedules s
JOIN buses b ON s.bus_id = b.bus_id
JOIN routes r ON s.route_id = r.route_id
ORDER BY occupancy_percentage DESC;

-- ----------------------------------------------------------------------------
-- QUERY 3: Passenger Manifest for a Specific Bus Schedule (e.g., Schedule #1)
-- Demonstrates: Multi-table joins across 5 tables, ORDER BY seat number
-- ----------------------------------------------------------------------------
SELECT 
    t.seat_number,
    p.full_name AS passenger_name,
    p.age,
    p.gender,
    p.phone_number,
    b.pnr_number,
    t.ticket_number,
    t.seat_fare,
    t.status AS ticket_status
FROM tickets t
JOIN bookings b ON t.booking_id = b.booking_id
JOIN passengers p ON b.passenger_id = p.passenger_id
WHERE b.schedule_id = 1
ORDER BY t.seat_number ASC;

-- ----------------------------------------------------------------------------
-- QUERY 4: Peak Travel Hours & Departure Distribution
-- Demonstrates: EXTRACT(HOUR ...), Date/Time Functions
-- ----------------------------------------------------------------------------
SELECT 
    EXTRACT(HOUR FROM s.departure_time) AS departure_hour_24h,
    COUNT(s.schedule_id) AS scheduled_departures_count,
    COUNT(t.ticket_id) AS total_seats_booked,
    COALESCE(SUM(t.seat_fare), 0) AS total_fare_revenue
FROM schedules s
LEFT JOIN bookings b ON s.schedule_id = b.schedule_id AND b.status = 'CONFIRMED'
LEFT JOIN tickets t ON b.booking_id = t.booking_id AND t.status = 'CONFIRMED'
GROUP BY departure_hour_24h
ORDER BY departure_hour_24h ASC;

-- ----------------------------------------------------------------------------
-- QUERY 5: Bus Fleet Utilization and Fleet Performance
-- Demonstrates: Subqueries, HAVING clause, CASE expressions
-- ----------------------------------------------------------------------------
SELECT 
    b.bus_number,
    b.bus_type,
    b.operator_name,
    COUNT(DISTINCT s.schedule_id) AS total_trips_assigned,
    COUNT(t.ticket_id) AS total_tickets_sold,
    COALESCE(SUM(t.seat_fare), 0) AS gross_revenue_generated,
    CASE 
        WHEN COUNT(t.ticket_id) >= 10 THEN 'High Demand Asset'
        WHEN COUNT(t.ticket_id) BETWEEN 5 AND 9 THEN 'Moderate Demand Asset'
        ELSE 'Underutilized'
    END AS asset_utilization_tier
FROM buses b
LEFT JOIN schedules s ON b.bus_id = s.bus_id
LEFT JOIN bookings bkg ON s.schedule_id = bkg.schedule_id AND bkg.status = 'CONFIRMED'
LEFT JOIN tickets t ON bkg.booking_id = t.booking_id AND t.status = 'CONFIRMED'
GROUP BY b.bus_id, b.bus_number, b.bus_type, b.operator_name
ORDER BY gross_revenue_generated DESC;

-- ----------------------------------------------------------------------------
-- QUERY 6: Cancellation Rate Analysis
-- Demonstrates: Ratio computations, Conditional aggregations
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(b.booking_id) AS total_booking_requests,
    COUNT(CASE WHEN b.status = 'CONFIRMED' THEN 1 END) AS confirmed_bookings,
    COUNT(CASE WHEN b.status = 'CANCELLED' THEN 1 END) AS cancelled_bookings,
    ROUND(
        (COUNT(CASE WHEN b.status = 'CANCELLED' THEN 1 END)::numeric / NULLIF(COUNT(b.booking_id), 0)) * 100, 
        2
    ) AS cancellation_rate_percentage
FROM bookings b;
