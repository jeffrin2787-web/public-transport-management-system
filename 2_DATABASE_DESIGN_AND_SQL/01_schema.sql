-- ============================================================================
-- DATABASE SCHEMA DEFINITION SCRIPT (DDL)
-- PROJECT: Public Transport Management and Passenger Travel Analysis System
-- INSTITUTION: Velalar College of Engineering and Technology, Erode - 12
-- STUDENT: Jeffrin (Reg No: 732925ITR040) | CLASS: 25IT3A
-- DATABASE: PostgreSQL (Compatible with Version 14+)
-- ============================================================================

-- Drop existing tables if re-running (respecting FK dependency order)
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS passengers CASCADE;
DROP TABLE IF EXISTS schedules CASCADE;
DROP TABLE IF EXISTS routes CASCADE;
DROP TABLE IF EXISTS buses CASCADE;

-- ----------------------------------------------------------------------------
-- 1. BUSES TABLE
-- Stores fleet assets, vehicle types, and certified seating capacities.
-- ----------------------------------------------------------------------------
CREATE TABLE buses (
    bus_id BIGSERIAL PRIMARY KEY,
    bus_number VARCHAR(20) NOT NULL UNIQUE,
    bus_type VARCHAR(30) NOT NULL,
    total_capacity INT NOT NULL,
    operator_name VARCHAR(100) DEFAULT 'Tamil Nadu State Express Transit',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_bus_capacity CHECK (total_capacity >= 10 AND total_capacity <= 60),
    CONSTRAINT chk_bus_type CHECK (bus_type IN ('AC_SLEEPER', 'SEMI_SLEEPER', 'ULTRA_DELUXE', 'NON_AC_SEATER'))
);

-- Index on bus_number for fast lookup
CREATE INDEX idx_bus_number ON buses(bus_number);

-- ----------------------------------------------------------------------------
-- 2. ROUTES TABLE
-- Stores transit corridors, source, destination, and distance in kilometers.
-- ----------------------------------------------------------------------------
CREATE TABLE routes (
    route_id BIGSERIAL PRIMARY KEY,
    source_city VARCHAR(50) NOT NULL,
    destination_city VARCHAR(50) NOT NULL,
    distance_km NUMERIC(6, 2) NOT NULL,
    estimated_duration_minutes INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_route_distance CHECK (distance_km > 0),
    CONSTRAINT chk_route_duration CHECK (estimated_duration_minutes > 0),
    CONSTRAINT uq_route_pair UNIQUE (source_city, destination_city)
);

-- Index on route search endpoints
CREATE INDEX idx_route_cities ON routes(source_city, destination_city);

-- ----------------------------------------------------------------------------
-- 3. SCHEDULES TABLE
-- Records bus trip assignments, travel dates, departure/arrival times, and fares.
-- ----------------------------------------------------------------------------
CREATE TABLE schedules (
    schedule_id BIGSERIAL PRIMARY KEY,
    bus_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    travel_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    base_fare NUMERIC(8, 2) NOT NULL,
    available_seats INT NOT NULL,
    status VARCHAR(20) DEFAULT 'SCHEDULED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_schedule_bus FOREIGN KEY (bus_id) REFERENCES buses(bus_id) ON DELETE CASCADE,
    CONSTRAINT fk_schedule_route FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE CASCADE,
    CONSTRAINT chk_base_fare CHECK (base_fare > 0),
    CONSTRAINT chk_available_seats CHECK (available_seats >= 0),
    CONSTRAINT chk_schedule_status CHECK (status IN ('SCHEDULED', 'DEPARTED', 'COMPLETED', 'CANCELLED'))
);

-- Composite index for fast passenger search queries
CREATE INDEX idx_schedules_search ON schedules(route_id, travel_date, status);

-- ----------------------------------------------------------------------------
-- 4. PASSENGERS TABLE
-- Stores passenger demographic and contact records.
-- ----------------------------------------------------------------------------
CREATE TABLE passengers (
    passenger_id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_passenger_age CHECK (age >= 1 AND age <= 120),
    CONSTRAINT chk_passenger_gender CHECK (gender IN ('MALE', 'FEMALE', 'OTHER'))
);

CREATE INDEX idx_passenger_phone ON passengers(phone_number);

-- ----------------------------------------------------------------------------
-- 5. BOOKINGS TABLE
-- Represents high-level transactions with unique PNR, total fare, and timestamps.
-- ----------------------------------------------------------------------------
CREATE TABLE bookings (
    booking_id BIGSERIAL PRIMARY KEY,
    pnr_number VARCHAR(30) NOT NULL UNIQUE,
    schedule_id BIGINT NOT NULL,
    passenger_id BIGINT NOT NULL,
    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'CONFIRMED',
    payment_status VARCHAR(20) DEFAULT 'PAID',
    CONSTRAINT fk_booking_schedule FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id) ON DELETE CASCADE,
    CONSTRAINT fk_booking_passenger FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id) ON DELETE CASCADE,
    CONSTRAINT chk_booking_amount CHECK (total_amount >= 0),
    CONSTRAINT chk_booking_status CHECK (status IN ('CONFIRMED', 'CANCELLED', 'PENDING')),
    CONSTRAINT chk_payment_status CHECK (payment_status IN ('PAID', 'REFUNDED', 'PENDING'))
);

CREATE INDEX idx_booking_pnr ON bookings(pnr_number);
CREATE INDEX idx_booking_schedule ON bookings(schedule_id);

-- ----------------------------------------------------------------------------
-- 6. TICKETS TABLE
-- Stores individual allocated seats for each passenger in a booking.
-- ----------------------------------------------------------------------------
CREATE TABLE tickets (
    ticket_id BIGSERIAL PRIMARY KEY,
    ticket_number VARCHAR(35) NOT NULL UNIQUE,
    booking_id BIGINT NOT NULL,
    seat_number INT NOT NULL,
    seat_fare NUMERIC(8, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'CONFIRMED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ticket_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE,
    CONSTRAINT chk_seat_number CHECK (seat_number >= 1),
    CONSTRAINT chk_seat_fare CHECK (seat_fare >= 0),
    CONSTRAINT chk_ticket_status CHECK (status IN ('CONFIRMED', 'CANCELLED'))
);

CREATE INDEX idx_ticket_booking ON tickets(booking_id);
CREATE INDEX idx_ticket_seat ON tickets(seat_number);

-- End of 01_schema.sql
