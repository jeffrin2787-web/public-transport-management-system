"""
================================================================================
INSTANT ZERO-CONFIG LOCAL PREVIEW SERVER (PORT 8080)
PROJECT: Public Transport Management and Passenger Travel Analysis System
VELALAR COLLEGE OF ENGINEERING AND TECHNOLOGY, ERODE - 12
AUTHOR: Jeffrin (Reg No: 732925ITR040) | CLASS: 25IT3A
================================================================================
This script starts a local HTTP server on port 8080 serving the exact same
REST APIs and Web UI as the Java Spring Boot application.
Use this for instant 1-click local testing and demonstration.
================================================================================
"""

import http.server
import socketserver
import json
import os
import re
from datetime import datetime, date

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "src", "main", "resources", "static")

# In-memory realistic database for instant preview
buses = [
    {"id": 1, "busNumber": "TN-33-N-2410", "busType": "AC_SLEEPER", "capacity": 30, "operatorName": "Kongu Express Transport"},
    {"id": 2, "busNumber": "TN-33-N-2845", "busType": "SEMI_SLEEPER", "capacity": 36, "operatorName": "Kongu Express Transport"},
    {"id": 3, "busNumber": "TN-38-N-3120", "busType": "ULTRA_DELUXE", "capacity": 40, "operatorName": "Cheran Line Transits"},
    {"id": 4, "busNumber": "TN-27-N-1890", "busType": "AC_SLEEPER", "capacity": 30, "operatorName": "Salem City Express"},
    {"id": 5, "busNumber": "TN-01-AN-6701", "busType": "SEMI_SLEEPER", "capacity": 36, "operatorName": "SETC Platinum Express"},
    {"id": 6, "busNumber": "TN-58-N-4422", "busType": "ULTRA_DELUXE", "capacity": 40, "operatorName": "Pandian Royal Route"},
    {"id": 7, "busNumber": "TN-45-N-5110", "busType": "NON_AC_SEATER", "capacity": 45, "operatorName": "Cholan Intercity Direct"},
    {"id": 8, "busNumber": "TN-43-N-1008", "busType": "AC_SLEEPER", "capacity": 28, "operatorName": "Nilgiri Mountain Rider"}
]

routes = [
    {"id": 1, "sourceCity": "Erode", "destinationCity": "Chennai Central", "distanceKm": 420.0, "estimatedDurationMinutes": 450},
    {"id": 2, "sourceCity": "Chennai Central", "destinationCity": "Erode", "distanceKm": 420.0, "estimatedDurationMinutes": 450},
    {"id": 3, "sourceCity": "Erode", "destinationCity": "Coimbatore", "distanceKm": 100.5, "estimatedDurationMinutes": 120},
    {"id": 4, "sourceCity": "Coimbatore", "destinationCity": "Erode", "distanceKm": 100.5, "estimatedDurationMinutes": 120},
    {"id": 5, "sourceCity": "Erode", "destinationCity": "Bengaluru", "distanceKm": 260.0, "estimatedDurationMinutes": 330},
    {"id": 6, "sourceCity": "Bengaluru", "destinationCity": "Erode", "distanceKm": 260.0, "estimatedDurationMinutes": 330},
    {"id": 7, "sourceCity": "Salem", "destinationCity": "Chennai Central", "distanceKm": 345.0, "estimatedDurationMinutes": 380},
    {"id": 8, "sourceCity": "Coimbatore", "destinationCity": "Bengaluru", "distanceKm": 360.0, "estimatedDurationMinutes": 420},
    {"id": 9, "sourceCity": "Erode", "destinationCity": "Madurai", "distanceKm": 195.0, "estimatedDurationMinutes": 240},
    {"id": 10, "sourceCity": "Erode", "destinationCity": "Tiruchirappalli", "distanceKm": 145.0, "estimatedDurationMinutes": 180},
    {"id": 11, "sourceCity": "Coimbatore", "destinationCity": "Ooty", "distanceKm": 85.0, "estimatedDurationMinutes": 180}
]

today_str = date.today().isoformat()
schedules = [
    {"id": 1, "bus": buses[0], "route": routes[0], "travelDate": today_str, "departureTime": "21:30:00", "arrivalTime": "05:00:00", "baseFare": 750.0, "availableSeats": 26},
    {"id": 2, "bus": buses[1], "route": routes[0], "travelDate": today_str, "departureTime": "22:15:00", "arrivalTime": "05:45:00", "baseFare": 550.0, "availableSeats": 32},
    {"id": 3, "bus": buses[2], "route": routes[2], "travelDate": today_str, "departureTime": "07:00:00", "arrivalTime": "09:00:00", "baseFare": 120.0, "availableSeats": 37},
    {"id": 4, "bus": buses[3], "route": routes[4], "travelDate": today_str, "departureTime": "23:00:00", "arrivalTime": "04:30:00", "baseFare": 650.0, "availableSeats": 28},
    {"id": 5, "bus": buses[4], "route": routes[1], "travelDate": today_str, "departureTime": "22:00:00", "arrivalTime": "05:30:00", "baseFare": 550.0, "availableSeats": 36},
    {"id": 6, "bus": buses[5], "route": routes[8], "travelDate": today_str, "departureTime": "14:30:00", "arrivalTime": "18:30:00", "baseFare": 250.0, "availableSeats": 39},
    {"id": 7, "bus": buses[7], "route": routes[10], "travelDate": today_str, "departureTime": "06:30:00", "arrivalTime": "09:30:00", "baseFare": 320.0, "availableSeats": 26}
]

bookings = [
    {
        "id": 1,
        "pnrNumber": "TCK-2026-1001",
        "schedule": schedules[0],
        "passenger": {"fullName": "Jeffrin", "age": 20, "gender": "MALE", "phoneNumber": "9876543210", "email": "jeffrin@vcet.ac.in"},
        "bookingTime": "2026-11-18T10:00:00",
        "totalAmount": 1500.0,
        "status": "CONFIRMED",
        "paymentStatus": "PAID",
        "tickets": [{"seatNumber": 1, "seatFare": 750.0}, {"seatNumber": 2, "seatFare": 750.0}]
    },
    {
        "id": 2,
        "pnrNumber": "TCK-2026-1002",
        "schedule": schedules[0],
        "passenger": {"fullName": "Anand Kumar", "age": 28, "gender": "MALE", "phoneNumber": "9842156789", "email": "anand.k@gmail.com"},
        "bookingTime": "2026-11-18T11:00:00",
        "totalAmount": 1500.0,
        "status": "CONFIRMED",
        "paymentStatus": "PAID",
        "tickets": [{"seatNumber": 5, "seatFare": 750.0}, {"seatNumber": 6, "seatFare": 750.0}]
    }
]

booked_seats_map = {1: [1, 2, 5, 6], 2: [3, 4], 3: [7, 8, 9], 4: [11, 12], 6: [15], 7: [1, 2]}
pnr_counter = 1005

class TransportHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        url = self.path.split("?")[0]

        if url == "/api/cities":
            self.send_json({
                "sources": sorted(list(set(r["sourceCity"] for r in routes))),
                "destinations": sorted(list(set(r["destinationCity"] for r in routes)))
            })
            return

        if url == "/api/schedules/search":
            self.send_json(schedules)
            return

        m_sched = re.match(r"^/api/schedules/(\d+)$", url)
        if m_sched:
            sid = int(m_sched.group(1))
            found = next((s for s in schedules if s["id"] == sid), None)
            if found:
                self.send_json(found)
            else:
                self.send_error(404, "Schedule not found")
            return

        m_seats = re.match(r"^/api/schedules/(\d+)/seats$", url)
        if m_seats:
            sid = int(m_seats.group(1))
            sched = next((s for s in schedules if s["id"] == sid), None)
            if sched:
                b_seats = booked_seats_map.get(sid, [])
                self.send_json({
                    "scheduleId": sid,
                    "busType": sched["bus"]["busType"],
                    "totalCapacity": sched["bus"]["capacity"],
                    "availableSeatsCount": sched["availableSeats"],
                    "bookedSeats": b_seats,
                    "baseFare": sched["baseFare"]
                })
            else:
                self.send_error(404, "Schedule not found")
            return

        m_pnr = re.match(r"^/api/bookings/([A-Za-z0-9\-]+)$", url)
        if m_pnr:
            pnr = m_pnr.group(1).upper()
            found = next((b for b in bookings if b["pnrNumber"] == pnr), None)
            if found:
                self.send_json(found)
            else:
                self.send_error(404, "Booking not found")
            return

        if url == "/api/admin/buses":
            self.send_json(buses)
            return

        if url == "/api/admin/routes":
            self.send_json(routes)
            return

        if url == "/api/admin/bookings":
            self.send_json(list(reversed(bookings)))
            return

        if url == "/api/db/all-tables":
            # Flatten relational tables for inspection
            tbl_buses = [{"bus_id": b["id"], "bus_number": b["busNumber"], "bus_type": b["busType"], "total_capacity": b["capacity"], "operator_name": b["operatorName"]} for b in buses]
            tbl_routes = [{"route_id": r["id"], "source_city": r["sourceCity"], "destination_city": r["destinationCity"], "distance_km": r["distanceKm"], "estimated_duration_minutes": r["estimatedDurationMinutes"]} for r in routes]
            tbl_schedules = [{"schedule_id": s["id"], "bus_number": s["bus"]["busNumber"], "corridor": f"{s['route']['sourceCity']} -> {s['route']['destinationCity']}", "travel_date": s["travelDate"], "departure_time": s["departureTime"], "arrival_time": s["arrivalTime"], "base_fare": s["baseFare"], "available_seats": s["availableSeats"], "status": "SCHEDULED"} for s in schedules]
            
            seen_passengers = {}
            tbl_passengers = []
            for b in bookings:
                p = b["passenger"]
                ph = p["phoneNumber"]
                if ph not in seen_passengers:
                    pid = len(seen_passengers) + 1
                    seen_passengers[ph] = pid
                    tbl_passengers.append({
                        "passenger_id": pid,
                        "full_name": p["fullName"],
                        "age": p["age"],
                        "gender": p["gender"],
                        "phone_number": ph,
                        "email": p.get("email", "-")
                    })

            tbl_bookings = []
            tbl_tickets = []
            t_counter = 1
            for b in bookings:
                pid = seen_passengers.get(b["passenger"]["phoneNumber"], 1)
                tbl_bookings.append({
                    "booking_id": b["id"],
                    "pnr_number": b["pnrNumber"],
                    "schedule_id": b["schedule"]["id"],
                    "passenger_id": pid,
                    "passenger_name": b["passenger"]["fullName"],
                    "booking_time": b["bookingTime"],
                    "total_amount": b["totalAmount"],
                    "status": b["status"],
                    "payment_status": b["paymentStatus"]
                })
                for t in b["tickets"]:
                    tbl_tickets.append({
                        "ticket_id": t_counter,
                        "ticket_number": f"T-{b['pnrNumber'].replace('TCK-', '')}-S{t['seatNumber']:02d}",
                        "booking_id": b["id"],
                        "seat_number": t["seatNumber"],
                        "seat_fare": t["seatFare"],
                        "status": b["status"]
                    })
                    t_counter += 1

            self.send_json({
                "buses": tbl_buses,
                "routes": tbl_routes,
                "schedules": tbl_schedules,
                "passengers": tbl_passengers,
                "bookings": tbl_bookings,
                "tickets": tbl_tickets
            })
            return

        if url == "/api/reports/summary":
            confirmed = [b for b in bookings if b["status"] == "CONFIRMED"]
            rev = sum(b["totalAmount"] for b in confirmed)
            self.send_json({
                "totalBookings": len(bookings),
                "confirmedBookings": len(confirmed),
                "cancelledBookings": len(bookings) - len(confirmed),
                "totalRevenue": rev,
                "averageOccupancyRate": 78.5,
                "activeSchedulesCount": len(schedules)
            })
            return

        if url == "/api/reports/route-revenue":
            rev_map = {}
            for b in bookings:
                if b["status"] == "CONFIRMED":
                    r_name = f"{b['schedule']['route']['sourceCity']} -> {b['schedule']['route']['destinationCity']}"
                    rev_map[r_name] = rev_map.get(r_name, 0.0) + b["totalAmount"]
            res = [{"route": k, "totalRevenue": v, "bookingCount": 1} for k, v in rev_map.items()]
            self.send_json(res)
            return

        if url == "/api/reports/occupancy":
            res = []
            for s in schedules:
                cap = s["bus"]["capacity"]
                booked = cap - s["availableSeats"]
                pct = round((booked / cap) * 100, 2)
                res.append({
                    "scheduleId": s["id"],
                    "busNumber": s["bus"]["busNumber"],
                    "busType": s["bus"]["busType"],
                    "corridor": f"{s['route']['sourceCity']} -> {s['route']['destinationCity']}",
                    "capacity": cap,
                    "bookedSeats": booked,
                    "availableSeats": s["availableSeats"],
                    "occupancyPercentage": pct
                })
            self.send_json(res)
            return

        if url == "/api/reports/chart-data":
            # Real-time recalculated metrics
            route_demand = {}
            route_revenue = {}
            for b in bookings:
                if b["status"] == "CONFIRMED":
                    r_name = f"{b['schedule']['route']['sourceCity']} -> {b['schedule']['route']['destinationCity']}"
                    seats_cnt = len(b["tickets"])
                    route_demand[r_name] = route_demand.get(r_name, 0) + seats_cnt
                    route_revenue[r_name] = route_revenue.get(r_name, 0.0) + b["totalAmount"]

            # Occupancy by bus type
            occ_by_type = {}
            for s in schedules:
                bt = s["bus"]["busType"]
                cap = s["bus"]["capacity"]
                occ = round(((cap - s["availableSeats"]) / cap) * 100, 1)
                occ_by_type.setdefault(bt, []).append(occ)

            bus_types = list(occ_by_type.keys())
            bus_type_avgs = [round(sum(occ_by_type[bt]) / len(occ_by_type[bt]), 1) for bt in bus_types]

            conf = sum(1 for b in bookings if b["status"] == "CONFIRMED")
            canc = sum(1 for b in bookings if b["status"] == "CANCELLED")

            self.send_json({
                "routeLabels": list(route_demand.keys()) if route_demand else ["Erode -> Chennai Central", "Erode -> Coimbatore"],
                "routeDemandData": list(route_demand.values()) if route_demand else [4, 2],
                "routeRevenueData": list(route_revenue.values()) if route_revenue else [3000, 240],
                "busTypeLabels": bus_types,
                "busTypeOccupancyData": bus_type_avgs,
                "statusLabels": ["Confirmed", "Cancelled"],
                "statusData": [conf, canc],
                "dailyLabels": [today_str],
                "dailyData": [conf]
            })
            return

        # Fallback to static files
        super().do_GET()

    def do_POST(self):
        url = self.path.split("?")[0]
        length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(length).decode('utf-8') if length > 0 else "{}"
        data = json.loads(body) if body else {}

        if url == "/api/bookings":
            global pnr_counter
            sid = data.get("scheduleId")
            seats = data.get("seatNumbers", [])
            sched = next((s for s in schedules if s["id"] == sid), None)
            if not sched:
                self.send_error(404, "Schedule not found")
                return

            # Check conflict
            current_booked = set(booked_seats_map.get(sid, []))
            for st in seats:
                if st in current_booked:
                    self.send_json({"message": f"Seat {st} is already booked!"}, status=409)
                    return

            # Book seats
            current_booked.update(seats)
            booked_seats_map[sid] = list(current_booked)
            sched["availableSeats"] -= len(seats)

            pnr_counter += 1
            pnr = f"TCK-2026-{pnr_counter}"
            total = sched["baseFare"] * len(seats)

            new_booking = {
                "id": len(bookings) + 1,
                "pnrNumber": pnr,
                "schedule": sched,
                "passenger": {
                    "fullName": data.get("fullName"),
                    "age": data.get("age"),
                    "gender": data.get("gender"),
                    "phoneNumber": data.get("phoneNumber"),
                    "email": data.get("email")
                },
                "bookingTime": datetime.now().isoformat(),
                "totalAmount": total,
                "status": "CONFIRMED",
                "paymentStatus": "PAID",
                "tickets": [{"seatNumber": s, "seatFare": sched["baseFare"]} for s in seats]
            }
            bookings.append(new_booking)
            self.send_json(new_booking, status=201)
            return

        m_cancel = re.match(r"^/api/bookings/cancel/([A-Za-z0-9\-]+)$", url)
        if m_cancel:
            pnr = m_cancel.group(1).upper()
            found = next((b for b in bookings if b["pnrNumber"] == pnr), None)
            if not found:
                self.send_error(404, "Booking not found")
                return

            if found["status"] == "CANCELLED":
                self.send_json({"message": "Booking is already cancelled"}, status=400)
                return

            found["status"] = "CANCELLED"
            found["paymentStatus"] = "REFUNDED"
            sid = found["schedule"]["id"]
            released = [t["seatNumber"] for t in found["tickets"]]
            
            # release seats
            if sid in booked_seats_map:
                booked_seats_map[sid] = [s for s in booked_seats_map[sid] if s not in released]
            found["schedule"]["availableSeats"] += len(released)

            self.send_json({
                "message": "Booking cancelled successfully. Seats released back to inventory.",
                "pnr": pnr,
                "status": "CANCELLED",
                "refundAmount": found["totalAmount"]
            })
            return

        if url == "/api/admin/buses":
            new_bus = {
                "id": len(buses) + 1,
                "busNumber": data.get("busNumber"),
                "busType": data.get("busType"),
                "capacity": data.get("capacity"),
                "operatorName": data.get("operatorName", "Tamil Nadu State Express")
            }
            buses.append(new_bus)
            self.send_json(new_bus, status=201)
            return

        if url == "/api/admin/routes":
            new_route = {
                "id": len(routes) + 1,
                "sourceCity": data.get("sourceCity"),
                "destinationCity": data.get("destinationCity"),
                "distanceKm": data.get("distanceKm"),
                "estimatedDurationMinutes": data.get("estimatedDurationMinutes")
            }
            routes.append(new_route)
            self.send_json(new_route, status=201)
            return

        self.send_error(404, "Endpoint not found")

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    print(f"==================================================================")
    print(f"  PUBLIC TRANSPORT MANAGEMENT & PASSENGER TRAVEL ANALYSIS SYSTEM  ")
    print(f"  VELALAR COLLEGE OF ENGINEERING AND TECHNOLOGY, ERODE - 12       ")
    print(f"  AUTHOR: JEFFRIN | REG NO: 732925ITR040 | CLASS: 25IT3A          ")
    print(f"  STARTING LOCAL PREVIEW SERVER AT: http://localhost:{PORT}       ")
    print(f"==================================================================")
    with socketserver.TCPServer(("", PORT), TransportHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Server stopped gracefully.")
