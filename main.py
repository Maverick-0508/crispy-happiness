"""
OmniSignal - Intelligent Transport System
Main orchestration module for the extended perception system.
"""

import time
from typing import List, Dict
from mesh_network import MeshNetwork
from pole import OmniSignalPole
from config import Config


class OmniSignalSystem:
    """
    Main orchestrator for the OmniSignal Intelligent Transport System.
    Manages multiple poles, mesh network, and overall system coordination.
    """
    
    def __init__(self, num_poles: int = 10):
        """
        Initialize the OmniSignal system.
        
        Args:
            num_poles: Number of poles to deploy on the highway
        """
        self.mesh_network = MeshNetwork()
        self.poles: List[OmniSignalPole] = []
        self.running = False
        
        # Deploy poles along highway
        self._deploy_poles(num_poles)
    
    def _deploy_poles(self, num_poles: int):
        """
        Deploy OmniSignal poles along the highway.
        
        Args:
            num_poles: Number of poles to deploy
        """
        print(f"Deploying {num_poles} OmniSignal poles...")
        
        for i in range(num_poles):
            pole_id = f"POLE_{i:03d}"
            position = i  # Position increases upstream
            
            pole = OmniSignalPole(pole_id, position, self.mesh_network)
            self.poles.append(pole)
            
            print(f"  ✓ Deployed {pole_id} at position {position}")
        
        print(f"Mesh network established with {len(self.poles)} nodes")
    
    def start(self, duration: float = None):
        """
        Start the OmniSignal system.
        
        Args:
            duration: How long to run in seconds (None = run indefinitely)
        """
        print("\n" + "="*60)
        print("OmniSignal Intelligent Transport System - ONLINE")
        print("Extended Perception Active")
        print("="*60 + "\n")
        
        self.running = True
        start_time = time.time()
        
        try:
            while self.running:
                # Update all poles
                for pole in self.poles:
                    pole.update()
                
                # Check if duration has elapsed
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Small delay to prevent CPU spinning
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\nShutdown requested...")
        
        finally:
            self.stop()
    
    def stop(self):
        """Stop the OmniSignal system."""
        self.running = False
        print("\nOmniSignal system shutting down...")
        
        for pole in self.poles:
            pole.deactivate()
        
        print("All poles deactivated. System offline.\n")
    
    def get_system_status(self) -> Dict:
        """
        Get overall system status.
        
        Returns:
            Dictionary with system-wide status information
        """
        active_poles = sum(1 for pole in self.poles if pole.active)
        poles_with_warnings = sum(
            1 for pole in self.poles 
            if pole.warning_system.led_status == 'ON'
        )
        
        return {
            'total_poles': len(self.poles),
            'active_poles': active_poles,
            'poles_with_warnings': poles_with_warnings,
            'mesh_network_online': self.mesh_network.online,
            'running': self.running
        }
    
    def display_status(self):
        """Display current system status to console."""
        print("\n" + "-"*60)
        print("SYSTEM STATUS")
        print("-"*60)
        
        system_status = self.get_system_status()
        print(f"Total Poles: {system_status['total_poles']}")
        print(f"Active Poles: {system_status['active_poles']}")
        print(f"Poles with Active Warnings: {system_status['poles_with_warnings']}")
        print(f"Mesh Network: {'ONLINE' if system_status['mesh_network_online'] else 'OFFLINE'}")
        
        print("\nPOLE STATUS:")
        for pole in self.poles:
            status = pole.get_status()
            led = status['led_status']
            
            status_icon = "●" if led['status'] == 'ON' else "○"
            color_text = led['color'] or "---"
            
            print(f"  {status_icon} {status['pole_id']} (Pos {status['position']:02d}) | "
                  f"LED: {color_text:6s} | Neighbors: {status['neighbors']} | "
                  f"Hazard: {'YES' if status['current_hazard'] else 'NO'}")
        
        print("-"*60 + "\n")
    
    def set_mesh_online_status(self, online: bool):
        """
        Set whether online mesh network is available.
        
        Args:
            online: True for online mode, False for offline-only mode
        """
        self.mesh_network.set_online_status(online)
        status = "ONLINE" if online else "OFFLINE"
        print(f"Mesh network mode: {status}")


def main():
    """Main entry point for OmniSignal system."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                      OmniSignal                             ║
    ║          Intelligent Transport System (ITS)                 ║
    ║                                                             ║
    ║  Extended Perception for Highway Safety                     ║
    ║  Formula 1 Marshalling Logic for Public Roads              ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Create system with 10 poles
    system = OmniSignalSystem(num_poles=10)
    
    # Display initial status
    system.display_status()
    
    # Run for demonstration (10 seconds)
    print("Running simulation for 10 seconds...")
    print("(Hazards will be randomly detected and warnings cascaded)\n")
    
    system.start(duration=10)
    
    # Display final status
    system.display_status()
    
    print("OmniSignal demonstration complete.")


if __name__ == "__main__":
    main()
