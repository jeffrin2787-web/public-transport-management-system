/**
 * Public Transport Management System - Main Interactive Frontend Logic
 * Author: Jeffrin (Reg No: 732925ITR040) | VCET IT Dept
 */

const API_BASE = "/api";

let selectedSchedule = null;
let selectedSeats = [];

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
    loadCities();
    loadSchedules();
});

// Load distinct cities for search dropdowns
async function loadCities() {
    try {
        const res = await fetch(`${API_BASE}/cities`);
        if (!res.ok) return;
        const data = await res.json();

        const srcSelect = document.getElementById("searchSource");
        const destSelect = document.getElementById("searchDestination");

        if (srcSelect && data.sources) {
            data.sources.forEach(city => {
                const opt = document.createElement("option");
                opt.value = city;
                opt.textContent = city;
                srcSelect.appendChild(opt);
            });
        }

        if (destSelect && data.destinations) {
            data.destinations.forEach(city => {
                const opt = document.createElement("option");
                opt.value = city;
                opt.textContent = city;
                destSelect.appendChild(opt);
            });
        }
    } catch (err) {
        console.error("Failed to load cities:", err);
    }
}

// Search and render schedules
async function loadSchedules(source = "", destination = "", date = "") {
    const listContainer = document.getElementById("scheduleList");
    if (!listContainer) return;

    listContainer.innerHTML = `
        <div style="text-align: center; padding: 3rem; color: #64748b;">
            <i class="fas fa-spinner fa-spin fa-2x"></i>
            <p style="margin-top: 0.75rem;">Loading active bus schedules...</p>
        </div>
    `;

    try {
        let url = `${API_BASE}/schedules/search`;
        const params = new URLSearchParams();
        if (source) params.append("source", source);
        if (destination) params.append("destination", destination);
        if (date) params.append("date", date);

        if (params.toString()) {
            url += `?${params.toString()}`;
        }

        const res = await fetch(url);
        const schedules = await res.json();

        if (!schedules || schedules.length === 0) {
            listContainer.innerHTML = `
                <div style="text-align: center; padding: 3rem; background: #ffffff; border-radius: 12px; border: 1px dashed #cbd5e1;">
                    <i class="fas fa-bus-slash fa-3x" style="color: #94a3b8; margin-bottom: 1rem;"></i>
                    <h3 style="font-weight: 700; color: #334155;">No buses found for this route or date</h3>
                    <p style="color: #64748b; margin-top: 0.5rem;">Try selecting a different corridor like Erode to Chennai Central or Coimbatore.</p>
                </div>
            `;
            return;
        }

        listContainer.innerHTML = schedules.map(s => {
            const avail = s.availableSeats;
            const badgeClass = avail > 10 ? "available" : (avail > 0 ? "filling-fast" : "sold-out");
            const badgeText = avail > 0 ? `${avail} Seats Left` : "Sold Out";

            return `
                <div class="bus-card">
                    <div>
                        <div class="operator-name">${s.bus.operatorName || "Express Line"}</div>
                        <div class="bus-type-badge">${s.bus.busType ? s.bus.busType.replace('_', ' ') : 'Express'}</div>
                        <div class="bus-number"><i class="fas fa-id-card"></i> ${s.bus.busNumber}</div>
                    </div>

                    <div class="timeline">
                        <div class="time-box">
                            <h4>${s.departureTime.substring(0, 5)}</h4>
                            <span>${s.route.sourceCity}</span>
                        </div>
                        <div class="duration-line">
                            <div class="duration-text">${s.route.distanceKm} km</div>
                            <div class="line-bar"></div>
                            <div class="duration-text">${s.travelDate}</div>
                        </div>
                        <div class="time-box">
                            <h4>${s.arrivalTime.substring(0, 5)}</h4>
                            <span>${s.route.destinationCity}</span>
                        </div>
                    </div>

                    <div class="fare-box">
                        <div class="fare-amount">₹${s.baseFare.toFixed(2)}</div>
                        <div class="fare-subtext">per seat</div>
                        <span class="seats-badge ${badgeClass}">${badgeText}</span>
                    </div>

                    <div style="text-align: right;">
                        <button class="btn-primary" onclick="openSeatModal(${s.id})" ${avail === 0 ? "disabled style='opacity: 0.5; cursor: not-allowed;'" : ""}>
                            <i class="fas fa-chair"></i> Select Seats
                        </button>
                    </div>
                </div>
            `;
        }).join("");

    } catch (err) {
        listContainer.innerHTML = `
            <div style="padding: 2rem; background: #fee2e2; border-radius: 8px; color: #b91c1c;">
                <strong>Error:</strong> Failed to fetch bus schedules. Please verify that the backend server is running.
            </div>
        `;
    }
}

// Search form submit handler
function handleSearch(e) {
    e.preventDefault();
    const source = document.getElementById("searchSource").value;
    const dest = document.getElementById("searchDestination").value;
    const date = document.getElementById("searchDate").value;
    loadSchedules(source, dest, date);
}

// Open visual seat selector modal
async function openSeatModal(scheduleId) {
    selectedSeats = [];
    try {
        const [schedRes, seatsRes] = await Promise.all([
            fetch(`${API_BASE}/schedules/${scheduleId}`),
            fetch(`${API_BASE}/schedules/${scheduleId}/seats`)
        ]);

        selectedSchedule = await schedRes.json();
        const seatData = await seatsRes.json();

        document.getElementById("modalRoute").textContent = `${selectedSchedule.route.sourceCity} to ${selectedSchedule.route.destinationCity}`;
        document.getElementById("modalBusInfo").textContent = `${selectedSchedule.bus.busNumber} (${selectedSchedule.bus.busType}) | Base Fare: ₹${selectedSchedule.baseFare.toFixed(2)}`;

        const seatGrid = document.getElementById("seatGrid");
        seatGrid.innerHTML = "";

        const bookedSet = new Set(seatData.bookedSeats || []);
        const totalCap = seatData.totalCapacity || 30;

        for (let i = 1; i <= totalCap; i++) {
            const seatDiv = document.createElement("div");
            seatDiv.classList.add("seat");
            seatDiv.dataset.seatNumber = i;
            seatDiv.textContent = i;

            if (bookedSet.has(i)) {
                seatDiv.classList.add("booked");
                seatDiv.title = `Seat #${i} is already booked`;
            } else {
                seatDiv.title = `Seat #${i} - Click to select`;
                seatDiv.onclick = () => toggleSeatSelection(i, seatDiv);
            }
            seatGrid.appendChild(seatDiv);
        }

        updateBookingSummary();
        document.getElementById("seatModal").classList.add("active");

    } catch (err) {
        alert("Could not load seat map: " + err.message);
    }
}

function toggleSeatSelection(seatNum, element) {
    const idx = selectedSeats.indexOf(seatNum);
    if (idx > -1) {
        selectedSeats.splice(idx, 1);
        element.classList.remove("selected");
    } else {
        selectedSeats.push(seatNum);
        element.classList.add("selected");
    }
    updateBookingSummary();
}

function updateBookingSummary() {
    const seatDisplay = document.getElementById("selectedSeatsDisplay");
    const fareDisplay = document.getElementById("totalFareDisplay");
    const bookBtn = document.getElementById("confirmBookingBtn");

    if (selectedSeats.length === 0) {
        seatDisplay.textContent = "None selected";
        fareDisplay.textContent = "₹0.00";
        if (bookBtn) bookBtn.disabled = true;
    } else {
        selectedSeats.sort((a, b) => a - b);
        seatDisplay.textContent = selectedSeats.join(", ");
        const total = selectedSeats.length * (selectedSchedule ? selectedSchedule.baseFare : 0);
        fareDisplay.textContent = `₹${total.toFixed(2)} (${selectedSeats.length} seat${selectedSeats.length > 1 ? 's' : ''})`;
        if (bookBtn) bookBtn.disabled = false;
    }
}

function closeSeatModal() {
    document.getElementById("seatModal").classList.remove("active");
    selectedSchedule = null;
    selectedSeats = [];
}

// Confirm booking submission
async function handleBookingSubmit(e) {
    e.preventDefault();
    if (!selectedSchedule || selectedSeats.length === 0) {
        alert("Please select at least one seat.");
        return;
    }

    const payload = {
        scheduleId: selectedSchedule.id,
        seatNumbers: selectedSeats,
        fullName: document.getElementById("passName").value.trim(),
        age: parseInt(document.getElementById("passAge").value, 10),
        gender: document.getElementById("passGender").value,
        phoneNumber: document.getElementById("passPhone").value.trim(),
        email: document.getElementById("passEmail").value.trim()
    };

    const bookBtn = document.getElementById("confirmBookingBtn");
    bookBtn.disabled = true;
    bookBtn.innerHTML = "<i class='fas fa-spinner fa-spin'></i> Reserving...";

    try {
        const res = await fetch(`${API_BASE}/bookings`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.message || "Booking failed");
        }

        const booking = await res.json();
        closeSeatModal();

        // Show ticket confirmation modal
        showTicketConfirmation(booking);

        // Reload schedules to update available seats count
        loadSchedules();

    } catch (err) {
        alert("Booking Error: " + err.message);
    } finally {
        bookBtn.disabled = false;
        bookBtn.innerHTML = "<i class='fas fa-check-circle'></i> Confirm & Pay";
    }
}

// Show ticket modal
function showTicketConfirmation(b) {
    const confModal = document.getElementById("ticketModal");
    if (!confModal) {
        alert(`Booking Confirmed!\nYour PNR: ${b.pnrNumber}\nSeats: ${b.tickets.map(t => t.seatNumber).join(', ')}`);
        return;
    }

    document.getElementById("ticketPnr").textContent = b.pnrNumber;
    document.getElementById("ticketPassenger").textContent = b.passenger.fullName;
    document.getElementById("ticketRoute").textContent = `${b.schedule.route.sourceCity} to ${b.schedule.route.destinationCity}`;
    document.getElementById("ticketDate").textContent = `${b.schedule.travelDate} at ${b.schedule.departureTime.substring(0, 5)}`;
    document.getElementById("ticketSeats").textContent = b.tickets.map(t => t.seatNumber).join(", ");
    document.getElementById("ticketAmount").textContent = `₹${b.totalAmount.toFixed(2)}`;

    confModal.classList.add("active");
}

function closeTicketModal() {
    const confModal = document.getElementById("ticketModal");
    if (confModal) confModal.classList.remove("active");
}
