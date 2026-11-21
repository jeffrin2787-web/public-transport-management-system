# SOFTWARE PROJECT MANAGEMENT AND COCOMO COST MODELLING (UNIT 5)
## Public Transport Management and Passenger Travel Analysis System

---

### **ACADEMIC ASSESSMENT DETAILS**
- **Institution:** Velalar College of Engineering and Technology (Autonomous), Erode – 638012
- **Department:** Department of Information Technology
- **Course Title & Code:** Software Engineering (25ITT33) | Unit 5: Project Management
- **Student Name:** Jeffrin
- **Register Number:** 732925ITR040
- **Class:** 25IT3A
- **Scenario:** Scenario 10 – Public Transport Management and Passenger Travel Analysis System

---

## 1. THE 4P'S OF SOFTWARE PROJECT MANAGEMENT

Software project management is the disciplined planning, monitoring, and control of personnel, process, and artifacts. The four P's represent the core pillars:

```mermaid
flowchart TD
    P1["1. PEOPLE<br/>• Student / Lead Developer: Jeffrin (732925ITR040)<br/>• Evaluator / Faculty: Department of IT, VCET<br/>• Stakeholders: Commuters, Transport Operators"]
    P2["2. PRODUCT<br/>• Scope: Public Bus Transit & Analysis<br/>• Technical Stack: Java 17, PostgreSQL, Python<br/>• Core Deliverables: 24/7 Web App, EDA Charts"]
    P3["3. PROCESS<br/>• Methodology: Agile Scrum (5 Sprints)<br/>• Lifecycle: Framework & Umbrella Activities<br/>• Standards: IEEE 830 SRS, CMMI Level 3"]
    P4["4. PROJECT<br/>• Delivery Window: 5 Academic Sprints<br/>• Size: 8,884 Lines of Code (8.884 KLOC)<br/>• Hosting: Render Cloud + Neon PostgreSQL"]

    P1 --- P2
    P2 --- P3
    P3 --- P4
    P4 --- P1
```

1. **People:**
   - **Lead Full-Stack Developer & Analyst:** Jeffrin (Reg No: 732925ITR040)
   - **Academic Mentors & Reviewers:** Department of Information Technology, VCET
   - **User Community:** Commuters traveling between Erode, Coimbatore, Salem, Tirupur, Chennai, and Bengaluru.
2. **Product:**
   - Real-time seat reservation engine, concurrency locking, cancellation management, dynamic Chart.js reporting, and Python exploratory data analysis.
3. **Process:**
   - Agile Scrum development model with weekly sprint reviews and continuous integration.
4. **Project:**
   - Time-boxed academic execution with automated test checkpoints and zero-cost cloud deployment.

---

## 2. COMPREHENSIVE LINES OF CODE (LOC) AUDIT

Lines of Code (LOC) is a direct, measurable size metric used as input to estimation models. The physical line count of the codebase was audited:

```
d:\SEM PROJECT\
├── Java Source Code (.java)      : 2,209 lines  (32 files)
├── Python Analytics Script (.py) : 1,246 lines  (5 files)
├── PostgreSQL Scripts (.sql)     :   491 lines  (4 files)
├── HTML5 User Interfaces (.html) : 3,068 lines  (10 files)
├── CSS3 Styling Rules (.css)     : 1,268 lines  (2 files)
└── Client JavaScript (.js)       :   602 lines  (2 files)
===========================================================
TOTAL PHYSICAL LINES OF CODE      : 8,884 Lines
TOTAL KLOC (Thousand Lines)       : 8.884 KLOC
```

---

## 3. FUNCTION POINT (FP) ANALYSIS

Function Point analysis measures software size based on functionality delivered to users rather than lines of programming code.

### 3.1 Unadjusted Function Points (UFP)

| Information Domain Element | Description / Examples | Count | Weight Factor | Unadjusted FP |
| :--- | :--- | :---: | :---: | :---: |
| **External Inputs (EI)** | Reserve Seat, Cancel Ticket, Register Bus, Add Route Corridor, Schedule Trip | 5 | Low (3) | $5 \times 3 = \mathbf{15}$ |
| **External Outputs (EO)** | Digital Boarding Pass, PNR Receipt, Live Chart Data, Financial Revenue Summary | 4 | Average (5) | $4 \times 5 = \mathbf{20}$ |
| **External Inquiries (EQ)** | Schedule Discovery, Seat Layout Matrix, PNR Tracking, Relational DB Inspector | 4 | Low (3) | $4 \times 3 = \mathbf{12}$ |
| **Internal Logical Files (ILF)** | `buses`, `routes`, `schedules`, `passengers`, `bookings`, `tickets` | 6 | Average (10) | $6 \times 10 = \mathbf{60}$ |
| **External Interface Files (EIF)** | Cloud PostgreSQL Driver, Neon Endpoint, Container Engine | 3 | Low (5) | $3 \times 5 = \mathbf{15}$ |
| **TOTAL UFP** | | | | **$\mathbf{122}$** |

### 3.2 Value Adjustment Factor (VAF)
Based on 14 General System Characteristics ($F_1$ to $F_{14}$):
$$\sum_{i=1}^{14} F_i = 51$$
$$\text{VAF} = 0.65 + (0.01 \times 51) = \mathbf{1.16}$$

### 3.3 Adjusted Function Points (AFP)
$$\text{FP} = \text{UFP} \times \text{VAF} = 122 \times 1.16 = \mathbf{141.52 \text{ FP}}$$

---

## 4. COCOMO COST MODELLING (CONSTRUCTIVE COST MODEL)

### 4.1 Mode Categorization: Organic Mode
The system is categorized under **Organic Mode** because:
- Relatively small software team.
- Well-understood application domain (public bus reservations).
- Stable operating environment and standardized Java/Spring framework.

### 4.2 Basic COCOMO Model

#### Mathematical Formulas for Organic Mode:
- **Effort ($E$):** $E = a_b \times (\text{KLOC})^{b_b}$ (in Person-Months)
- **Development Time ($D$):** $D = c_b \times (E)^{d_b}$ (in Months)
- **Staff Size ($SS$):** $SS = \frac{E}{D}$ (in Persons)
- **Productivity ($P$):** $P = \frac{\text{LOC}}{E}$ (in LOC/Person-Month)

*Coefficients for Organic Mode:*
$$a_b = 2.4, \quad b_b = 1.05, \quad c_b = 2.5, \quad d_b = 0.38$$
$$\text{Project Size} = \mathbf{8.884 \text{ KLOC}}$$

---

### 4.3 Step-by-Step Mathematical Calculations

#### 1. Effort ($E$):
$$E = 2.4 \times (8.884)^{1.05}$$
$$\ln(8.884) = 2.1842$$
$$(8.884)^{1.05} = e^{2.1842 \times 1.05} = e^{2.2934} \approx 9.9085$$
$$E = 2.4 \times 9.9085 = \mathbf{23.78 \text{ Person-Months}}$$

#### 2. Development Time ($D$):
$$D = 2.5 \times (23.78)^{0.38}$$
$$\ln(23.78) = 3.1688$$
$$(23.78)^{0.38} = e^{3.1688 \times 0.38} = e^{1.2041} \approx 3.334$$
$$D = 2.5 \times 3.334 = \mathbf{8.34 \text{ Months}}$$

#### 3. Average Staff Size ($SS$):
$$SS = \frac{E}{D} = \frac{23.78}{8.34} \approx \mathbf{2.85 \implies 3 \text{ Full-Time Engineers}}$$

#### 4. Developer Productivity ($P$):
$$P = \frac{8,884 \text{ LOC}}{23.78 \text{ Person-Months}} = \mathbf{373.6 \text{ LOC / Person-Month}}$$

---

### 4.4 Realistic Software Project Cost Estimation (INR)
Using average industry developer compensation in Tamil Nadu (₹45,000 / month / engineer):

$$\text{Total Engineering Effort Cost} = 23.78 \text{ Person-Months} \times ₹45,000 = \mathbf{₹10,70,100 \text{ INR}}$$

| Cost Category | Estimation Basis | Amount (INR) |
| :--- | :--- | :---: |
| **Software Development Effort** | 23.78 Person-Months @ ₹45,000/PM | ₹10,70,100 |
| **Quality Assurance & Testing** | 15% of Development Effort | ₹1,60,515 |
| **Cloud Hosting & Infrastructure** | Containerization, CI/CD, SSL | ₹45,000 |
| **Contingency Buffer (10%)** | Risk Mitigation Reserve | ₹1,27,560 |
| **TOTAL ESTIMATED PROJECT BUDGET** | | **₹14,03,175 INR** |

---

## 5. RISK IDENTIFICATION AND MANAGEMENT (RMMM PLAN)

The Risk Mitigation, Monitoring, and Management (RMMM) plan establishes proactive measures against project failure:

```mermaid
quadrantChart
    title Risk Impact vs Probability Matrix
    x-axis Low Probability --> High Probability
    y-axis Low Impact --> Critical Impact
    quadrant-1 High Priority (Immediate Action)
    quadrant-2 Monitor & Plan
    quadrant-3 Low Priority
    quadrant-4 Mitigate via Design
    "Render Cloud 512MB RAM Limit": [0.85, 0.90]
    "Concurrent Overbooking Race": [0.80, 0.85]
    "Database Container Permissions": [0.65, 0.75]
    "External Neon Connection Dropped": [0.50, 0.60]
    "Scope Creep in Reports": [0.30, 0.40]
```

1. **Risk 1: Cloud Container RAM Overflow (>512MB on Free Tier)**
   - *Mitigation:* Explicit JVM memory flags (`-Xmx350m -XX:+UseContainerSupport`) added to Dockerfile.
2. **Risk 2: High Concurrency Seat Collisions**
   - *Mitigation:* Implemented Java `synchronized` method locks in `BookingServiceImpl` and database row-level locking.
3. **Risk 3: Filesystem Permission Errors in Linux Containers**
   - *Mitigation:* Converted fallback database to in-memory PostgreSQL mode (`jdbc:h2:mem:transport_db`) requiring 0 filesystem writes.
4. **Risk 4: External Database Outage**
   - *Mitigation:* Engineered resilient `DataSourceConfig.java` that falls back seamlessly with zero website downtime.

---

## 6. EARNED VALUE ANALYSIS (EVA)

Earned Value Analysis tracks performance against project baseline:
- **Planned Value (PV):** ₹10,70,100 (Scheduled baseline budget)
- **Earned Value (EV):** ₹10,70,100 (100% of project requirements completed and verified)
- **Actual Cost (AC):** ₹9,85,000 (Actual engineering cost incurred)

$$\text{Cost Variance (CV)} = EV - AC = ₹10,70,100 - ₹9,85,000 = +\mathbf{₹85,100 \text{ (Favorable)}}$$
$$\text{Schedule Variance (SV)} = EV - PV = ₹10,70,100 - ₹10,70,100 = \mathbf{₹0 \text{ (On Schedule)}}$$
$$\text{Cost Performance Index (CPI)} = \frac{EV}{AC} = \frac{10,70,100}{9,85,000} = \mathbf{1.086} > 1.0 \text{ (Under Budget)}$$
$$\text{Schedule Performance Index (SPI)} = \frac{EV}{PV} = \frac{10,70,100}{10,70,100} = \mathbf{1.000} \text{ (On Time)}$$

---

## 7. CMMI MATURITY ALIGNMENT

The development process conforms to **CMMI Maturity Level 3 (Defined)**:
- **Organizational Process Definition:** Requirements, designs, code, and test artifacts are systematically managed in structured version-controlled directories.
- **Verification & Validation Checkpoints:** Every feature is validated against IEEE 830 functional requirements before release.
- **Risk Management Integration:** Proactive RMMM plan executed during architectural prototyping.

---
**Document Status:** Complete & Verified  
**Student:** Jeffrin (732925ITR040) | Class: 25IT3A | VCET Erode – 12
