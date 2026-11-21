# SYSTEM DESIGN AND ARCHITECTURAL DIAGRAMS
## Public Transport Management and Passenger Travel Analysis System

---

### **ACADEMIC ASSESSMENT DETAILS**
- **Institution:** Velalar College of Engineering and Technology (Autonomous), Erode – 638012
- **Department:** Department of Information Technology
- **Course Title & Code:** Software Engineering (25ITT33)
- **Student Name:** Jeffrin
- **Register Number:** 732925ITR040
- **Class:** 25IT3A
- **Scenario:** Scenario 10 – Public Transport Management and Passenger Travel Analysis System

---

## 1. SYSTEM ARCHITECTURE DIAGRAM

The overall system architecture follows a modern **Multi-Tiered Layered Architecture** with distinct presentation, business service, data persistence, and data science analytical layers.

```mermaid
flowchart TD
    subgraph ClientLayer ["1. Client / Presentation Layer"]
        Browser["Desktop & Mobile Web Browser"]
        UI_Home["Bus Search & Discovery View"]
        UI_Seat["Interactive Seat Layout Selector"]
        UI_Ticket["Ticket Download & PNR Lookup"]
        UI_Admin["Admin Management Console"]
        UI_BI["BI Visual Analytics Dashboard"]
    end

    subgraph AppLayer ["2. Application / Business Logic Layer (Java 17 / Spring Boot)"]
        Controller["REST & Page Controllers<br/>(Booking, Admin, Report, Page)"]
        Security["Input Sanitization & Validation Layer"]
        subgraph Services ["Service Core (Multithreaded / Synchronized)"]
            BookingSvc["BookingService (Synchronized / Capacity Control)"]
            BusSvc["BusService & RouteService"]
            ScheduleSvc["ScheduleService (Fare & Inventory Engine)"]
            ReportSvc["ReportService (Revenue & Occupancy Metrics)"]
        end
        Repo["Data Access Layer<br/>(Spring Data JPA Repositories)"]
    end

    subgraph DataLayer ["3. Relational Persistence Layer (PostgreSQL)"]
        DB[(PostgreSQL Database)]
        Tables["Tables: buses, routes, schedules,<br/>passengers, bookings, tickets"]
        Triggers["Triggers: Update Seat Count,<br/>Views: revenue_summary_view"]
    end

    subgraph AnalyticsLayer ["4. Data Science & Visualizations Layer (Python 3.x)"]
        PythonScript["passenger_travel_analysis.py<br/>& Jupyter Notebook"]
        PandasEngine["Pandas & NumPy<br/>Data Cleaning & Feature Engineering"]
        Charts["Matplotlib & Seaborn Visualizations<br/>(Bar, Pie, Heatmaps, Trends)"]
    end

    Browser --> UI_Home & UI_Seat & UI_Ticket & UI_Admin & UI_BI
    UI_Home & UI_Seat & UI_Ticket & UI_Admin & UI_BI --> Controller
    Controller --> Security --> Services
    Services --> Repo --> DB
    DB --> Tables & Triggers
    DB -.->|ETL Query / Data Extraction| PythonScript
    PythonScript --> PandasEngine --> Charts
    Charts -.->|Embed Generated Charts| UI_BI
```

---

## 2. USE CASE DIAGRAM

The Use Case Diagram defines the primary actors (**Passenger / Commuter**, **Transport Administrator**, and **Data Analyst**) and their operational interactions with the system.

```mermaid
flowchart LR
    Passenger(("Passenger / Commuter"))
    Admin(("Transport Admin"))
    Analyst(("Data Analyst"))

    subgraph SystemBoundary ["Public Transport Management System"]
        UC1["Search Buses by Route & Date"]
        UC2["View Real-Time Seat Availability"]
        UC3["Select Seat & Reserve Ticket"]
        UC4["Download E-Ticket & PNR Receipt"]
        UC5["Cancel Ticket & Release Seat"]
        UC6["Track PNR Booking Status"]
        
        UC7["Add / Modify Bus Fleet Details"]
        UC8["Manage Transit Corridors & Routes"]
        UC9["Schedule Bus Trips & Set Fares"]
        UC10["Generate Revenue & Occupancy Reports"]
        UC11["View Passenger Manifest Lists"]
        
        UC12["Extract Transit Data via Python"]
        UC13["Preprocess & Clean Dataset"]
        UC14["Generate Seaborn / Matplotlib Visualizations"]
    end

    Passenger --> UC1
    Passenger --> UC2
    Passenger --> UC3
    Passenger --> UC4
    Passenger --> UC5
    Passenger --> UC6

    Admin --> UC7
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10
    Admin --> UC11

    Analyst --> UC12
    Analyst --> UC13
    Analyst --> UC14
```

---

## 3. CLASS DIAGRAM

The Class Diagram illustrates the object-oriented structure implemented in the Java backend (Unit 1 to Unit 5 of the Java Programming syllabus), showcasing classes, attributes, methods, relationships, and inheritance.

```mermaid
classDiagram
    direction TB

    class BusType {
        <<enumeration>>
        AC_SLEEPER
        SEMI_SLEEPER
        ULTRA_DELUXE
        NON_AC_SEATER
    }

    class BookingStatus {
        <<enumeration>>
        CONFIRMED
        CANCELLED
        PENDING
    }

    class Vehicle {
        <<abstract>>
        #Long id
        #String registrationNumber
        #int capacity
        +getRegistrationNumber() String
        +getCapacity() int
    }

    class Bus {
        -String busNumber
        -BusType busType
        -String operatorName
        -boolean isActive
        +getBusNumber() String
        +getBusType() BusType
        +setCapacity(int capacity) void
    }

    class Route {
        -Long id
        -String sourceCity
        -String destinationCity
        -double distanceKm
        -int estimatedMinutes
        +getRouteSummary() String
        +getDistanceKm() double
    }

    class Schedule {
        -Long id
        -Bus bus
        -Route route
        -LocalDate travelDate
        -LocalTime departureTime
        -LocalTime arrivalTime
        -double baseFare
        -int availableSeats
        +decreaseAvailableSeats(int count) boolean
        +increaseAvailableSeats(int count) void
        +isSeatAvailable() boolean
    }

    class Passenger {
        -Long id
        -String fullName
        -int age
        -String gender
        -String phoneNumber
        -String email
        +getContactDetails() String
    }

    class Booking {
        -Long id
        -String pnrNumber
        -Schedule schedule
        -Passenger passenger
        -LocalDateTime bookingTime
        -double totalAmount
        -BookingStatus status
        -List~Ticket~ tickets
        +confirmBooking() void
        +cancelBooking() void
    }

    class Ticket {
        -Long id
        -String ticketNumber
        -Booking booking
        -int seatNumber
        -double fare
        -String status
        +getSeatNumber() int
        +markAsCancelled() void
    }

    class BookingService {
        <<interface>>
        +createBooking(BookingRequest req) Booking
        +cancelBooking(String pnr) boolean
        +getSeatAvailability(Long scheduleId) List~Integer~
    }

    class BookingServiceImpl {
        -BookingRepository bookingRepo
        -ScheduleRepository scheduleRepo
        -TicketRepository ticketRepo
        +synchronized createBooking(BookingRequest req) Booking
        +synchronized cancelBooking(String pnr) boolean
    }

    Vehicle <|-- Bus : extends (Inheritance)
    Bus --> BusType : has
    Schedule --> Bus : assigned to
    Schedule --> Route : operates on
    Booking --> Schedule : books for
    Booking --> Passenger : made by
    Booking --> BookingStatus : has state
    Booking "1" *-- "many" Ticket : aggregates
    BookingService <|.. BookingServiceImpl : implements
```

---

## 4. COMPONENT DIAGRAM

The UML Component Diagram describes the organization and wiring of the physical components across the presentation, application, data, and analytics subsystems.

```mermaid
flowchart TD
    subgraph PkgPresentation ["Package: 1. Client & Presentation Tier"]
        WebUI["«component»<br/><b>Web Browser UI Component</b><br/>(HTML5 / Tailwind CSS / Vanilla JS)"]
        SeatUI["«component»<br/><b>Interactive Seat Grid Component</b>"]
        ChartUI["«component»<br/><b>Chart.js BI Visualizer Component</b>"]
    end

    subgraph PkgApp ["Package: 2. Application Tier (Spring Boot / Java 17)"]
        Controllers["«component»<br/><b>REST API Controller Component</b>"]
        Validator["«component»<br/><b>Validation & Security Component</b>"]
        BookingSvc["«component»<br/><b>Booking Service Component</b><br/>(Synchronized Concurrency Lock)"]
        FleetSvc["«component»<br/><b>Fleet & Route Management Component</b>"]
        ReportSvc["«component»<br/><b>Reporting & Aggregation Component</b>"]
        JPA["«component»<br/><b>Spring Data JPA Component</b>"]
    end

    subgraph PkgDB ["Package: 3. Relational Persistence Tier"]
        DB[("«database»<br/><b>PostgreSQL Relational DB</b><br/>(buses, routes, schedules, bookings, tickets)")]
        DBInspector["«component»<br/><b>Database Table Inspector Component</b>"]
    end

    subgraph PkgAnalytics ["Package: 4. Data Science Subsystem"]
        PyScript["«component»<br/><b>Python Analytics Script</b><br/>(passenger_travel_analysis.py)"]
        PyEngine["«component»<br/><b>Pandas & Seaborn Engine</b>"]
        Visuals["«artifact»<br/><b>Generated Visualizations (7 PNGs)</b>"]
    end

    WebUI -->|HTTP REST / JSON| Controllers
    SeatUI -->|Query Seats| Controllers
    ChartUI -->|Fetch Metrics| Controllers

    Controllers --> Validator
    Validator --> BookingSvc
    Validator --> FleetSvc
    Controllers --> ReportSvc
    Controllers --> DBInspector

    BookingSvc --> JPA
    FleetSvc --> JPA
    ReportSvc --> JPA
    DBInspector --> JPA

    JPA -->|JDBC Connection Pool| DB
    DB -.->|Data Extraction| PyScript
    PyScript --> PyEngine
    PyEngine --> Visuals
```

---

## 5. SEQUENCE DIAGRAM: TICKET BOOKING & OVERBOOKING PREVENTION

This sequence diagram depicts the **multithreaded synchronized transaction** workflow when a passenger books a ticket, highlighting race-condition prevention and atomic seat decrement.

```mermaid
sequenceDiagram
    autonumber
    actor Passenger as Commuter
    participant UI as Web Frontend (UI)
    participant Controller as BookingController
    participant Service as BookingServiceImpl (Synchronized)
    participant ScheduleRepo as ScheduleRepository
    participant DB as PostgreSQL Database
    participant TicketRepo as TicketRepository

    Passenger->>UI: Select Bus Schedule & Click Seat #14
    UI->>Controller: POST /api/bookings (ScheduleId, Seat #14, Passenger Details)
    Controller->>Service: createBooking(bookingRequest)
    
    activate Service
    Note over Service: Synchronized Execution Block<br/>(Prevents Concurrency Race Conditions)
    
    Service->>ScheduleRepo: findScheduleByIdWithPessimisticLock(scheduleId)
    ScheduleRepo->>DB: SELECT * FROM schedules WHERE id = ? FOR UPDATE
    DB-->>ScheduleRepo: Return locked schedule record
    ScheduleRepo-->>Service: Schedule object (availableSeats: 3)

    alt availableSeats > 0 AND seat #14 is unreserved
        Service->>DB: INSERT INTO passengers (name, age, phone, email) VALUES (...)
        Service->>DB: INSERT INTO bookings (pnr, schedule_id, total_amount, status) VALUES (...)
        Service->>TicketRepo: save(Ticket #14, status: 'CONFIRMED')
        TicketRepo->>DB: INSERT INTO tickets (seat_number, status, booking_id) VALUES (...)
        Service->>ScheduleRepo: update available_seats = available_seats - 1
        ScheduleRepo->>DB: UPDATE schedules SET available_seats = available_seats - 1
        Service-->>Controller: Return Confirmed Booking with PNR
        Controller-->>UI: 200 OK (Booking Confirmation + E-Ticket Data)
        UI-->>Passenger: Display Booking Success & Download Ticket PDF
    else availableSeats == 0 OR Seat Already Reserved
        Service-->>Controller: Throw OverbookingException / SeatNotAvailableException
        Controller-->>UI: 409 Conflict ("Selected seat is already booked")
        UI-->>Passenger: Show Alert ("Seat unavailable. Please select another seat.")
    end
    deactivate Service
```

---

## 6. SEQUENCE DIAGRAM: TICKET CANCELLATION & SEAT RELEASE

```mermaid
sequenceDiagram
    autonumber
    actor Passenger as Commuter
    participant UI as Web Frontend (UI)
    participant Controller as BookingController
    participant Service as BookingServiceImpl
    participant DB as PostgreSQL Database

    Passenger->>UI: Enter PNR (e.g., TCK-2026-0042) & Click Cancel
    UI->>Controller: POST /api/bookings/cancel/{pnr}
    Controller->>Service: cancelBooking(pnr)
    
    activate Service
    Service->>DB: SELECT * FROM bookings WHERE pnr = ? FOR UPDATE
    DB-->>Service: Return Booking record (status: 'CONFIRMED')
    
    Service->>DB: UPDATE bookings SET status = 'CANCELLED' WHERE pnr = ?
    Service->>DB: UPDATE tickets SET status = 'CANCELLED' WHERE booking_id = ?
    Service->>DB: UPDATE schedules SET available_seats = available_seats + 1 WHERE id = ?
    
    Service-->>Controller: Success (Booking Cancelled & Seat Released)
    deactivate Service
    
    Controller-->>UI: 200 OK (Cancellation Receipt + Refund Notice)
    UI-->>Passenger: "Booking cancelled successfully. Seat #14 released back to inventory."
```

---

## 7. ACTIVITY DIAGRAM: END-TO-END PASSENGER BOOKING WORKFLOW

```mermaid
flowchart TD
    Start([Passenger Opens Transport Portal]) --> Search[Enter Origin, Destination & Travel Date]
    Search --> QueryDB[Query Available Bus Schedules]
    QueryDB --> CheckRoutes{Schedules Found?}
    CheckRoutes -- No --> DisplayEmpty[Display 'No Buses Found for this Date']
    DisplayEmpty --> Search
    CheckRoutes -- Yes --> DisplayList[Display Matching Bus Cards & Fares]
    DisplayList --> SelectBus[Select Preferred Bus & Click 'View Seats']
    SelectBus --> LoadGrid[Fetch Live Seat Matrix]
    LoadGrid --> PickSeat[Click Desired Seat]
    PickSeat --> FillForm[Enter Passenger Details: Name, Age, Phone, Email]
    FillForm --> SubmitBooking[Click 'Confirm & Reserve Ticket']
    SubmitBooking --> LockTransaction[Acquire Synchronized Transaction Lock]
    LockTransaction --> CheckAvailable{Is Selected Seat Free & Capacity > 0?}
    CheckAvailable -- No --> AlertError[Show Error: 'Seat Already Booked by Another User']
    AlertError --> LoadGrid
    CheckAvailable -- Yes --> DeductSeat[Decrement Schedule Available Seats]
    DeductSeat --> SaveRecords[Persist Passenger, Booking & Ticket Records]
    SaveRecords --> CommitTx[Commit Database Transaction & Release Lock]
    CommitTx --> GeneratePNR[Generate Unique PNR & Ticket Receipt]
    GeneratePNR --> End([Passenger Views Confirmed Ticket & Downloads Receipt])
```
