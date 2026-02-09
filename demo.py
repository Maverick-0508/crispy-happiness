"""
Interactive demonstration of OmniSignal system with controlled hazards.
Shows cascading warning propagation in action.
"""

import time
from main import OmniSignalSystem
from config import Config


def demo_cascading_warnings():
    """Demonstrate cascading warning system with controlled hazards."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         OmniSignal - Cascading Warning Demo                 ║
    ║                                                             ║
    ║  This demo shows how warnings cascade upstream when         ║
    ║  a hazard is detected on the highway.                      ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Create system with 8 poles
    system = OmniSignalSystem(num_poles=8)
    
    print("\n[SCENARIO] Simulating accident at POLE_002")
    print("Expected: Warning should cascade upstream to poles 3-7\n")
    
    # Simulate an accident detection at pole 2
    pole_2 = system.poles[2]
    
    # Manually inject a hazard (simulating detection)
    hazard = {
        'type': 'ACCIDENT',
        'color': 'RED',
        'priority': 5,
        'detected_at': time.time(),
        'pole_id': 'POLE_002'
    }
    
    # Activate warning on pole 2
    warning = {
        'type': hazard['type'],
        'color': hazard['color'],
        'priority': hazard['priority'],
        'source': pole_2.pole_id,
        'detected_at': hazard['detected_at'],
        'hops': 0
    }
    
    pole_2.warning_system.activate_warning(warning)
    pole_2.mesh_network.broadcast_hazard(pole_2.pole_id, hazard)
    
    # Let the system propagate warnings
    print("Propagating warnings...")
    for i in range(20):  # Run update cycles
        for pole in system.poles:
            pole.update()
        time.sleep(0.1)
    
    # Display final status
    print("\nFinal Status After Propagation:")
    system.display_status()
    
    # Show which poles have warnings
    poles_with_warnings = [
        pole.pole_id for pole in system.poles 
        if pole.warning_system.led_status == 'ON'
    ]
    
    print(f"\nPoles with Active Warnings: {', '.join(poles_with_warnings)}")
    print(f"Total Poles Warned: {len(poles_with_warnings)}/8")
    
    system.stop()


def demo_multiple_hazards():
    """Demonstrate system handling multiple simultaneous hazards."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║      OmniSignal - Multiple Hazards Demo                    ║
    ║                                                             ║
    ║  Shows how the system handles multiple hazards with        ║
    ║  different priorities simultaneously.                      ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    system = OmniSignalSystem(num_poles=8)
    
    print("\n[SCENARIO 1] Debris detected at POLE_001 (Priority: 2, Yellow)")
    print("[SCENARIO 2] Accident detected at POLE_004 (Priority: 5, Red)")
    print("Expected: Higher priority warnings should take precedence\n")
    
    # Inject debris at pole 1
    debris_hazard = {
        'type': 'DEBRIS',
        'color': 'YELLOW',
        'priority': 2,
        'detected_at': time.time(),
        'pole_id': 'POLE_001'
    }
    
    pole_1 = system.poles[1]
    pole_1.warning_system.activate_warning({
        'type': debris_hazard['type'],
        'color': debris_hazard['color'],
        'priority': debris_hazard['priority'],
        'source': pole_1.pole_id,
        'detected_at': debris_hazard['detected_at'],
        'hops': 0
    })
    pole_1.mesh_network.broadcast_hazard(pole_1.pole_id, debris_hazard)
    
    # Inject accident at pole 4
    accident_hazard = {
        'type': 'ACCIDENT',
        'color': 'RED',
        'priority': 5,
        'detected_at': time.time(),
        'pole_id': 'POLE_004'
    }
    
    pole_4 = system.poles[4]
    pole_4.warning_system.activate_warning({
        'type': accident_hazard['type'],
        'color': accident_hazard['color'],
        'priority': accident_hazard['priority'],
        'source': pole_4.pole_id,
        'detected_at': accident_hazard['detected_at'],
        'hops': 0
    })
    pole_4.mesh_network.broadcast_hazard(pole_4.pole_id, accident_hazard)
    
    # Let warnings propagate
    print("Propagating warnings...")
    for i in range(20):
        for pole in system.poles:
            pole.update()
        time.sleep(0.1)
    
    # Display results
    system.display_status()
    
    # Analyze warning colors
    print("\nWarning Analysis:")
    for pole in system.poles:
        if pole.warning_system.led_status == 'ON':
            color = pole.warning_system.current_color
            num_warnings = len(pole.warning_system.active_warnings)
            print(f"  {pole.pole_id}: {color} LED ({num_warnings} warning(s))")
    
    system.stop()


def demo_offline_mode():
    """Demonstrate system operating in offline mesh mode."""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║       OmniSignal - Offline Mesh Mode Demo                  ║
    ║                                                             ║
    ║  Demonstrates resilient operation when online network      ║
    ║  is unavailable (offline mesh only).                       ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    system = OmniSignalSystem(num_poles=6)
    
    print("\n[MODE] Switching to OFFLINE mesh network mode")
    system.set_mesh_online_status(False)
    
    print("[SCENARIO] Animal crossing detected at POLE_001")
    print("Expected: Warnings should still propagate via offline mesh\n")
    
    # Inject hazard
    hazard = {
        'type': 'ANIMAL_CROSSING',
        'color': 'YELLOW',
        'priority': 3,
        'detected_at': time.time(),
        'pole_id': 'POLE_001'
    }
    
    pole_1 = system.poles[1]
    pole_1.warning_system.activate_warning({
        'type': hazard['type'],
        'color': hazard['color'],
        'priority': hazard['priority'],
        'source': pole_1.pole_id,
        'detected_at': hazard['detected_at'],
        'hops': 0
    })
    pole_1.mesh_network.broadcast_hazard(pole_1.pole_id, hazard)
    
    # Propagate
    print("Propagating via offline mesh...")
    for i in range(20):
        for pole in system.poles:
            pole.update()
        time.sleep(0.1)
    
    system.display_status()
    
    poles_warned = sum(1 for pole in system.poles if pole.warning_system.led_status == 'ON')
    print(f"\nOffline mesh successfully warned {poles_warned} poles")
    
    system.stop()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("OmniSignal Interactive Demonstrations")
    print("="*60)
    
    # Demo 1: Cascading warnings
    demo_cascading_warnings()
    
    print("\n" + "="*60 + "\n")
    time.sleep(2)
    
    # Demo 2: Multiple hazards
    demo_multiple_hazards()
    
    print("\n" + "="*60 + "\n")
    time.sleep(2)
    
    # Demo 3: Offline mode
    demo_offline_mode()
    
    print("\n" + "="*60)
    print("All demonstrations complete!")
    print("="*60 + "\n")
