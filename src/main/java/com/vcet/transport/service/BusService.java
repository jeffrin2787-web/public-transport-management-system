package com.vcet.transport.service;

import com.vcet.transport.model.Bus;
import com.vcet.transport.model.BusType;
import com.vcet.transport.repository.BusRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class BusService {

    private final BusRepository busRepository;

    public BusService(BusRepository busRepository) {
        this.busRepository = busRepository;
    }

    public List<Bus> getAllBuses() {
        return busRepository.findAll();
    }

    public Optional<Bus> getBusById(Long id) {
        return busRepository.findById(id);
    }

    public Bus registerBus(String busNumber, BusType busType, int capacity, String operatorName) {
        if (busRepository.existsByBusNumber(busNumber)) {
            throw new IllegalArgumentException("Bus with registration number " + busNumber + " already exists.");
        }
        Bus bus = new Bus(busNumber, busType, capacity, operatorName);
        return busRepository.save(bus);
    }
}
