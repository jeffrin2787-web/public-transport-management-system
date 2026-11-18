package com.vcet.transport.service;

import com.vcet.transport.model.Route;
import com.vcet.transport.repository.RouteRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class RouteService {

    private final RouteRepository routeRepository;

    public RouteService(RouteRepository routeRepository) {
        this.routeRepository = routeRepository;
    }

    public List<Route> getAllRoutes() {
        return routeRepository.findAll();
    }

    public Optional<Route> getRouteById(Long id) {
        return routeRepository.findById(id);
    }

    public List<String> getSourceCities() {
        return routeRepository.findDistinctSourceCities();
    }

    public List<String> getDestinationCities() {
        return routeRepository.findDistinctDestinationCities();
    }

    public Route createRoute(String sourceCity, String destinationCity, double distanceKm, int estimatedMinutes) {
        Optional<Route> existing = routeRepository.findBySourceCityIgnoreCaseAndDestinationCityIgnoreCase(sourceCity, destinationCity);
        if (existing.isPresent()) {
            throw new IllegalArgumentException("Route between " + sourceCity + " and " + destinationCity + " already exists.");
        }
        Route route = new Route(sourceCity, destinationCity, distanceKm, estimatedMinutes);
        return routeRepository.save(route);
    }
}
