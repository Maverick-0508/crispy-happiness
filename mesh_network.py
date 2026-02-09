"""
Mesh network module for offline/online hybrid communication.
Enables poles to communicate hazard information to neighbors.
"""

import time
from typing import Dict, List, Set, Optional
from config import Config


class MeshNode:
    """Represents a node in the mesh network."""
    
    def __init__(self, node_id: str, position: int):
        """
        Initialize mesh node.
        
        Args:
            node_id: Unique identifier for this node
            position: Position on highway (for determining upstream/downstream)
        """
        self.node_id = node_id
        self.position = position
        self.neighbors: Set[str] = set()
        self.messages: List[Dict] = []
        self.last_ping = time.time()
    
    def add_neighbor(self, neighbor_id: str):
        """Add a neighbor to this node's network."""
        self.neighbors.add(neighbor_id)
    
    def remove_neighbor(self, neighbor_id: str):
        """Remove a neighbor from this node's network."""
        self.neighbors.discard(neighbor_id)
    
    def send_message(self, message: Dict):
        """Queue a message to be sent to neighbors."""
        self.messages.append(message)
    
    def get_messages(self) -> List[Dict]:
        """Retrieve and clear queued messages."""
        messages = self.messages.copy()
        self.messages.clear()
        return messages


class MeshNetwork:
    """
    Hybrid offline/online mesh network for pole-to-pole communication.
    Implements cascading warning propagation upstream.
    """
    
    def __init__(self):
        """Initialize the mesh network."""
        self.nodes: Dict[str, MeshNode] = {}
        self.online = True  # Track if online network is available
    
    def register_node(self, node_id: str, position: int) -> MeshNode:
        """
        Register a new node in the mesh network.
        
        Args:
            node_id: Unique identifier for the node
            position: Position on highway (higher = further upstream)
            
        Returns:
            The registered MeshNode
        """
        node = MeshNode(node_id, position)
        self.nodes[node_id] = node
        self._discover_neighbors(node_id)
        return node
    
    def _discover_neighbors(self, node_id: str):
        """
        Discover and connect to neighboring nodes.
        Uses position-based neighbor discovery.
        
        Args:
            node_id: ID of node to discover neighbors for
        """
        if node_id not in self.nodes:
            return
        
        current_node = self.nodes[node_id]
        
        # Find nearby nodes based on position
        for other_id, other_node in self.nodes.items():
            if other_id == node_id:
                continue
            
            # Consider nodes within range as neighbors
            distance = abs(current_node.position - other_node.position)
            if distance <= 1:  # Adjacent poles
                current_node.add_neighbor(other_id)
                other_node.add_neighbor(node_id)
    
    def propagate_warning(self, source_node_id: str, warning: Dict):
        """
        Propagate warning upstream through the mesh network.
        
        Args:
            source_node_id: ID of node where hazard was detected
            warning: Warning information to propagate
        """
        if source_node_id not in self.nodes:
            return
        
        source_node = self.nodes[source_node_id]
        
        # Propagate to upstream neighbors (higher position numbers)
        upstream_neighbors = [
            neighbor_id for neighbor_id in source_node.neighbors
            if self.nodes[neighbor_id].position > source_node.position
        ]
        
        for neighbor_id in upstream_neighbors:
            message = {
                'type': 'WARNING',
                'source': source_node_id,
                'warning': warning,
                'timestamp': time.time(),
                'hops': warning.get('hops', 0) + 1
            }
            
            self.nodes[neighbor_id].send_message(message)
    
    def broadcast_hazard(self, source_node_id: str, hazard: Dict):
        """
        Broadcast hazard detection to all neighbors.
        
        Args:
            source_node_id: ID of node that detected hazard
            hazard: Hazard information
        """
        if source_node_id not in self.nodes:
            return
        
        message = {
            'type': 'HAZARD_DETECTED',
            'source': source_node_id,
            'hazard': hazard,
            'timestamp': time.time()
        }
        
        source_node = self.nodes[source_node_id]
        for neighbor_id in source_node.neighbors:
            self.nodes[neighbor_id].send_message(message)
    
    def ping_neighbors(self, node_id: str) -> List[str]:
        """
        Ping neighbors to check connectivity.
        
        Args:
            node_id: ID of node to ping from
            
        Returns:
            List of responsive neighbor IDs
        """
        if node_id not in self.nodes:
            return []
        
        node = self.nodes[node_id]
        node.last_ping = time.time()
        
        # In a real system, this would send actual ping messages
        # For simulation, we return all neighbors if online, subset if offline
        if self.online:
            return list(node.neighbors)
        else:
            # Simulate degraded offline mesh: approximately 2/3 of neighbors respond
            # (offline mesh is less reliable but still functional)
            return [n for n in node.neighbors if hash(n) % 3 != 0]
    
    def set_online_status(self, online: bool):
        """Set whether online network is available."""
        self.online = online
    
    def get_node_messages(self, node_id: str) -> List[Dict]:
        """
        Get messages for a specific node.
        
        Args:
            node_id: ID of node to get messages for
            
        Returns:
            List of messages
        """
        if node_id not in self.nodes:
            return []
        
        return self.nodes[node_id].get_messages()
