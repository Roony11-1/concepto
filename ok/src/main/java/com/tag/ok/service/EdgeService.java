package com.tag.ok.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.tag.ok.domain.Edge;
import com.tag.ok.repository.EdgeRepository;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class EdgeService 
{
    private final EdgeRepository _edgeRepository;

    @Transactional
    public List<Edge> saveAll(List<Edge> edges)
    {
        return _edgeRepository.saveAll(edges);
    }

    public List<Edge> findAll()
    {
        return _edgeRepository.findAll();
    }

    public Double getTotalRouteDistance(List<Long> routeIds) 
    {
        Double distance = _edgeRepository.calculateTotalDistanceMetres(routeIds);
        
        // Si la ruta no existe o los IDs están mal, evitamos el NullPointerException
        return (distance != null) ? distance : 0.0;
    }

    public List<Edge> findRoute(Long sourceNodeId, Long targetNodeId)
    {
        return _edgeRepository.findShortestPath(sourceNodeId, targetNodeId);
    }
}
