"""
Warning system module for cascading LED alerts.
Implements upstream propagation of warnings to approaching drivers.
"""

import time
from typing import Dict, Optional
from config import Config


class WarningSystem:
    """Manages LED warning display and cascading propagation."""
    
    def __init__(self, pole_id: str):
        """
        Initialize warning system.
        
        Args:
            pole_id: Unique identifier for the pole
        """
        self.pole_id = pole_id
        self.active_warnings: Dict[str, Dict] = {}  # warning_id -> warning_info
        self.led_status = 'OFF'
        self.current_color = None
    
    def activate_warning(self, warning: Dict) -> bool:
        """
        Activate a warning on this pole's LED.
        
        Args:
            warning: Warning information including hazard type, color, priority
            
        Returns:
            True if warning was activated, False if a higher priority warning is active
        """
        # Generate unique warning ID using source, timestamp, and hash to avoid collisions
        warning_id = f"{warning.get('source', 'unknown')}_{warning.get('detected_at', time.time())}_{hash(str(warning))}"
        
        # Check if we should override current warning based on priority
        if self.current_color:
            current_priority = self._get_current_priority()
            new_priority = warning.get('priority', 0)
            
            if new_priority <= current_priority:
                # Don't override with lower priority warning
                return False
        
        # Activate the warning
        self.active_warnings[warning_id] = {
            **warning,
            'activated_at': time.time(),
            'expires_at': time.time() + Config.WARNING_LED_DURATION
        }
        
        self._update_led_display()
        return True
    
    def _update_led_display(self):
        """Update LED display based on active warnings."""
        if not self.active_warnings:
            self.led_status = 'OFF'
            self.current_color = None
            return
        
        # Find highest priority warning
        highest_priority_warning = max(
            self.active_warnings.values(),
            key=lambda w: w.get('priority', 0)
        )
        
        self.current_color = highest_priority_warning.get('color', 'YELLOW')
        self.led_status = 'ON'
    
    def _get_current_priority(self) -> int:
        """Get priority of currently displayed warning."""
        if not self.active_warnings:
            return 0
        
        return max(w.get('priority', 0) for w in self.active_warnings.values())
    
    def update(self):
        """Update warning system, clearing expired warnings."""
        current_time = time.time()
        
        # Remove expired warnings
        expired_warnings = [
            warning_id for warning_id, warning in self.active_warnings.items()
            if current_time > warning.get('expires_at', 0)
        ]
        
        for warning_id in expired_warnings:
            del self.active_warnings[warning_id]
        
        self._update_led_display()
    
    def get_led_status(self) -> Dict:
        """
        Get current LED status.
        
        Returns:
            Dictionary with LED status information
        """
        return {
            'pole_id': self.pole_id,
            'status': self.led_status,
            'color': self.current_color,
            'active_warnings': len(self.active_warnings),
            'message': Config.LED_COLORS.get(self.current_color, 'No active warnings')
        }
    
    def clear_warnings(self):
        """Clear all active warnings."""
        self.active_warnings.clear()
        self.led_status = 'OFF'
        self.current_color = None
    
    def expire_all_warnings(self):
        """
        Helper method to expire all warnings immediately.
        Primarily for testing purposes.
        """
        current_time = time.time()
        for warning_id in self.active_warnings:
            self.active_warnings[warning_id]['expires_at'] = current_time - 1
        self.update()
    
    def should_propagate(self) -> bool:
        """
        Check if warnings should be propagated upstream.
        
        Returns:
            True if there are active warnings that should cascade
        """
        return len(self.active_warnings) > 0
    
    def get_propagation_info(self) -> Optional[Dict]:
        """
        Get information for warning propagation.
        
        Returns:
            Warning info to propagate, or None if no propagation needed
        """
        if not self.active_warnings:
            return None
        
        # Get highest priority warning for propagation
        highest_priority_warning = max(
            self.active_warnings.values(),
            key=lambda w: w.get('priority', 0)
        )
        
        return {
            'type': highest_priority_warning.get('type'),
            'color': highest_priority_warning.get('color'),
            'priority': highest_priority_warning.get('priority'),
            'source': highest_priority_warning.get('source'),
            'detected_at': highest_priority_warning.get('detected_at'),
            'hops': highest_priority_warning.get('hops', 0)
        }
