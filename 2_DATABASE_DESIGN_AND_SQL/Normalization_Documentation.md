# DATABASE NORMALIZATION DOCUMENTATION
## Public Transport Management and Passenger Travel Analysis System

---

### **ACADEMIC ASSESSMENT DETAILS**
- **Institution:** Velalar College of Engineering and Technology (Autonomous), Erode – 638012
- **Department:** Department of Information Technology
- **Course Title & Code:** Database Management Systems (25ITT31) – Unit 3: Normalization
- **Student Name:** Jeffrin
- **Register Number:** 732925ITR040
- **Class:** 25IT3A
- **Scenario:** Scenario 10 – Public Transport Management and Passenger Travel Analysis System

---

## 1. PURPOSE AND THEORETICAL FOUNDATION

The objective of relational database normalization is to organize tables and attributes to minimize data redundancy, eliminate update, insertion, and deletion anomalies, and ensure data integrity.

### Armstrong's Axioms and Functional Dependencies
Let $R$ be a relational schema and $F$ be a set of functional dependencies.
1. **Reflexivity:** If $Y \subseteq X$, then $X \to Y$.
2. **Augmentation:** If $X \to Y$, then $XZ \to YZ$ for any $Z$.
3. **Transitivity:** If $X \to Y$ and $Y \to Z$, then $X \to Z$.

---

## 2. THE UNNORMALIZED FORM (UNF)

In an unnormalized legacy transport sheet, all transit, schedule, passenger, and ticket details are stored in a single massive flat relation:

```
UNNORMALIZED_TRANSPORT_RECORD (
    PNR_Number,
    Booking_Date,
    Passenger_Name,
    Passenger_Age,
    Passenger_Phone,
    Passenger_Email,
    Bus_Number,
    Bus_Type,
    Bus_Capacity,
    Operator_Name,
    Source_City,
    Destination_City,
    Route_Distance_KM,
    Travel_Date,
    Departure_Time,
    Arrival_Time,
    Base_Fare,
    Seat_Numbers_List,       -- Multi-valued attribute (e.g., "12, 14, 15")
    Ticket_Fares_List,        -- Multi-valued attribute (e.g., "450, 450, 450")
    Total_Booking_Amount,
    Booking_Status
)
```

### Anomalies in UNF:
1. **Redundancy:** Bus number, capacity, source city, destination, and fare are duplicated for every passenger booking on that bus.
2. **Insertion Anomaly:** Cannot record a new bus or route without booking at least one passenger ticket.
3. **Deletion Anomaly:** Cancelling all passenger bookings on a route inadvertently deletes the bus specifications and route distance data.
4. **Update Anomaly:** Updating the fare or bus capacity requires modifying hundreds of individual passenger rows, risking data inconsistency.

---

## 3. FIRST NORMAL FORM (1NF)

### 1NF Definition:
A relation $R$ is in First Normal Form (1NF) if and only if all underlying attribute domains contain only **atomic (indivisible) values**, and there are no repeating groups or multi-valued attributes.

### Transformation from UNF to 1NF:
- We split the multi-valued comma-separated attributes (`Seat_Numbers_List`, `Ticket_Fares_List`) into individual atomic rows.
- We establish a composite candidate key: `{PNR_Number, Seat_Number}`.

```
FLAT_1NF_TRANSPORT (
    PNR_Number,                -- Key component
    Seat_Number,               -- Key component
    Booking_Date,
    Passenger_Name,
    Passenger_Age,
    Passenger_Phone,
    Passenger_Email,
    Bus_Number,
    Bus_Type,
    Bus_Capacity,
    Operator_Name,
    Source_City,
    Destination_City,
    Route_Distance_KM,
    Travel_Date,
    Departure_Time,
    Arrival_Time,
    Base_Fare,
    Seat_Fare,
    Total_Booking_Amount,
    Booking_Status
)
```
- **State in 1NF:** All attributes are atomic. However, severe partial dependencies exist on the composite key.

---

## 4. SECOND NORMAL FORM (2NF)

### 2NF Definition:
A relation $R$ is in Second Normal Form (2NF) if and only if it is in **1NF** and **no non-prime attribute is partially dependent** on any candidate key (i.e., every non-prime attribute is fully functionally dependent on the entire primary key).

### Identification of Functional Dependencies:
- `FD1: {PNR_Number, Seat_Number} -> Seat_Fare` (Full key dependency)
- `FD2: PNR_Number -> {Booking_Date, Passenger_Name, Passenger_Phone, Total_Booking_Amount, Booking_Status}` (Partial dependency on composite key!)
- `FD3: Bus_Number -> {Bus_Type, Bus_Capacity, Operator_Name}` (Partial dependency!)
- `FD4: {Source_City, Destination_City} -> {Route_Distance_KM}` (Partial dependency!)

### Decomposing into 2NF:
We decompose `FLAT_1NF_TRANSPORT` into separate relations where non-prime attributes depend on full keys:

1. **`TICKETS_2NF`** (`PNR_Number`, `Seat_Number`, `Seat_Fare`, `Ticket_Status`)
   - Primary Key: `{PNR_Number, Seat_Number}`
2. **`BOOKINGS_2NF`** (`PNR_Number`, `Passenger_Phone`, `Schedule_Code`, `Booking_Date`, `Total_Amount`, `Status`)
   - Primary Key: `{PNR_Number}`
3. **`SCHEDULES_2NF`** (`Schedule_Code`, `Bus_Number`, `Route_Code`, `Travel_Date`, `Departure_Time`, `Arrival_Time`, `Base_Fare`)
   - Primary Key: `{Schedule_Code}`
4. **`BUSES_2NF`** (`Bus_Number`, `Bus_Type`, `Bus_Capacity`, `Operator_Name`)
   - Primary Key: `{Bus_Number}`
5. **`ROUTES_2NF`** (`Route_Code`, `Source_City`, `Destination_City`, `Route_Distance_KM`, `Estimated_Duration`)
   - Primary Key: `{Route_Code}`
6. **`PASSENGERS_2NF`** (`Passenger_Phone`, `Passenger_Name`, `Passenger_Age`, `Passenger_Email`)
   - Primary Key: `{Passenger_Phone}`

---

## 5. THIRD NORMAL FORM (3NF)

### 3NF Definition:
A relation $R$ is in Third Normal Form (3NF) if and only if it is in **2NF** and **no transitive dependency exists** for non-prime attributes. Formally, for every non-trivial functional dependency $X \to Y$:
- $X$ is a super key, OR
- $Y$ is a prime attribute (part of a candidate key).

### Elimination of Transitive Dependencies:
In `BOOKINGS_2NF`:
- Dependency: `PNR_Number -> Schedule_Code`
- And `Schedule_Code -> {Base_Fare, Travel_Date, Departure_Time}`
- Here, `PNR_Number -> Base_Fare` is a transitive dependency via `Schedule_Code`.
- By removing schedule-specific calculation attributes from `BOOKINGS` and computing `Total_Amount` strictly from `Ticket_Fare` sums, transitive dependencies are eliminated.

### 3NF Schema Result:
- **`buses`** (bus_id [PK], bus_number [UK], bus_type, total_capacity, operator_name, is_active)
- **`routes`** (route_id [PK], source_city, destination_city, distance_km, estimated_duration_minutes)
- **`schedules`** (schedule_id [PK], bus_id [FK], route_id [FK], travel_date, departure_time, arrival_time, base_fare, available_seats)
- **`passengers`** (passenger_id [PK], full_name, age, gender, phone_number, email)
- **`bookings`** (booking_id [PK], pnr_number [UK], schedule_id [FK], passenger_id [FK], booking_time, total_amount, status)
- **`tickets`** (ticket_id [PK], ticket_number [UK], booking_id [FK], seat_number, seat_fare, status)

All non-prime attributes are directly and strictly dependent on the primary keys without transitivity.

---

## 6. BOYCE-CODD NORMAL FORM (BCNF)

### BCNF Definition:
A relation $R$ is in Boyce-Codd Normal Form (BCNF) if and only if for **every non-trivial functional dependency $X \to Y$, $X$ is a super key**.

### Evaluation of Schema in BCNF:

1. **Relation `buses`:**
   - Determinant: `bus_id` is a primary key (super key).
   - Determinant: `bus_number` is a candidate key (super key).
   - `bus_id -> {bus_number, bus_type, total_capacity, operator_name}`
   - `bus_number -> {bus_id, bus_type, total_capacity, operator_name}`
   - *Status:* **In BCNF**.

2. **Relation `routes`:**
   - Determinant: `route_id` is a primary key.
   - Determinant: `{source_city, destination_city}` is unique (candidate key).
   - `route_id -> {source_city, destination_city, distance_km, estimated_duration_minutes}`
   - `{source_city, destination_city} -> {route_id, distance_km, estimated_duration_minutes}`
   - *Status:* **In BCNF**.

3. **Relation `schedules`:**
   - Determinant: `schedule_id` is a primary key (super key).
   - `schedule_id -> {bus_id, route_id, travel_date, departure_time, arrival_time, base_fare, available_seats}`
   - *Status:* **In BCNF**.

4. **Relation `passengers`:**
   - Determinant: `passenger_id` is a primary key (super key).
   - `passenger_id -> {full_name, age, gender, phone_number, email}`
   - *Status:* **In BCNF**.

5. **Relation `bookings`:**
   - Determinant: `booking_id` is a primary key (super key).
   - Determinant: `pnr_number` is a unique candidate key (super key).
   - `booking_id -> {pnr_number, schedule_id, passenger_id, booking_time, total_amount, status}`
   - `pnr_number -> {booking_id, schedule_id, passenger_id, booking_time, total_amount, status}`
   - *Status:* **In BCNF**.

6. **Relation `tickets`:**
   - Determinant: `ticket_id` is a primary key (super key).
   - Determinant: `ticket_number` is unique (super key).
   - Determinant: `{booking_id, seat_number}` is unique (super key).
   - *Status:* **In BCNF**.

### Lossless-Join and Dependency Preservation:
- **Lossless-Join Property:** Each decomposition step used a common attribute that forms a primary key in one of the sub-relations, guaranteeing $R_1 \bowtie R_2 = R$.
- **Dependency Preservation:** All functional dependencies are preserved across the tables.

---

## 7. SUMMARY COMPARISON TABLE

| Normal Form | Requirement Met | Anomalies Eliminated | Current Schema Status |
| :--- | :--- | :--- | :--- |
| **UNF** | None (Raw spreadsheet format) | None (Severe duplication & anomalies) | Transformed |
| **1NF** | Atomic attribute values, no repeating lists | Inconsistent list indexing | Satisfied |
| **2NF** | In 1NF + no partial dependencies on composite keys | Redundant bus/route updates | Satisfied |
| **3NF** | In 2NF + no transitive dependencies | Intermediate calculation leakage | Satisfied |
| **BCNF** | Every determinant is a candidate super key | Overlapping multi-attribute anomalies | **Fully Satisfied & Compliant** |
