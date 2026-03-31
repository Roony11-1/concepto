package com.tag.ok.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.tag.ok.domain.Node;
import com.tag.ok.repository.NodeRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class NodeService 
{
    private final NodeRepository _nodeRepository;

    public List<Node> findAll()
    {
        return _nodeRepository.findAll();
    }

    public List<Node> saveAll(List<Node> nodes)
    {
        return _nodeRepository.saveAll(nodes);
    }
}
