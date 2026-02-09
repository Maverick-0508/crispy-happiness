"""
Pole module representing an individual OmniSignal pole/node.
Integrates sensor, mesh network, and warning system.
"""

import time
from typing import Dict, Optional
from hazard_detector import HazardDetector
from warning_system import WarningSystem
from config import Config


class OmniSignalPole:
    """
    Represents a single OmniSignal pole on the highway.
    Integrates Edge AI sensor, mesh network communication, and LED warning system.
    """
    
    def __init__(self, pole_id: str, position: int, mesh_network):
        """
        Initialize an OmniSignal pole.
        
        Args:
            pole_id: Unique identifier for this pole
            position: Position on highway (higher numbers = further upstream)
            mesh_network: Reference to the shared mesh network
        """
        self.pole_id = pole_id
        self.position = position
        self.mesh_network = mesh_network
        
        # Initialize components
        self.hazard_detector = HazardDetector(pole_id)
        self.warning_system = WarningSystem(pole_id)
        
        # Register with mesh network
        self.mesh_node = mesh_network.register_node(pole_id, position)
        
        # State tracking
        self.last_hazard_broadcast = 0
        self.active = True
    
    def update(self):
        """
        Main update loop for the pole.
        Scans for hazards, processes messages, and manages warnings.
        """
        if not self.active:
            return
        
        # Scan for local hazards
        hazard = self.hazard_detector.scan()
        if hazard:
            self._handle_local_hazard(hazard)
        
        # Process incoming mesh network messages
        messages = self.mesh_network.get_node_messages(self.pole_id)
        for message in messages:
            self._process_message(message)
        
        # Update warning system (clear expired warnings)
        self.warning_system.update()
        
        # Propagate warnings upstream if needed
        if self.warning_system.should_propagate():
            self._propagate_warnings()
    
    def _handle_local_hazard(self, hazard: Dict):
        """
        Handle a locally detected hazard.
        
        Args:
            hazard: Hazard information from sensor
        """
        # Activate local warning
        warning = {
            'type': hazard['type'],
            'color': hazard['color'],
            'priority': hazard['priority'],
            'source': self.pole_id,
            'detected_at': hazard['detected_at'],
            'hops': 0
        }
        
        self.warning_system.activate_warning(warning)
        
        # Broadcast to neighbors (throttled to avoid spam)
        current_time = time.time()
        if current_time - self.last_hazard_broadcast > 1.0:
            self.mesh_network.broadcast_hazard(self.pole_id, hazard)
            self.last_hazard_broadcast = current_time
    
    def _process_message(self, message: Dict):
        """
        Process an incoming mesh network message.
        
        Args:
            message: Message from mesh network
        """
        msg_type = message.get('type')
        
        if msg_type == 'HAZARD_DETECTED':
            # Another pole detected a hazard
            hazard = message.get('hazard', {})
            warning = {
                'type': hazard.get('type'),
                'color': hazard.get('color'),
                'priority': hazard.get('priority'),
                'source': message.get('source'),
                'detected_at': hazard.get('detected_at'),
                'hops': 1
            }
            self.warning_system.activate_warning(warning)
        
        elif msg_type == 'WARNING':
            # Cascading warning from downstream
            warning_data = message.get('warning', {})
            hops = message.get('hops', 0)
            
            # Only propagate if within propagation distance
            if hops < Config.WARNING_PROPAGATION_DISTANCE:
                warning = {
                    **warning_data,
                    'hops': hops
                }
                self.warning_system.activate_warning(warning)
    
    def _propagate_warnings(self):
        """Propagate active warnings upstream through mesh network."""
        propagation_info = self.warning_system.get_propagation_info()
        
        if propagation_info and propagation_info.get('hops', 0) < Config.WARNING_PROPAGATION_DISTANCE:
            # Note: In production, use async/non-blocking delay or event scheduling
            # This sleep creates a visual cascading effect in the demo
            time.sleep(Config.WARNING_CASCADE_DELAY)
            self.mesh_network.propagate_warning(self.pole_id, propagation_info)
    
    def get_status(self) -> Dict:
        """
        Get current status of the pole.
        
        Returns:
            Dictionary with pole status information
        """
        led_status = self.warning_system.get_led_status()
        
        return {
            'pole_id': self.pole_id,
            'position': self.position,
            'active': self.active,
            'led_status': led_status,
            'neighbors': len(self.mesh_node.neighbors),
            'current_hazard': self.hazard_detector.current_hazard is not None
        }
    
    def ping_neighbors(self):
        """Ping neighboring poles to check connectivity."""
        return self.mesh_network.ping_neighbors(self.pole_id)
    
    def deactivate(self):
        """Deactivate this pole."""
        self.active = False
        self.warning_system.clear_warnings()
    
    def activate(self):
        """Activate this pole."""
        self.active = True
