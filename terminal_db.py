#!/usr/bin/env python3
"""
================================================================================
INTERACTIVE DATABASE TERMINAL & TABLE VIEWER
PROJECT: Public Transport Management and Passenger Travel Analysis System
VELALAR COLLEGE OF ENGINEERING AND TECHNOLOGY (AUTONOMOUS), ERODE - 638012
STUDENT: Jeffrin (Reg No: 732925ITR040) | CLASS: 25IT3A
================================================================================
This script executes real SQL queries and displays formatted relational tables
directly in the terminal console without needing external database servers.
================================================================================
"""

import sqlite3
import sys
import os

def create_and_seed_database():
    """Initializes an in-memory relational database with all 6 tables and Tamil Nadu transit seed data."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # 1. BUSES TABLE
    cursor.execute("""
    CREATE TABLE buses (
        bus_id INTEGER PRIMARY KEY,
        bus_number TEXT NOT NULL UNIQUE,
        bus_type TEXT NOT NULL,
        total_capacity INTEGER NOT NULL,
        operator_name TEXT DEFAULT 'Tamil Nadu State Express Transit',
        is_active INTEGER DEFAULT 1
    )
    """)
    buses_data = [
        (1, 'TN-33-N-2410', 'AC_SLEEPER', 30, 'Kongu Express Transport', 1),
        (2, 'TN-33-N-2845', 'SEMI_SLEEPER', 36, 'Kongu Express Transport', 1),
        (3, 'TN-38-N-3120', 'ULTRA_DELUXE', 40, 'Cheran Line Transits', 1),
        (4, 'TN-27-N-1890', 'AC_SLEEPER', 30, 'Salem City Express', 1),
        (5, 'TN-01-AN-6701', 'SEMI_SLEEPER', 36, 'SETC Platinum Express', 1),
        (6, 'TN-58-N-4422', 'ULTRA_DELUXE', 40, 'Pandian Royal Route', 1),
        (7, 'TN-45-N-5110', 'NON_AC_SEATER', 45, 'Cholan Intercity Direct', 1),
        (8, 'TN-43-N-1008', 'AC_SLEEPER', 28, 'Nilgiri Mountain Rider', 1)
    ]
    cursor.executemany("INSERT INTO buses VALUES (?, ?, ?, ?, ?, ?)", buses_data)

    # 2. ROUTES TABLE
    cursor.execute("""
    CREATE TABLE routes (
        route_id INTEGER PRIMARY KEY,
        source_city TEXT NOT NULL,
        destination_city TEXT NOT NULL,
        distance_km REAL NOT NULL,
        estimated_duration_minutes INTEGER NOT NULL,
        is_active INTEGER DEFAULT 1
    )
    """)
    routes_data = [
        (1, 'Erode', 'Chennai Central', 420.00, 450, 1),
        (2, 'Chennai Central', 'Erode', 420.00, 450, 1),
        (3, 'Erode', 'Coimbatore', 100.50, 120, 1),
        (4, 'Coimbatore', 'Erode', 100.50, 120, 1),
        (5, 'Erode', 'Bengaluru', 260.00, 330, 1),
        (6, 'Bengaluru', 'Erode', 260.00, 330, 1),
        (7, 'Salem', 'Chennai Central', 345.00, 380, 1),
        (8, 'Coimbatore', 'Bengaluru', 360.00, 420, 1),
        (9, 'Erode', 'Madurai', 195.00, 240, 1),
        (10, 'Erode', 'Tiruchirappalli', 145.00, 180, 1),
        (11, 'Coimbatore', 'Ooty', 85.00, 180, 1)
    ]
    cursor.executemany("INSERT INTO routes VALUES (?, ?, ?, ?, ?, ?)", routes_data)

    # 3. SCHEDULES TABLE
    cursor.execute("""
    CREATE TABLE schedules (
        schedule_id INTEGER PRIMARY KEY,
        bus_id INTEGER NOT NULL REFERENCES buses(bus_id),
        route_id INTEGER NOT NULL REFERENCES routes(route_id),
        travel_date TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        arrival_time TEXT NOT NULL,
        base_fare REAL NOT NULL,
        available_seats INTEGER NOT NULL,
        status TEXT DEFAULT 'SCHEDULED'
    )
    """)
    schedules_data = [
        (1, 1, 1, '2026-11-21', '21:30:00', '05:00:00', 750.00, 26, 'SCHEDULED'),
        (2, 2, 1, '2026-11-21', '22:15:00', '05:45:00', 550.00, 32, 'SCHEDULED'),
        (3, 3, 3, '2026-11-21', '07:00:00', '09:00:00', 120.00, 36, 'SCHEDULED'),
        (4, 4, 5, '2026-11-21', '23:00:00', '04:30:00', 650.00, 28, 'SCHEDULED'),
        (5, 5, 2, '2026-11-21', '22:00:00', '05:30:00', 550.00, 36, 'SCHEDULED'),
        (6, 6, 9, '2026-11-21', '14:30:00', '18:30:00', 250.00, 38, 'SCHEDULED'),
        (7, 8, 11, '2026-11-21', '06:30:00', '09:30:00', 320.00, 26, 'SCHEDULED')
    ]
    cursor.executemany("INSERT INTO schedules VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", schedules_data)

    # 4. PASSENGERS TABLE
    cursor.execute("""
    CREATE TABLE passengers (
        passenger_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT
    )
    """)
    passengers_data = [
        (1, 'Anand Kumar', 28, 'MALE', '9842156789', 'anand.k@gmail.com'),
        (2, 'Priya Dharshini', 24, 'FEMALE', '9789123456', 'priya.d@yahoo.com'),
        (3, 'Karthik Raja', 32, 'MALE', '9443218765', 'karthik.r@live.com'),
        (4, 'Deepa Mohan', 21, 'FEMALE', '9944556677', 'deepa.m@outlook.com'),
        (5, 'Vigneshwaran S', 26, 'MALE', '9629112233', 'vignesh.s@gmail.com'),
        (6, 'Soundarya Lakshmi', 29, 'FEMALE', '9500443322', 'soundarya@gmail.com'),
        (7, 'Saravanan R', 45, 'MALE', '9442332211', 'saravanan.r@gmail.com'),
        (8, 'Jeffrin', 20, 'MALE', '9876543210', 'jeffrin@gmail.com'),
        (9, 'Rio', 24, 'MALE', '6789054321', 'rio123@gmail.com')
    ]
    cursor.executemany("INSERT INTO passengers VALUES (?, ?, ?, ?, ?, ?)", passengers_data)

    # 5. BOOKINGS TABLE
    cursor.execute("""
    CREATE TABLE bookings (
        booking_id INTEGER PRIMARY KEY,
        pnr_number TEXT NOT NULL UNIQUE,
        schedule_id INTEGER NOT NULL REFERENCES schedules(schedule_id),
        passenger_id INTEGER NOT NULL REFERENCES passengers(passenger_id),
        booking_time TEXT NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT DEFAULT 'CONFIRMED',
        payment_status TEXT DEFAULT 'PAID'
    )
    """)
    bookings_data = [
        (1, 'TCK-2026-0001', 1, 1, '2026-11-20 09:30:00', 1500.00, 'CONFIRMED', 'PAID'),
        (2, 'TCK-2026-0002', 1, 2, '2026-11-20 10:15:00', 1500.00, 'CONFIRMED', 'PAID'),
        (3, 'TCK-2026-0003', 2, 3, '2026-11-20 11:00:00', 1100.00, 'CONFIRMED', 'PAID'),
        (4, 'TCK-2026-0004', 3, 4, '2026-11-20 11:45:00', 240.00, 'CONFIRMED', 'PAID'),
        (5, 'TCK-2026-0005', 4, 5, '2026-11-20 12:20:00', 1300.00, 'CONFIRMED', 'PAID'),
        (6, 'TCK-2026-0006', 1, 6, '2026-11-20 13:00:00', 750.00, 'CANCELLED', 'REFUNDED')
    ]
    cursor.executemany("INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?, ?, ?)", bookings_data)

    # 6. TICKETS TABLE
    cursor.execute("""
    CREATE TABLE tickets (
        ticket_id INTEGER PRIMARY KEY,
        ticket_number TEXT NOT NULL UNIQUE,
        booking_id INTEGER NOT NULL REFERENCES bookings(booking_id),
        seat_number INTEGER NOT NULL,
        seat_fare REAL NOT NULL,
        status TEXT DEFAULT 'CONFIRMED'
    )
    """)
    tickets_data = [
        (1, 'T-0001-S01', 1, 1, 750.00, 'CONFIRMED'),
        (2, 'T-0001-S02', 1, 2, 750.00, 'CONFIRMED'),
        (3, 'T-0002-S03', 2, 3, 750.00, 'CONFIRMED'),
        (4, 'T-0002-S04', 2, 4, 750.00, 'CONFIRMED'),
        (5, 'T-0003-S05', 3, 5, 550.00, 'CONFIRMED'),
        (6, 'T-0003-S06', 3, 6, 550.00, 'CONFIRMED'),
        (7, 'T-0004-S01', 4, 1, 120.00, 'CONFIRMED'),
        (8, 'T-0004-S02', 4, 2, 120.00, 'CONFIRMED'),
        (9, 'T-0005-S11', 5, 11, 650.00, 'CONFIRMED'),
        (10, 'T-0005-S12', 5, 12, 650.00, 'CONFIRMED'),
        (11, 'T-0006-S07', 6, 7, 750.00, 'CANCELLED')
    ]
    cursor.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)", tickets_data)

    # VIEWS
    cursor.execute("""
    CREATE VIEW vw_route_revenue_summary AS
    SELECT 
        r.route_id,
        r.source_city || ' -> ' || r.destination_city AS route_corridor,
        COUNT(DISTINCT b.booking_id) AS total_bookings,
        COUNT(t.ticket_id) AS total_passengers,
        COALESCE(SUM(t.seat_fare), 0.0) AS total_revenue
    FROM routes r
    LEFT JOIN schedules s ON r.route_id = s.route_id
    LEFT JOIN bookings b ON s.schedule_id = b.schedule_id AND b.status = 'CONFIRMED'
    LEFT JOIN tickets t ON b.booking_id = t.booking_id AND t.status = 'CONFIRMED'
    GROUP BY r.route_id, r.source_city, r.destination_city
    ORDER BY total_revenue DESC;
    """)

    conn.commit()
    return conn

def print_table(headers, rows, title=None):
    """Prints a beautifully aligned ASCII table with borders."""
    if title:
        print(f"\n=== {title.upper()} ===")
    
    if not rows:
        print("[No records found]")
        return

    # Convert all cells to strings
    str_rows = [[str(cell) if cell is not None else "NULL" for cell in row] for row in rows]
    str_headers = [str(h) for h in headers]

    # Calculate column widths
    col_widths = [len(h) for h in str_headers]
    for row in str_rows:
        for i, cell in enumerate(row):
            if len(cell) > col_widths[i]:
                col_widths[i] = len(cell)

    # Format helpers
    sep_border = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    header_line = "|" + "|".join([f" {h.ljust(col_widths[i])} " for i, h in enumerate(str_headers)]) + "|"

    print(sep_border)
    print(header_line)
    print(sep_border)
    for row in str_rows:
        row_line = "|" + "|".join([f" {row[i].ljust(col_widths[i])} " for i in range(len(row))]) + "|"
        print(row_line)
    print(sep_border)
    print(f"Total Rows: {len(rows)}\n")

def execute_query(conn, query, title="QUERY RESULT"):
    """Executes a SQL query and prints the formatted result table."""
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if cursor.description:
            headers = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            print_table(headers, rows, title=title)
        else:
            conn.commit()
            print(f"Query executed successfully. ({cursor.rowcount} rows affected)\n")
    except Exception as e:
        print(f"\n[SQL ERROR]: {e}\n")

def show_interactive_menu(conn):
    """Displays interactive CLI menu for student and faculty."""
    print("=" * 76)
    print("  PUBLIC TRANSPORT MANAGEMENT SYSTEM - DATABASE CONSOLE (VCET)")
    print("  Student: Jeffrin (Reg No: 732925ITR040) | Class: 25IT3A")
    print("  Department of Information Technology, VCET Erode - 12")
    print("=" * 76)
    print("  Available Relational Tables:")
    print("    1. buses        - Fleet assets and certified capacities")
    print("    2. routes       - Transit corridors across Tamil Nadu & Bangalore")
    print("    3. schedules    - Daily bus schedules, departure times & fares")
    print("    4. passengers   - Passenger directory (Name, Age, Gender, Phone)")
    print("    5. bookings     - Reservation transactions & PNR codes")
    print("    6. tickets      - Allocated seat numbers and fares")
    print("    7. all          - Display ALL 6 tables at once")
    print("    8. view         - Display pre-compiled view: vw_route_revenue_summary")
    print("    9. manifest     - Display Passenger Travel Manifest (Multi-Table JOIN)")
    print("    0. exit         - Close database console")
    print("=" * 76)

    table_map = {
        "1": "buses", "buses": "buses",
        "2": "routes", "routes": "routes",
        "3": "schedules", "schedules": "schedules",
        "4": "passengers", "passengers": "passengers",
        "5": "bookings", "bookings": "bookings",
        "6": "tickets", "tickets": "tickets"
    }

    while True:
        try:
            choice = input("Enter choice (1-9, table name, or SQL query) > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting database console. Goodbye!")
            break

        if not choice:
            continue

        if choice.lower() in ["0", "exit", "quit", "q"]:
            print("Exiting database console. Goodbye!")
            break

        if choice.lower() == "all" or choice == "7":
            for tbl in ["buses", "routes", "schedules", "passengers", "bookings", "tickets"]:
                execute_query(conn, f"SELECT * FROM {tbl}", title=f"TABLE: {tbl}")
            continue

        if choice.lower() == "view" or choice == "8":
            execute_query(conn, "SELECT * FROM vw_route_revenue_summary", title="VIEW: vw_route_revenue_summary")
            continue

        if choice.lower() == "manifest" or choice == "9":
            manifest_query = """
            SELECT 
                p.full_name AS passenger_name,
                p.phone_number,
                b.pnr_number,
                t.seat_number,
                r.source_city || ' -> ' || r.destination_city AS travel_route,
                t.seat_fare,
                t.status
            FROM passengers p
            JOIN bookings b ON p.passenger_id = b.passenger_id
            JOIN tickets t ON b.booking_id = t.booking_id
            JOIN schedules s ON b.schedule_id = s.schedule_id
            JOIN routes r ON s.route_id = r.route_id
            ORDER BY t.seat_number ASC;
            """
            execute_query(conn, manifest_query, title="PASSENGER TRAVEL MANIFEST (MULTI-TABLE JOIN)")
            continue

        if choice.lower() in table_map:
            tbl = table_map[choice.lower()]
            execute_query(conn, f"SELECT * FROM {tbl}", title=f"TABLE: {tbl}")
            continue

        # If user types raw SQL (e.g. SELECT * FROM ...)
        if any(choice.upper().startswith(kw) for kw in ["SELECT", "INSERT", "UPDATE", "DELETE", "PRAGMA", "SHOW"]):
            execute_query(conn, choice, title="SQL QUERY RESULT")
        else:
            print(f"[!] Unknown option '{choice}'. Enter 1-9, table name, or a SQL query.\n")

def main():
    conn = create_and_seed_database()

    # If arguments provided on command line (e.g., python terminal_db.py passengers)
    if len(sys.argv) > 1:
        arg = " ".join(sys.argv[1:]).strip()
        table_names = ["buses", "routes", "schedules", "passengers", "bookings", "tickets"]
        
        if arg.lower() in table_names:
            execute_query(conn, f"SELECT * FROM {arg}", title=f"TABLE: {arg}")
        elif arg.lower() == "all":
            for tbl in table_names:
                execute_query(conn, f"SELECT * FROM {tbl}", title=f"TABLE: {tbl}")
        elif arg.lower() == "manifest":
            manifest_query = """
            SELECT 
                p.full_name AS passenger_name,
                p.phone_number,
                b.pnr_number,
                t.seat_number,
                r.source_city || ' -> ' || r.destination_city AS travel_route,
                t.seat_fare,
                t.status
            FROM passengers p
            JOIN bookings b ON p.passenger_id = b.passenger_id
            JOIN tickets t ON b.booking_id = t.booking_id
            JOIN schedules s ON b.schedule_id = s.schedule_id
            JOIN routes r ON s.route_id = r.route_id
            ORDER BY t.seat_number ASC;
            """
            execute_query(conn, manifest_query, title="PASSENGER TRAVEL MANIFEST")
        else:
            execute_query(conn, arg, title="CUSTOM SQL QUERY RESULT")
    else:
        show_interactive_menu(conn)

if __name__ == "__main__":
    main()
