# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## Public Transport Management and Passenger Travel Analysis System

---

### **ACADEMIC ASSESSMENT DETAILS**
- **Institution:** Velalar College of Engineering and Technology (Autonomous), Erode – 638012
- **Department:** Department of Information Technology
- **Academic Year:** 2026–2027 (ODD Semester)
- **Class:** 25IT3A & B (Class: 25IT3A)
- **Course Title & Code:** Software Engineering (25ITT33) | Integrated Project Assessment
- **Student Name:** Jeffrin
- **Register Number:** 732925ITR040
- **Assigned Scenario:** Scenario 10 – Public Transport Management and Passenger Travel Analysis System (Register No: 10, 40, 70, 100)

---

## 1. INTRODUCTION

### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) document is to provide a complete, formal description of the **Public Transport Management and Passenger Travel Analysis System**. It details the functional and non-functional requirements, external interfaces, system domain constraints, database design dependencies, and analytical visualization components required for tracking bus transit, managing seat allocations, processing tickets, and evaluating passenger travel patterns.

### 1.2 Scope of the System
The system is an enterprise-grade web application with integrated relational database storage and Python-driven analytical capabilities:
1. **Bus & Fleet Management:** Maintenance of fleet assets (Bus Number, Registration, Type: AC Sleeper, Semi-Sleeper, Ultra Deluxe, Seater, and Total Seating Capacity).
2. **Route & Corridor Management:** Management of transit corridors across Tamil Nadu and South India (Source, Destination, Distance in km, Intermediate stops, Estimated Travel Time).
3. **Trip & Schedule Scheduling:** Assignment of buses to routes with departure times, arrival times, operating dates, and dynamic fare structures.
4. **Passenger Booking & Ticketing:** Interactive, seat-selection booking engine allowing commuters to view real-time seat grids, reserve seats, receive ticket confirmations with PNRs, and cancel tickets with automatic seat release.
5. **Concurrency & Capacity Control:** Robust multithreaded transaction management preventing overbooking beyond certified bus seating capacity under high-concurrency peak load.
6. **Reporting & Business Intelligence:** Automated report generation for passenger manifests, route-wise revenue, and bus occupancy rates.
7. **Python Exploratory Data Analysis (EDA):** Extraction of transactional data from PostgreSQL to generate statistical distributions, route demand heatmaps, peak travel histograms, and correlation matrices for data-driven transit planning.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS:** Software Requirements Specification
- **PNR:** Passenger Name Record (Unique Booking / Ticket Reference)
- **DBMS:** Database Management System
- **RDBMS:** Relational Database Management System (PostgreSQL)
- **ACID:** Atomicity, Consistency, Isolation, Durability
- **EDA:** Exploratory Data Analysis
- **API:** Application Programming Interface
- **VCET:** Velalar College of Engineering and Technology

### 1.4 References
- IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.
- VCET IT Department Project Assessment Guidelines (Academic Year 2026-27 ODD).
- 25ITT32 Java Programming, 25ITT31 DBMS, 25ITC31 Foundations of Data Science, 25ITT33 Software Engineering syllabi.

---

## 2. OVERALL DESCRIPTION

### 2.1 Product Perspective
The system operates as an integrated multi-tier software solution:
- **Presentation Tier:** Responsive Web Interface (HTML5, Tailwind CSS, JavaScript, Chart.js) providing intuitive passenger booking portals, visual seat selectors, and admin management dashboards.
- **Application Tier:** Java 17 / Spring Boot enterprise service handling business validation, synchronized booking transactions, multithreaded capacity checks, and REST endpoints.
- **Database Tier:** PostgreSQL relational database hosting normalized tables (3NF/BCNF) enforcing referential integrity, foreign key cascading, check constraints, and triggers.
- **Analytics & BI Tier:** Python (Pandas, NumPy, Matplotlib, Seaborn) analytics pipeline reading relational records to produce diagnostic charts and travel demand forecasts.

```
+-------------------------------------------------------------------+
|               PRESENTATION TIER (Web Browser UI)                 |
|  Passenger Portal  |  Seat Matrix Grid  |  Admin Control Panel    |
+---------------------------------+---------------------------------+
                                  | HTTP / JSON REST APIs
+---------------------------------v---------------------------------+
|             APPLICATION TIER (Java 17 / Spring Boot)             |
|  Controllers  |  Services (Synchronized Concurrency) | JPA Repos  |
+---------------------------------+---------------------------------+
                                  | JDBC / SQL Connections
+---------------------------------v---------------------------------+
|             DATABASE TIER (PostgreSQL Relational DB)             |
|   Buses | Routes | Schedules | Passengers | Bookings | Tickets    |
+---------------------------------+---------------------------------+
                                  | Data Extraction & SQL Queries
+---------------------------------v---------------------------------+
|        ANALYTICS & DATA SCIENCE TIER (Python / Pandas / Seaborn)  |
|  ETL Cleaning | Descriptive Stats | Heatmaps | Demand Visualizations|
+-------------------------------------------------------------------+
```

### 2.2 User Characteristics
1. **Passengers (Commuters):** General public searching for buses between cities (e.g., Erode to Chennai), reviewing departure timings, selecting available seats, booking tickets, downloading e-tickets, and cancelling bookings.
2. **Transport Administrators / Fleet Managers:** Transit staff responsible for registering new buses, defining transit routes, scheduling daily trips, setting base fares, viewing passenger manifests, and reviewing revenue reports.
3. **Transit Data Analysts:** Operations staff utilizing Python data science modules to analyze passenger route demand, load factors, revenue leakages, and seasonal travel surges.

### 2.3 General Constraints
- Language: Java (Version 17 LTS).
- Database: PostgreSQL (Relational DBMS) with strict relational constraints.
- Data Science Stack: Python 3.x using Pandas, NumPy, Matplotlib, Seaborn.
- Deployment: 24/7 Cloud Architecture (Dockerized container on Render + Cloud PostgreSQL).
- Operating System: Platform independent (Windows, Linux, macOS).

---

## 3. SPECIFIC FUNCTIONAL REQUIREMENTS

### 3.1 Bus Details Management
- **FR-1.1:** The system shall allow administrators to register new buses with attributes: Bus ID, Bus Number (e.g., `TN-33-AB-1234`), Bus Type (`AC Sleeper`, `Semi-Sleeper`, `Ultra Deluxe`, `Non-AC Seater`), and Total Capacity (ranging from 24 to 45 seats).
- **FR-1.2:** The system shall enforce unique registration numbers for each bus.
- **FR-1.3:** The system shall validate that capacity is a positive integer and that bus type conforms to standardized categories.

### 3.2 Route Information Management
- **FR-2.1:** The system shall maintain corridor details including Route ID, Source City (e.g., Erode), Destination City (e.g., Chennai Central), Distance in kilometers (e.g., 420.5 km), and Estimated Duration (e.g., 7 hours 30 mins).
- **FR-2.2:** The system shall allow querying of routes by origin and destination city.
- **FR-2.3:** The system shall prevent duplicate active routes having the identical source and destination combination.

### 3.3 Bus Scheduling & Fare Management
- **FR-3.1:** The system shall schedule trips linking a specific bus to an active route on designated travel dates.
- **FR-3.2:** The system shall record Departure Time, Expected Arrival Time, Base Ticket Fare, and Available Seats for each schedule.
- **FR-3.3:** The system shall initialize available seats equal to the bus's certified total seating capacity upon schedule creation.

### 3.4 Passenger Booking & Ticket Reservation
- **FR-4.1:** The system shall provide an interactive seat map displaying booked seats (disabled) and available seats (selectable).
- **FR-4.2:** The system shall capture passenger information: Name, Age, Gender, Contact Phone, and Email Address.
- **FR-4.3:** The system shall generate a unique PNR (Passenger Name Record) reference code upon successful transaction (e.g., `TCK-2026-XXXX`).
- **FR-4.4:** The system shall calculate the total booking fare based on selected seats and schedule base fare.

### 3.5 Thread-Safe Concurrency & Overbooking Prevention
- **FR-5.1:** The system shall employ Java synchronized methods / database pessimistic row locking during seat allocation.
- **FR-5.2:** If two concurrent requests attempt to reserve the same seat or book beyond the remaining capacity, the system shall safely commit the first transaction and throw a `SeatNotAvailableException` or `OverbookingException` for subsequent conflicting attempts.
- **FR-5.3:** Under no circumstance shall total confirmed seats exceed the bus capacity.

### 3.6 Ticket Cancellation & Seat Release
- **FR-6.1:** Commuters shall be permitted to cancel confirmed bookings by providing their unique PNR / Ticket Number.
- **FR-6.2:** Upon cancellation, the system shall mark the ticket status as `CANCELLED`, update booking status, and automatically increment the schedule's available seat count.
- **FR-6.3:** Cancelled seats shall immediately return to the available inventory for other commuters to book.

### 3.7 Operational Reporting & Financial Summaries
- **FR-7.1:** The system shall compute and display Route-Wise Revenue aggregated across confirmed bookings.
- **FR-7.2:** The system shall generate Bus Occupancy Percentage reports calculated as `(Booked Seats / Total Capacity) * 100`.
- **FR-7.3:** The system shall produce passenger manifest lists for each bus schedule showing seat numbers, passenger names, and contact details.

### 3.8 Python Data Retrieval, Preprocessing & Visualizations
- **FR-8.1:** The Python pipeline shall connect to PostgreSQL or ingest the exported operational dataset.
- **FR-8.2:** The pipeline shall preprocess data using Pandas: handle missing values, format timestamps, compute duration deltas, detect statistical outliers, and encode categorical variables.
- **FR-8.3:** The system shall generate meaningful exploratory charts:
  - Route-Wise Passenger Demand (Bar Chart).
  - Route-Wise Revenue Generation (Bar Chart).
  - Seat Occupancy Distribution by Bus Type (Box Plot).
  - Hourly Departure Demand Profile (Histogram / KDE).
  - Booking Status Ratio (Pie Chart).
  - Correlation Heatmap of Travel Metrics (Seaborn Heatmap).
  - Daily Booking Volume Trend (Time Series Line Chart).

---

## 4. NON-FUNCTIONAL REQUIREMENTS

### 4.1 Performance Requirements
- **Response Time:** Web API requests (seat search, schedule lookup) shall respond within 200 milliseconds under standard load.
- **Throughput:** Booking engine shall handle at least 100 concurrent transactions per second without deadlocks or race conditions.

### 4.2 Reliability & Availability
- **Uptime:** The application shall maintain 99.9% uptime when deployed on 24/7 cloud infrastructure.
- **Data Integrity:** ACID properties shall strictly govern all booking and cancellation transactions.

### 4.3 Security Requirements
- **Input Validation:** All client inputs shall be validated on both client-side and server-side to prevent SQL injection and cross-site scripting (XSS).
- **Data Privacy:** Passenger contact numbers and email addresses shall be stored securely with standard privacy guidelines.

### 4.4 Maintainability & Extensibility
- **Architecture:** Layered Model-View-Controller (MVC) and Repository pattern for clean separation of concerns.
- **Documentation:** Well-commented Java classes, modular SQL scripts, and annotated Python code.

---

## 5. REVISION HISTORY
| Version | Date | Description | Author |
| :--- | :--- | :--- | :--- |
| 1.0 | 2026-11-18 | Initial Complete SRS for VCET Project Assessment Scenario 10 | Jeffrin (732925ITR040) |
