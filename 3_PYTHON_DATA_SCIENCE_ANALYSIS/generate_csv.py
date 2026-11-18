import csv
import random
from datetime import datetime, timedelta

routes = [
    {"source": "Erode", "dest": "Chennai Central", "dist": 420.0, "time": 450, "fare": 750.0},
    {"source": "Chennai Central", "dest": "Erode", "dist": 420.0, "time": 450, "fare": 750.0},
    {"source": "Erode", "dest": "Coimbatore", "dist": 100.5, "time": 120, "fare": 130.0},
    {"source": "Coimbatore", "dest": "Erode", "dist": 100.5, "time": 120, "fare": 130.0},
    {"source": "Erode", "dest": "Bengaluru", "dist": 260.0, "time": 330, "fare": 650.0},
    {"source": "Bengaluru", "dest": "Erode", "dist": 260.0, "time": 330, "fare": 650.0},
    {"source": "Salem", "dest": "Chennai Central", "dist": 345.0, "time": 380, "fare": 600.0},
    {"source": "Coimbatore", "dest": "Bengaluru", "dist": 360.0, "time": 420, "fare": 800.0},
    {"source": "Erode", "dest": "Madurai", "dist": 195.0, "time": 240, "fare": 260.0},
    {"source": "Madurai", "dest": "Erode", "dist": 195.0, "time": 240, "fare": 260.0},
    {"source": "Erode", "dest": "Tiruchirappalli", "dist": 145.0, "time": 180, "fare": 180.0},
    {"source": "Coimbatore", "dest": "Ooty", "dist": 85.0, "time": 180, "fare": 320.0}
]

bus_types = ["AC_SLEEPER", "SEMI_SLEEPER", "ULTRA_DELUXE", "NON_AC_SEATER"]
capacities = {"AC_SLEEPER": 30, "SEMI_SLEEPER": 36, "ULTRA_DELUXE": 40, "NON_AC_SEATER": 45}
operators = ["Kongu Express Transport", "Cheran Line Transits", "SETC Platinum Express", "Pandian Royal Route", "Nilgiri Mountain Rider"]

first_names = ["Jeffrin", "Anand", "Priya", "Karthik", "Deepa", "Vignesh", "Soundarya", "Saravanan", "Kavitha", "Manoj", "Suresh", "Divya", "Balaji", "Nithya", "Ramesh", "Swetha", "Arun", "Meena", "Ganesh", "Bhavani"]
last_names = ["Kumar", "Raja", "Dharshini", "Mohan", "Selvan", "Lakshmi", "Natarajan", "Sundaram", "Venkatesh", "Prakash", "Krishnan", "Chandran"]

random.seed(42)

start_date = datetime(2026, 11, 1)

rows = []
for i in range(1, 151):
    r = random.choice(routes)
    b_type = random.choice(bus_types)
    cap = capacities[b_type]
    b_date = start_date + timedelta(days=random.randint(0, 20), hours=random.randint(6, 23), minutes=random.choice([0, 15, 30, 45]))
    
    # Fare adjustment based on bus type
    multiplier = 1.25 if b_type == "AC_SLEEPER" else (1.1 if b_type == "SEMI_SLEEPER" else 1.0)
    seat_fare = round(r["fare"] * multiplier, 2)
    
    # Passenger count in booking (1 to 4)
    seats_booked = random.choices([1, 2, 3, 4], weights=[0.60, 0.25, 0.10, 0.05])[0]
    total_amount = round(seat_fare * seats_booked, 2)
    
    p_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    p_age = random.randint(18, 65)
    p_gender = random.choice(["MALE", "FEMALE"])
    p_phone = f"98{random.randint(10000000, 99999999)}"
    
    status = random.choices(["CONFIRMED", "CANCELLED"], weights=[0.92, 0.08])[0]
    payment = "PAID" if status == "CONFIRMED" else "REFUNDED"
    
    bus_reg = f"TN-{random.choice(['33', '38', '27', '01', '45'])}-N-{random.randint(1000, 9999)}"
    dep_time = b_date.strftime("%H:%M")
    
    # Occupancy simulated
    occupied_seats = random.randint(int(cap * 0.55), cap)
    occ_rate = round((occupied_seats / cap) * 100, 2)
    
    rows.append({
        "booking_id": f"TCK-2026-{1000 + i}",
        "booking_timestamp": b_date.strftime("%Y-%m-%d %H:%M:%S"),
        "travel_date": (b_date + timedelta(days=random.randint(1, 4))).strftime("%Y-%m-%d"),
        "departure_time": dep_time,
        "passenger_name": p_name,
        "passenger_age": p_age,
        "passenger_gender": p_gender,
        "passenger_phone": p_phone,
        "source_city": r["source"],
        "destination_city": r["dest"],
        "route_name": f"{r['source']} -> {r['dest']}",
        "distance_km": r["dist"],
        "bus_registration": bus_reg,
        "bus_type": b_type,
        "bus_capacity": cap,
        "seats_booked": seats_booked,
        "fare_per_seat": seat_fare,
        "total_amount": total_amount,
        "booking_status": status,
        "payment_status": payment,
        "occupancy_rate_pct": occ_rate
    })

fieldnames = list(rows[0].keys())
with open(r"d:\SEM PROJECT\3_PYTHON_DATA_SCIENCE_ANALYSIS\data\public_transport_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} records in public_transport_dataset.csv")
