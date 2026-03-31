package com.tag.ok.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.tag.ok.domain.Node;

@Repository
public interface NodeRepository extends JpaRepository<Node, Long>
{

}
