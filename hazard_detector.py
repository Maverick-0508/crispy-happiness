"""
Hazard detection module using Edge AI simulation.
Detects and classifies road hazards in real-time.
"""

import random
import time
from typing import Dict, Optional
from config import Config


class HazardDetector:
    """Edge AI sensor for real-time hazard detection."""
    
    def __init__(self, pole_id: str):
        """
        Initialize hazard detector.
        
        Args:
            pole_id: Unique identifier for the pole this detector is attached to
        """
        self.pole_id = pole_id
        self.last_scan_time = 0
        self.current_hazard: Optional[Dict] = None
    
    def scan(self) -> Optional[Dict]:
        """
        Scan for hazards using Edge AI.
        
        Returns:
            Dictionary with hazard info if detected, None otherwise
        """
        current_time = time.time()
        
        # Throttle scanning based on interval
        if current_time - self.last_scan_time < Config.SENSOR_SCAN_INTERVAL:
            return self.current_hazard
        
        self.last_scan_time = current_time
        
        # Simulate AI detection (in real system, this would be actual AI model)
        detection_result = self._simulate_ai_detection()
        
        if detection_result:
            self.current_hazard = detection_result
            return detection_result
        else:
            self.current_hazard = None
            return None
    
    def _simulate_ai_detection(self) -> Optional[Dict]:
        """
        Simulate Edge AI hazard detection.
        In production, this would use actual computer vision/AI models.
        
        Returns:
            Hazard information if detected
        """
        # Simulate random detection (5% chance per scan)
        if random.random() < 0.05:
            hazard_type = random.choice(list(Config.HAZARD_TYPES.keys()))
            confidence = random.uniform(0.75, 0.99)
            
            hazard_info = Config.HAZARD_TYPES[hazard_type]
            
            return {
                'type': hazard_type,
                'confidence': confidence,
                'color': hazard_info['color'],
                'priority': hazard_info['priority'],
                'detected_at': time.time(),
                'pole_id': self.pole_id,
                'location': self._get_location()
            }
        
        return None
    
    def _get_location(self) -> Dict[str, float]:
        """
        Get current location (simulated).
        In production, this would use GPS.
        
        Returns:
            Dictionary with latitude and longitude
        """
        # Simulate location for this pole
        base_lat = 40.7128
        base_lon = -74.0060
        
        # Create unique location based on pole_id
        pole_num = hash(self.pole_id) % 1000
        
        return {
            'latitude': base_lat + (pole_num * 0.001),
            'longitude': base_lon + (pole_num * 0.001)
        }
    
    def clear_hazard(self):
        """Clear the current hazard detection."""
        self.current_hazard = None
