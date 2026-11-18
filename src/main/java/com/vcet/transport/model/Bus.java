package com.vcet.transport.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Concrete Bus entity inheriting from abstract Vehicle.
 * Demonstrates Inheritance, Method Overriding, and JPA Annotations.
 */
@Entity
@Table(name = "buses")
public class Bus extends Vehicle {

    @Column(name = "bus_number", unique = true, nullable = false, length = 20)
    private String busNumber;

    @Enumerated(EnumType.STRING)
    @Column(name = "bus_type", nullable = false, length = 30)
    private BusType busType;

    @Column(name = "operator_name", length = 100)
    private String operatorName;

    @Column(name = "is_active")
    private boolean active = true;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public Bus() {
        super();
    }

    public Bus(String busNumber, BusType busType, int capacity, String operatorName) {
        super(busNumber, capacity);
        this.busNumber = busNumber;
        this.busType = busType;
        this.operatorName = operatorName;
    }

    public String getBusNumber() {
        return busNumber;
    }

    public void setBusNumber(String busNumber) {
        this.busNumber = busNumber;
        this.registrationNumber = busNumber;
    }

    public BusType getBusType() {
        return busType;
    }

    public void setBusType(BusType busType) {
        this.busType = busType;
    }

    public String getOperatorName() {
        return operatorName;
    }

    public void setOperatorName(String operatorName) {
        this.operatorName = operatorName;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    @Override
    public String getVehicleCategoryDescription() {
        return "Public Transport Bus [" + busNumber + "] - " + (busType != null ? busType.getDisplayName() : "Standard") + " (Capacity: " + capacity + ")";
    }
}
