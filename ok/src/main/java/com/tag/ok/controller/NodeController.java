package com.tag.ok.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.tag.ok.domain.Node;
import com.tag.ok.service.NodeService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/node/v1")
@RequiredArgsConstructor
public class NodeController 
{
    private final NodeService _nodeService;

    @GetMapping
    public ResponseEntity<List<Node>> findAll()
    {
        return ResponseEntity.ok(_nodeService.findAll());
    }

    @PostMapping
    public ResponseEntity<List<Node>> saveAll(@RequestBody List<Node> nodes)
    {
        return ResponseEntity.ok(_nodeService.saveAll(nodes));
    }
}
