-- ============================================================================
-- SEED DATA INSERTION SCRIPT (DML)
-- PROJECT: Public Transport Management and Passenger Travel Analysis System
-- REALISTIC TAMIL NADU & SOUTH INDIA TRANSIT NETWORK
-- VCET REGIONAL HUB: Erode, Coimbatore, Salem, Tirupur, Chennai, Bangalore, Madurai
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. SEED BUSES (Fleet Assets)
-- ----------------------------------------------------------------------------
INSERT INTO buses (bus_id, bus_number, bus_type, total_capacity, operator_name, is_active) VALUES
(1, 'TN-33-N-2410', 'AC_SLEEPER', 30, 'Kongu Express Transport', true),
(2, 'TN-33-N-2845', 'SEMI_SLEEPER', 36, 'Kongu Express Transport', true),
(3, 'TN-38-N-3120', 'ULTRA_DELUXE', 40, 'Cheran Line Transits', true),
(4, 'TN-27-N-1890', 'AC_SLEEPER', 30, 'Salem City Express', true),
(5, 'TN-01-AN-6701', 'SEMI_SLEEPER', 36, 'SETC Platinum Express', true),
(6, 'TN-58-N-4422', 'ULTRA_DELUXE', 40, 'Pandian Royal Route', true),
(7, 'TN-45-N-5110', 'NON_AC_SEATER', 45, 'Cholan Intercity Direct', true),
(8, 'TN-43-N-1008', 'AC_SLEEPER', 28, 'Nilgiri Mountain Rider', true),
(9, 'KA-01-F-8890', 'AC_SLEEPER', 32, 'Bangalore Silicon Cruiser', true),
(10, 'TN-39-N-3315', 'SEMI_SLEEPER', 36, 'Tirupur Knit City Express', true);

SELECT setval('buses_bus_id_seq', (SELECT MAX(bus_id) FROM buses));

-- ----------------------------------------------------------------------------
-- 2. SEED ROUTES (Corridors across Tamil Nadu & Bangalore)
-- ----------------------------------------------------------------------------
INSERT INTO routes (route_id, source_city, destination_city, distance_km, estimated_duration_minutes, is_active) VALUES
(1, 'Erode', 'Chennai Central', 420.00, 450, true),
(2, 'Chennai Central', 'Erode', 420.00, 450, true),
(3, 'Erode', 'Coimbatore', 100.50, 120, true),
(4, 'Coimbatore', 'Erode', 100.50, 120, true),
(5, 'Erode', 'Bengaluru', 260.00, 330, true),
(6, 'Bengaluru', 'Erode', 260.00, 330, true),
(7, 'Salem', 'Chennai Central', 345.00, 380, true),
(8, 'Coimbatore', 'Bengaluru', 360.00, 420, true),
(9, 'Erode', 'Madurai', 195.00, 240, true),
(10, 'Madurai', 'Erode', 195.00, 240, true),
(11, 'Erode', 'Tiruchirappalli', 145.00, 180, true),
(12, 'Coimbatore', 'Ooty', 85.00, 180, true);

SELECT setval('routes_route_id_seq', (SELECT MAX(route_id) FROM routes));

-- ----------------------------------------------------------------------------
-- 3. SEED SCHEDULES (Trips with Timings and Fares)
-- ----------------------------------------------------------------------------
INSERT INTO schedules (schedule_id, bus_id, route_id, travel_date, departure_time, arrival_time, base_fare, available_seats, status) VALUES
(1, 1, 1, CURRENT_DATE + INTERVAL '1 day', '21:30:00', '05:00:00', 750.00, 26, 'SCHEDULED'),
(2, 2, 1, CURRENT_DATE + INTERVAL '1 day', '22:15:00', '05:45:00', 550.00, 32, 'SCHEDULED'),
(3, 3, 3, CURRENT_DATE + INTERVAL '1 day', '07:00:00', '09:00:00', 120.00, 36, 'SCHEDULED'),
(4, 4, 5, CURRENT_DATE + INTERVAL '1 day', '23:00:00', '04:30:00', 650.00, 28, 'SCHEDULED'),
(5, 5, 2, CURRENT_DATE + INTERVAL '1 day', '22:00:00', '05:30:00', 550.00, 36, 'SCHEDULED'),
(6, 6, 9, CURRENT_DATE + INTERVAL '1 day', '14:30:00', '18:30:00', 250.00, 38, 'SCHEDULED'),
(7, 7, 11, CURRENT_DATE + INTERVAL '1 day', '08:00:00', '11:00:00', 160.00, 43, 'SCHEDULED'),
(8, 8, 12, CURRENT_DATE + INTERVAL '1 day', '06:30:00', '09:30:00', 320.00, 26, 'SCHEDULED'),
(9, 9, 8, CURRENT_DATE + INTERVAL '1 day', '22:45:00', '05:45:00', 800.00, 30, 'SCHEDULED'),
(10, 10, 3, CURRENT_DATE + INTERVAL '1 day', '17:30:00', '19:30:00', 140.00, 34, 'SCHEDULED'),
(11, 1, 1, CURRENT_DATE + INTERVAL '2 day', '21:30:00', '05:00:00', 750.00, 30, 'SCHEDULED'),
(12, 4, 5, CURRENT_DATE + INTERVAL '2 day', '23:00:00', '04:30:00', 650.00, 30, 'SCHEDULED');

SELECT setval('schedules_schedule_id_seq', (SELECT MAX(schedule_id) FROM schedules));

-- ----------------------------------------------------------------------------
-- 4. SEED PASSENGERS
-- ----------------------------------------------------------------------------
INSERT INTO passengers (passenger_id, full_name, age, gender, phone_number, email) VALUES
(1, 'Jeffrin', 20, 'MALE', '9876543210', 'jeffrin@vcet.ac.in'),
(2, 'Anand Kumar', 28, 'MALE', '9842156789', 'anand.k@gmail.com'),
(3, 'Priya Dharshini', 24, 'FEMALE', '9789123456', 'priya.d@yahoo.com'),
(4, 'Karthik Raja', 32, 'MALE', '9443218765', 'karthik.r@live.com'),
(5, 'Deepa Mohan', 21, 'FEMALE', '9944556677', 'deepa.m@outlook.com'),
(6, 'Vigneshwaran S', 26, 'MALE', '9629112233', 'vignesh.s@gmail.com'),
(7, 'Soundarya Lakshmi', 29, 'FEMALE', '9500443322', 'soundarya@gmail.com'),
(8, 'Saravanan R', 45, 'MALE', '9442332211', 'saravanan.r@gmail.com');

SELECT setval('passengers_passenger_id_seq', (SELECT MAX(passenger_id) FROM passengers));

-- ----------------------------------------------------------------------------
-- 5. SEED BOOKINGS
-- ----------------------------------------------------------------------------
INSERT INTO bookings (booking_id, pnr_number, schedule_id, passenger_id, booking_time, total_amount, status, payment_status) VALUES
(1, 'TCK-2026-0001', 1, 1, CURRENT_TIMESTAMP - INTERVAL '2 hours', 1500.00, 'CONFIRMED', 'PAID'),
(2, 'TCK-2026-0002', 1, 2, CURRENT_TIMESTAMP - INTERVAL '3 hours', 1500.00, 'CONFIRMED', 'PAID'),
(3, 'TCK-2026-0003', 2, 3, CURRENT_TIMESTAMP - INTERVAL '4 hours', 1100.00, 'CONFIRMED', 'PAID'),
(4, 'TCK-2026-0004', 2, 4, CURRENT_TIMESTAMP - INTERVAL '5 hours', 1100.00, 'CONFIRMED', 'PAID'),
(5, 'TCK-2026-0005', 3, 5, CURRENT_TIMESTAMP - INTERVAL '6 hours', 480.00, 'CONFIRMED', 'PAID'),
(6, 'TCK-2026-0006', 4, 6, CURRENT_TIMESTAMP - INTERVAL '1 day', 1300.00, 'CONFIRMED', 'PAID'),
(7, 'TCK-2026-0007', 6, 7, CURRENT_TIMESTAMP - INTERVAL '1 day', 500.00, 'CONFIRMED', 'PAID'),
(8, 'TCK-2026-0008', 8, 8, CURRENT_TIMESTAMP - INTERVAL '1 day', 640.00, 'CONFIRMED', 'PAID'),
(9, 'TCK-2026-0009', 1, 3, CURRENT_TIMESTAMP - INTERVAL '2 days', 750.00, 'CANCELLED', 'REFUNDED');

SELECT setval('bookings_booking_id_seq', (SELECT MAX(booking_id) FROM bookings));

-- ----------------------------------------------------------------------------
-- 6. SEED TICKETS (Allocated Seats)
-- ----------------------------------------------------------------------------
INSERT INTO tickets (ticket_id, ticket_number, booking_id, seat_number, seat_fare, status) VALUES
(1, 'T-0001-S01', 1, 1, 750.00, 'CONFIRMED'),
(2, 'T-0001-S02', 1, 2, 750.00, 'CONFIRMED'),
(3, 'T-0002-S03', 2, 3, 750.00, 'CONFIRMED'),
(4, 'T-0002-S04', 2, 4, 750.00, 'CONFIRMED'),
(5, 'T-0003-S05', 3, 5, 550.00, 'CONFIRMED'),
(6, 'T-0003-S06', 3, 6, 550.00, 'CONFIRMED'),
(7, 'T-0004-S07', 4, 7, 550.00, 'CONFIRMED'),
(8, 'T-0004-S08', 4, 8, 550.00, 'CONFIRMED'),
(9, 'T-0005-S01', 5, 1, 120.00, 'CONFIRMED'),
(10, 'T-0005-S02', 5, 2, 120.00, 'CONFIRMED'),
(11, 'T-0005-S03', 5, 3, 120.00, 'CONFIRMED'),
(12, 'T-0005-S04', 5, 4, 120.00, 'CONFIRMED'),
(13, 'T-0006-S11', 6, 11, 650.00, 'CONFIRMED'),
(14, 'T-0006-S12', 6, 12, 650.00, 'CONFIRMED'),
(15, 'T-0007-S15', 7, 15, 250.00, 'CONFIRMED'),
(16, 'T-0007-S16', 7, 16, 250.00, 'CONFIRMED'),
(17, 'T-0008-S01', 8, 1, 320.00, 'CONFIRMED'),
(18, 'T-0008-S02', 8, 2, 320.00, 'CONFIRMED'),
(19, 'T-0009-S09', 9, 9, 750.00, 'CANCELLED');

SELECT setval('tickets_ticket_id_seq', (SELECT MAX(ticket_id) FROM tickets));

-- End of 02_seed_data.sql
