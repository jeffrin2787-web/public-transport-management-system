package com.vcet.transport.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Route entity representing transit corridors across Tamil Nadu and South India.
 */
@Entity
@Table(name = "routes", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"source_city", "destination_city"})
})
public class Route {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "route_id")
    private Long id;

    @Column(name = "source_city", nullable = false, length = 50)
    private String sourceCity;

    @Column(name = "destination_city", nullable = false, length = 50)
    private String destinationCity;

    @Column(name = "distance_km", nullable = false)
    private double distanceKm;

    @Column(name = "estimated_duration_minutes", nullable = false)
    private int estimatedDurationMinutes;

    @Column(name = "is_active")
    private boolean active = true;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public Route() {
    }

    public Route(String sourceCity, String destinationCity, double distanceKm, int estimatedDurationMinutes) {
        this.sourceCity = sourceCity;
        this.destinationCity = destinationCity;
        this.distanceKm = distanceKm;
        this.estimatedDurationMinutes = estimatedDurationMinutes;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getSourceCity() {
        return sourceCity;
    }

    public void setSourceCity(String sourceCity) {
        this.sourceCity = sourceCity;
    }

    public String getDestinationCity() {
        return destinationCity;
    }

    public void setDestinationCity(String destinationCity) {
        this.destinationCity = destinationCity;
    }

    public double getDistanceKm() {
        return distanceKm;
    }

    public void setDistanceKm(double distanceKm) {
        this.distanceKm = distanceKm;
    }

    public int getEstimatedDurationMinutes() {
        return estimatedDurationMinutes;
    }

    public void setEstimatedDurationMinutes(int estimatedDurationMinutes) {
        this.estimatedDurationMinutes = estimatedDurationMinutes;
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

    public String getFormattedDuration() {
        int hours = estimatedDurationMinutes / 60;
        int mins = estimatedDurationMinutes % 60;
        return hours + "h " + (mins > 0 ? mins + "m" : "");
    }

    public String getRouteSummary() {
        return sourceCity + " -> " + destinationCity + " (" + distanceKm + " km, " + getFormattedDuration() + ")";
    }
}
