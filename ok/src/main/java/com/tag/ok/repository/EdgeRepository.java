package com.tag.ok.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
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

    @Query(value = """
    WITH inicio AS (
        SELECT id 
        FROM edge_vertices_pgr 
        ORDER BY the_geom <-> ST_SetSRID(ST_Point(:lonInicio, :latInicio), 4326) 
        LIMIT 1
    ),
    fin AS (
        SELECT id 
        FROM edge_vertices_pgr 
        ORDER BY the_geom <-> ST_SetSRID(ST_Point(:lonFin, :latFin), 4326) 
        LIMIT 1
    )
    SELECT 
        r.seq AS seq,
        e.name AS calle,
        e.highway AS tipo,
        r.cost AS costoTramo,
        ST_AsText(e.geometry) AS geomWkt
    FROM pgr_dijkstra(
        'SELECT id, source, target, cost, reverse_cost FROM edge',
        (SELECT id FROM inicio), 
        (SELECT id FROM fin), 
        directed := true
    ) r
    JOIN edge e ON r.edge = e.id
    ORDER BY r.seq
    """, nativeQuery = true)
    List<RutaProjection> findShortestPathByCoords(
        @Param("lonInicio") double lonInicio,
        @Param("latInicio") double latInicio,
        @Param("lonFin") double lonFin,
        @Param("latFin") double latFin
    );
}
