package com.vcet.transport.controller;

import com.vcet.transport.service.ReportService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/reports")
@CrossOrigin(origins = "*")
public class ReportController {

    private final ReportService reportService;

    public ReportController(ReportService reportService) {
        this.reportService = reportService;
    }

    @GetMapping("/summary")
    public ResponseEntity<Map<String, Object>> getSummary() {
        return ResponseEntity.ok(reportService.getOverallSummary());
    }

    @GetMapping("/route-revenue")
    public ResponseEntity<List<Map<String, Object>>> getRouteRevenue() {
        return ResponseEntity.ok(reportService.getRouteWiseRevenue());
    }

    @GetMapping("/occupancy")
    public ResponseEntity<List<Map<String, Object>>> getOccupancy() {
        return ResponseEntity.ok(reportService.getScheduleOccupancy());
    }
}
