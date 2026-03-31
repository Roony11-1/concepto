package com.tag.ok.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.tag.ok.domain.Edge;
import com.tag.ok.service.EdgeService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/edge/v1")
@RequiredArgsConstructor
public class EdgeController 
{
    private final EdgeService _edgeService;

    @PostMapping
    public ResponseEntity<List<Edge>> saveAll(@RequestBody List<Edge> edges)
    {
        return ResponseEntity.ok(_edgeService.saveAll(edges));
    }

    @GetMapping
    public ResponseEntity<List<Edge>> findAll()
    {
        return ResponseEntity.ok(_edgeService.findAll());
    }

    @GetMapping("/distance")
    public ResponseEntity<Double> getDistance(@RequestParam List<Long> ids) 
    {
        return ResponseEntity.ok(_edgeService.getTotalRouteDistance(ids));
    }

    @GetMapping("/route")
    public ResponseEntity<List<Edge>> getRoute(@RequestParam Long sourceNodeId, @RequestParam Long targetNodeId)
    {
        return ResponseEntity.ok(_edgeService.findRoute(sourceNodeId, targetNodeId));
    }
}
