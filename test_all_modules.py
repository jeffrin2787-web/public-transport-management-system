"""
Module Verification Test Suite
Tests every single user option, business logic rule, and API endpoint.
"""
import json
import urllib.request
import urllib.parse
from datetime import date
import threading
import time
import sys

# Import the server components
import run_preview_server

def run_tests():
    print("==================================================================")
    print("  COMPREHENSIVE MODULE TEST & VERIFICATION SUITE                  ")
    print("==================================================================")

    # 1. Start test server in background thread on port 8085
    test_port = 8085
    run_preview_server.PORT = test_port
    server = run_preview_server.socketserver.TCPServer(("127.0.0.1", test_port), run_preview_server.TransportHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.5)

    base = f"http://127.0.0.1:{test_port}"
    passed = 0
    total = 0

    def check(name, condition):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {name}")
        else:
            print(f"[FAIL] {name}")

    try:
        # TEST 1: Cities API
        req = urllib.request.urlopen(f"{base}/api/cities")
        cities = json.loads(req.read().decode())
        check("Cities API returns sources and destinations", "sources" in cities and len(cities["sources"]) > 0)

        # TEST 2: Schedules Search API
        req = urllib.request.urlopen(f"{base}/api/schedules/search")
        schedules = json.loads(req.read().decode())
        check("Schedules Search returns active trips", len(schedules) > 0)
        first_sched = schedules[0]
        sid = first_sched["id"]

        # TEST 3: Seat Availability API
        req = urllib.request.urlopen(f"{base}/api/schedules/{sid}/seats")
        seat_data = json.loads(req.read().decode())
        check("Seat Availability returns total capacity and booked seats", "bookedSeats" in seat_data and seat_data["totalCapacity"] > 0)

        # Find an unbooked seat
        booked_set = set(seat_data["bookedSeats"])
        free_seat = None
        for s in range(1, seat_data["totalCapacity"] + 1):
            if s not in booked_set:
                free_seat = s
                break

        check("Found unreserved seat for booking test", free_seat is not None)

        # TEST 4: Create Booking Transaction (Reserve Seat)
        payload = {
            "scheduleId": sid,
            "seatNumbers": [free_seat],
            "fullName": "Test Verifier",
            "age": 22,
            "gender": "MALE",
            "phoneNumber": "9988776655",
            "email": "test@vcet.ac.in"
        }
        req = urllib.request.Request(
            f"{base}/api/bookings",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(req)
        booking = json.loads(resp.read().decode())
        check("Booking created successfully (HTTP 201)", resp.status == 201 and "pnrNumber" in booking)
        pnr = booking["pnrNumber"]

        # TEST 5: Track PNR
        req = urllib.request.urlopen(f"{base}/api/bookings/{pnr}")
        tracked = json.loads(req.read().decode())
        check("Track PNR retrieves valid confirmed booking", tracked["pnrNumber"] == pnr and tracked["status"] == "CONFIRMED")

        # TEST 6: Overbooking / Double Booking Prevention
        try:
            req_dup = urllib.request.Request(
                f"{base}/api/bookings",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            urllib.request.urlopen(req_dup)
            check("Double booking prevented on same seat", False)
        except urllib.error.HTTPError as e:
            check("Double booking prevented with HTTP 409 Conflict", e.code == 409)

        # TEST 7: Live Chart Data API
        req = urllib.request.urlopen(f"{base}/api/reports/chart-data")
        chart_data = json.loads(req.read().decode())
        check("Live Chart Data contains routeDemand and routeRevenue", "routeDemandData" in chart_data and len(chart_data["routeDemandData"]) > 0)
        check("Live Chart Data contains busTypeOccupancy and statusData", "busTypeOccupancyData" in chart_data and "statusData" in chart_data)

        # TEST 8: Cancel Ticket & Release Seat
        req_cancel = urllib.request.Request(f"{base}/api/bookings/cancel/{pnr}", data=b"", method="POST")
        resp_cancel = urllib.request.urlopen(req_cancel)
        cancel_data = json.loads(resp_cancel.read().decode())
        check("Ticket cancellation succeeds", cancel_data["status"] == "CANCELLED")

        # TEST 9: Verify Seat was Released Back to Inventory
        req_seats_after = urllib.request.urlopen(f"{base}/api/schedules/{sid}/seats")
        seats_after = json.loads(req_seats_after.read().decode())
        check("Cancelled seat is no longer in bookedSeats list", free_seat not in seats_after["bookedSeats"])

        # TEST 10: Reports Summary KPI API
        req_kpi = urllib.request.urlopen(f"{base}/api/reports/summary")
        kpi = json.loads(req_kpi.read().decode())
        check("Reports Summary returns totalBookings and totalRevenue", kpi["totalBookings"] > 0 and "totalRevenue" in kpi)

        # TEST 11: Route Revenue Report API
        req_rev = urllib.request.urlopen(f"{base}/api/reports/route-revenue")
        rev_list = json.loads(req_rev.read().decode())
        check("Route Revenue Report returns non-empty list", len(rev_list) > 0)

        # TEST 12: Occupancy Report API
        req_occ = urllib.request.urlopen(f"{base}/api/reports/occupancy")
        occ_list = json.loads(req_occ.read().decode())
        check("Occupancy Report returns list of schedules", len(occ_list) > 0)

        # TEST 13: Admin Register Bus API
        bus_payload = {
            "busNumber": "TN-TEST-9999",
            "busType": "AC_SLEEPER",
            "capacity": 30,
            "operatorName": "VCET Test Fleet"
        }
        req_bus = urllib.request.Request(
            f"{base}/api/admin/buses",
            data=json.dumps(bus_payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp_bus = urllib.request.urlopen(req_bus)
        check("Admin can register new bus", resp_bus.status == 201)

        # TEST 14: Admin Create Route API
        route_payload = {
            "sourceCity": "Erode",
            "destinationCity": "Dindigul",
            "distanceKm": 140.0,
            "estimatedDurationMinutes": 160
        }
        req_route = urllib.request.Request(
            f"{base}/api/admin/routes",
            data=json.dumps(route_payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp_route = urllib.request.urlopen(req_route)
        check("Admin can create new transit route corridor", resp_route.status == 201)

        # TEST 15: Admin Master Bookings Audit API
        req_admin_bkg = urllib.request.urlopen(f"{base}/api/admin/bookings")
        admin_bkgs = json.loads(req_admin_bkg.read().decode())
        check("Admin Master Bookings returns audit trail", len(admin_bkgs) > 0)

        print("------------------------------------------------------------------")
        print(f"  TEST VERIFICATION COMPLETED: {passed}/{total} TESTS PASSED ({passed*100//total}%)")
        print("==================================================================")

    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    run_tests()
