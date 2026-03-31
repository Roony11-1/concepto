package com.tag.ok.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import com.tag.ok.domain.Edge;

@Repository
public interface EdgeRepository extends JpaRepository<Edge, Long> 
{
    // Suma las distancias de una lista de IDs de bordes (Edges)
    // Usamos ::geography para obtener metros exactos en lugar de grados
    @Query(value = "SELECT SUM(ST_Length(geometry::geography)) FROM edge WHERE id IN :edgeIds", 
           nativeQuery = true)
    Double calculateTotalDistanceMetres(List<Long> edgeIds);

    @Query(value = "SELECT e.* FROM pgr_dijkstra(" +
        "  'SELECT id, source_id as source, target_id as target, cost FROM edge', " +
        "  :startNodeId, :endNodeId, false" +
        ") AS di " +
        "JOIN edge e ON di.edge = e.id " +
        "ORDER BY di.seq", nativeQuery = true)
    List<Edge> findShortestPath(Long startNodeId, Long endNodeId);
}
