package com.vcet.transport.model;

import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;

/**
 * Abstract Vehicle entity demonstrating OOP Inheritance (Unit 2: 25ITT32).
 */
@MappedSuperclass
public abstract class Vehicle {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    protected Long id;

    protected String registrationNumber;
    protected int capacity;

    public Vehicle() {
    }

    public Vehicle(String registrationNumber, int capacity) {
        this.registrationNumber = registrationNumber;
        this.capacity = capacity;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getRegistrationNumber() {
        return registrationNumber;
    }

    public void setRegistrationNumber(String registrationNumber) {
        this.registrationNumber = registrationNumber;
    }

    public int getCapacity() {
        return capacity;
    }

    public void setCapacity(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("Capacity must be greater than zero.");
        }
        this.capacity = capacity;
    }

    // Abstract method to be implemented by subclasses
    public abstract String getVehicleCategoryDescription();
}
