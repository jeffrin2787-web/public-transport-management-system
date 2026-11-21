# PUBLIC TRANSPORT MANAGEMENT AND PASSENGER TRAVEL ANALYSIS SYSTEM
### Activity: Project-Based Assessment (Academic Year: 2026–2027 ODD)
**Velalar College of Engineering and Technology (Autonomous), Erode – 638012**  
**Department of Information Technology**  
**Class:** 25IT3A  

---

### **STUDENT & SUBMISSION DETAILS**
- **Student Name:** Jeffrin
- **Register Number:** 732925ITR040
- **Class / Section:** 25IT3A
- **Assigned Scenario:** **Scenario 10 – Public Transport Management and Passenger Travel Analysis System** (Register No: 10, 40, 70, 100)
- **Primary Database:** PostgreSQL
- **Transit Network Scope:** Tamil Nadu & South India Regional Transit Hub (Erode, Coimbatore, Salem, Tirupur, Chennai Central, Bengaluru, Madurai, Tiruchirappalli, Ooty)

---

## 1. PROJECT OVERVIEW & PROBLEM STATEMENT

A public transport service operates bus fleets, transit corridors, daily schedules, commuter ticket reservations, and cancellation records. Maintaining these records manually or via legacy disconnected spreadsheets causes:
- Difficulty in tracking real-time seat availability.
- Overbooking race conditions during high passenger concurrency.
- Inability to quickly detect high-demand corridors and peak travel hours.
- Lack of data-driven intelligence for fleet scheduling and revenue optimization.

This **Public Transport Management and Passenger Travel Analysis System** addresses these operational hurdles by uniting **Java 17 / Spring Boot**, **PostgreSQL Relational DBMS**, and **Python Data Science (Pandas, NumPy, Matplotlib, Seaborn)** into a production-grade, 24/7 web application.

---

## 2. INTEGRATED COURSE SYLLABUS ALIGNMENT

| Course Code & Name | Key Concepts Implemented | Project Artifacts |
| :--- | :--- | :--- |
| **25ITT32: Java Programming** | OOP Inheritance (`Vehicle` &rarr; `Bus`), Interfaces (`BookingService`), Custom Exceptions, Concurrency & Multithreading (synchronized seat allocation), Spring Data JPA, Collections, Lambdas & Streams. | `src/main/java/com/vcet/transport/` |
| **25ITT31: Database Management Systems** | Relational Modeling, Entity-Relationship (ER) Diagram, Normalization (1NF, 2NF, 3NF, BCNF), Complex SQL Joins, Triggers, Views, Check Constraints. | `2_DATABASE_DESIGN_AND_SQL/` |
| **25ITC31: Foundations of Data Science** | Data Preprocessing, Handling Missing Values, Outlier Analysis, Exploratory Data Analysis (EDA), Statistical Distributions, Visualizations (Bar, Pie, Heatmap, Time-Series, Box plots). | `3_PYTHON_DATA_SCIENCE_ANALYSIS/` |
| **25ITT33: Software Engineering** | IEEE 830 SRS Document, Use Case Diagrams, Class Diagrams, Sequence Diagrams, System Architecture, White-Box & Black-Box Test Cases with Expected vs Actual Results. | `1_SOFTWARE_ENGINEERING_DOCS/` |

---

## 3. REPOSITORY DIRECTORY STRUCTURE

```
d:\SEM PROJECT\
├── README.md                                    # Project documentation, execution & deployment guide
├── Dockerfile                                   # Multi-stage production container build
├── render.yaml                                  # Render blueprint for 1-click 24/7 web + DB hosting
├── pom.xml                                      # Maven dependencies (Java 17, Spring Boot, JPA, PostgreSQL)
├── .gitignore                                   # Git configuration
│
├── 1_SOFTWARE_ENGINEERING_DOCS/                 # 25ITT33: Unit-wise SE documentation, diagrams, testing & COCOMO
│   ├── UNIT_WISE_SOFTWARE_ENGINEERING_PORTFOLIO.md # Master Comprehensive Portfolio (Units 1 to 5)
│   ├── SRS_Document.md                          # IEEE 830 format SRS Document (Units 1 & 2)
│   ├── Design_Diagrams.md                       # Mermaid Architecture, Class, Component, Sequence (Unit 3)
│   ├── Testing_Document_and_Test_Cases.md       # V&V, White/Black Box test tables, Cyclomatic Complexity (Unit 4)
│   └── Project_Management_and_COCOMO.md         # 4P's, LOC (8,884), Function Points & COCOMO calculations (Unit 5)
│
├── 2_DATABASE_DESIGN_AND_SQL/                   # Requirement 3 & 5: ER Diagram, relational model, SQL scripts, normalization
│   ├── ER_Diagram_and_Relational_Model.md       # Entity-Relationship diagram, schemas, constraints
│   ├── Normalization_Documentation.md           # 1NF, 2NF, 3NF, BCNF step-by-step documentation
│   ├── 01_schema.sql                            # DDL statements (Buses, Routes, Schedules, Passengers, Bookings, Tickets)
│   ├── 02_seed_data.sql                         # Realistic Tamil Nadu routes (Erode, CBE, Salem, Chennai, etc.)
│   ├── 03_queries_and_reports.sql               # Complex analytical queries, joins, aggregates
│   └── 04_triggers_and_views.sql                # Triggers for capacity checks, revenue & occupancy views
│
├── 3_PYTHON_DATA_SCIENCE_ANALYSIS/              # Requirement 6 & 10: Data retrieval, preprocessing, visualizations
│   ├── data/
│   │   └── public_transport_dataset.csv         # Realistic Tamil Nadu transit dataset (150 records)
│   ├── passenger_travel_analysis.py             # Python script for ETL, data cleaning, wrangling & plotting
│   ├── passenger_travel_analysis.ipynb          # Jupyter notebook for submission
│   └── visualizations/                          # Generated high-resolution charts
│       ├── 01_route_wise_passenger_demand.png
│       ├── 02_route_wise_revenue.png
│       ├── 03_bus_type_occupancy_distribution.png
│       ├── 04_hourly_departure_pattern.png
│       ├── 05_booking_status_distribution.png
│       ├── 06_correlation_heatmap.png
│       └── 07_daily_booking_trends.png
│
└── src/                                         # Requirement 4: Java source code (Spring Boot 3 / Java 17)
    ├── main/
    │   ├── java/com/vcet/transport/
    │   │   ├── TransportApplication.java       # Spring Boot main class
    │   │   ├── config/DataLoader.java           # Startup seed data loader
    │   │   ├── model/                           # Bus, Route, Schedule, Passenger, Booking, Ticket, BusType
    │   │   ├── repository/                      # Spring Data JPA repositories
    │   │   ├── service/                         # Multithreaded synchronized booking & report services
    │   │   ├── exception/                       # Custom exception handlers (Overbooking/Not Found)
    │   │   └── controller/                      # REST & web endpoints
    │   └── resources/
    │       ├── application.properties           # Primary app config (PostgreSQL + auto H2 fallback)
    │       ├── application-prod.properties      # 24/7 cloud deployment configuration
    │       └── static/                          # Interactive web frontend
    │           ├── index.html                   # Bus search & visual seat selector
    │           ├── ticket.html                  # PNR enquiry & ticket cancellation
    │           ├── admin.html                   # Fleet, route & schedule manager
    │           ├── reports.html                 # BI & Python visualization dashboard
    │           ├── css/styles.css
    │           ├── js/app.js
    │           └── visualizations/              # Embedded Python charts
    └── test/
        └── java/com/vcet/transport/
            └── BookingServiceTest.java          # Unit & Multithreaded concurrency tests
```

---

## 4. FUNCTIONAL HIGHLIGHTS & KEY FEATURES

1. **Bus Search & Visual Seat Selection:**
   - Real-time search across Tamil Nadu routes (e.g. Erode &rarr; Chennai Central, Coimbatore &rarr; Bengaluru).
   - Visual interactive bus cabin layout showing driver cabin, booked seats (disabled), and available seats.
   - Live fare calculation and instant PNR generation.
2. **Synchronized Multithreaded Concurrency Protection:**
   - Prevents race conditions when multiple commuters click the last remaining seat at the exact same millisecond.
   - Synchronized service transactions guarantee total bookings never exceed certified bus seating capacity.
3. **Ticket Cancellation & Seat Auto-Restoration:**
   - Commuters can track PNR and cancel tickets online.
   - Cancelled seats are immediately returned to public inventory and available seat counters are incremented.
4. **Fleet & Transit Corridor Administration:**
   - Dedicated Admin Console to register new buses, add new transit corridors, and create daily schedules.
   - Master bookings audit table with live status monitoring.
5. **Business Intelligence & Python Exploratory Data Analysis:**
   - Route-wise gross revenue aggregation.
   - Fleet occupancy percentage tracking.
   - 7 publication-grade statistical charts generated using Matplotlib & Seaborn.

---

## 5. LOCAL EXECUTION & SETUP INSTRUCTIONS

### Prerequisites
- **Java:** JDK 17 or higher
- **Python:** Python 3.9+ with `pandas`, `numpy`, `matplotlib`, `seaborn`
- **Database:** PostgreSQL (Optional: the app automatically falls back to an embedded persistent H2 database if local PostgreSQL is not running, so it works instantly anywhere!)

### Step 1: Run the Python Data Science Visualizations Pipeline
To regenerate the 7 statistical figures from the transit dataset:
```bash
cd "d:\SEM PROJECT\3_PYTHON_DATA_SCIENCE_ANALYSIS"
python passenger_travel_analysis.py
```
*All charts will be refreshed in both `3_PYTHON_DATA_SCIENCE_ANALYSIS/visualizations/` and `src/main/resources/static/visualizations/`.*

### Step 2: Initialize Database (If using local PostgreSQL)
Open `psql` or pgAdmin and run:
```sql
\i 'd:/SEM PROJECT/2_DATABASE_DESIGN_AND_SQL/01_schema.sql'
\i 'd:/SEM PROJECT/2_DATABASE_DESIGN_AND_SQL/02_seed_data.sql'
\i 'd:/SEM PROJECT/2_DATABASE_DESIGN_AND_SQL/04_triggers_and_views.sql'
```

### Step 3: Run the Java Spring Boot Web Application
Using Maven:
```bash
mvn clean spring-boot:run
```
Or build and run the JAR:
```bash
mvn clean package -DskipTests
java -jar target/public-transport-system-1.0.0.jar
```

### Step 4: Access the Application in Your Browser
- **Passenger Booking Portal:** [http://localhost:8080](http://localhost:8080)
- **PNR Tracking & Cancellation:** [http://localhost:8080/ticket.html](http://localhost:8080/ticket.html)
- **Admin Fleet & Schedule Portal:** [http://localhost:8080/admin.html](http://localhost:8080/admin.html)
- **Data Science Analytics Dashboard:** [http://localhost:8080/reports.html](http://localhost:8080/reports.html)

---

## 6. STEP-BY-STEP 24/7 LIVE CLOUD DEPLOYMENT GUIDE (RENDER)

To host this project **100% free and live 24/7** on the cloud:

### Phase A: Create a Free Managed PostgreSQL Database
1. Go to [neon.tech](https://neon.tech) or [render.com](https://render.com) and sign up for a free account.
2. Click **New Database** &rarr; Name it `public_transport_db` &rarr; Choose Region: **Singapore / Asia-South**.
3. Copy your connection URL:
   `jdbc:postgresql://<host>/public_transport_db?sslmode=require`

### Phase B: Push Project to GitHub
1. In your local terminal:
   ```bash
   git init
   git add .
   git commit -m "Public Transport Management and Passenger Travel Analysis System - VCET Scenario 10"
   ```
2. Create a new repository on GitHub: `public-transport-management-system`.
3. Push your code:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-github-username>/public-transport-management-system.git
   git push -u origin main
   ```

### Phase C: Deploy to Render for 24/7 Live Access
1. Sign in to [render.com](https://render.com) with your GitHub account.
2. Click **New +** &rarr; **Web Service**.
3. Select your GitHub repository (`public-transport-management-system`).
4. Configure service:
   - **Environment:** `Docker` (Render will automatically detect our `Dockerfile`)
   - **Plan:** `Free`
   - **Region:** `Singapore`
5. In **Environment Variables**, add:
   - `SPRING_DATASOURCE_URL` = `<your-postgresql-jdbc-url>`
   - `SPRING_DATASOURCE_USERNAME` = `<your-db-username>`
   - `SPRING_DATASOURCE_PASSWORD` = `<your-db-password>`
6. Click **Deploy Web Service**.

### Phase D: Your Website is Live!
- In 2 to 3 minutes, Render builds the container and gives you a public URL:
  `https://vcet-transport-system.onrender.com`
- Anyone can access the full live application 24/7 on laptop or mobile!

---

## 7. GITHUB SUBMISSION CHECKLIST

- [x] **Requirement 1:** SRS document, design diagrams (Use Case, Class, Sequence, Architecture), and testing documents.
- [x] **Requirement 2:** Java source code with input handling, classes, methods, business logic, multithreaded concurrency, and sample outputs.
- [x] **Requirement 3:** ER Diagram, Relational Model, complete SQL scripts (`01_schema.sql`, `02_seed_data.sql`, `03_queries_and_reports.sql`, `04_triggers_and_views.sql`), and 1NF–BCNF Normalization details.
- [x] **Requirement 4:** Python code for database retrieval, data preprocessing, and visualizations (`passenger_travel_analysis.py` & `.ipynb`).
- [x] **Requirement 5:** Comprehensive `README.md` with project description, technologies used, database setup, and execution instructions.
- [x] **Bonus Requirement:** 24/7 Cloud deployment infrastructure (`Dockerfile` and `render.yaml`).
