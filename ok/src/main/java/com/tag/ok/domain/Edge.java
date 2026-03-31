package com.tag.ok.domain;

import org.locationtech.jts.geom.LineString;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
public class Edge 
{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "source_id")
    private Node source;

    @ManyToOne
    @JoinColumn(name = "target_id")
    private Node target;

    private Double distance;
    private Double cost;
    private boolean oneway;

    private LineString geometry; 
}