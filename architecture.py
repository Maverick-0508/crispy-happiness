"""
Architecture overview and system components for OmniSignal.
This module provides documentation of the system architecture.
"""

ARCHITECTURE = """
OmniSignal System Architecture
================================

┌─────────────────────────────────────────────────────────────────┐
│                      OmniSignal System                          │
│                   (Main Orchestrator)                           │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Manages
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Mesh Network                                 │
│  - Hybrid Offline/Online Communication                          │
│  - Automatic Neighbor Discovery                                 │
│  - Warning Propagation (Upstream)                               │
│  - Hazard Broadcasting (All Neighbors)                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Connects
                     ▼
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐      ┌─────────────────┐       ┌──────────────
│  OmniSignal     │◄────►│  OmniSignal     │◄─────►│  OmniSignal
│  Pole (N-1)     │      │  Pole (N)       │       │  Pole (N+1)
└────────┬────────┘      └────────┬────────┘       └──────┬───────
         │                        │                        │
    ┌────┴────┐              ┌────┴────┐             ┌────┴────┐
    │         │              │         │             │         │
    ▼         ▼              ▼         ▼             ▼         ▼
┌────────┐ ┌────────┐   ┌────────┐ ┌────────┐  ┌────────┐ ┌────────┐
│ Hazard │ │Warning │   │ Hazard │ │Warning │  │ Hazard │ │Warning │
│Detector│ │ System │   │Detector│ │ System │  │Detector│ │ System │
└────────┘ └────────┘   └────────┘ └────────┘  └────────┘ └────────┘
    │         │              │         │             │         │
    │         │              │         │             │         │
    ▼         ▼              ▼         ▼             ▼         ▼
  Edge AI    LED          Edge AI    LED         Edge AI    LED
  Sensor   Display        Sensor   Display       Sensor   Display


Data Flow: Hazard Detection & Warning Propagation
===================================================

1. DETECTION PHASE
   ┌──────────────┐
   │ Edge AI      │──► Scan for hazards
   │ Sensor       │    (debris, accidents, etc.)
   └──────┬───────┘
          │
          │ Hazard Detected
          ▼
   ┌──────────────┐
   │ Local Pole   │──► Activate LED warning
   │ (Pole N)     │    Broadcast to neighbors
   └──────┬───────┘
          │
          │
          ▼

2. PROPAGATION PHASE
   
   Downstream          Current            Upstream
   (Position N-1)      (Position N)       (Position N+1...N+5)
   
   ┌──────┐            ┌──────┐           ┌──────┐  ┌──────┐  ┌──────┐
   │POLE  │◄───────────│POLE  │──────────►│POLE  │─►│POLE  │─►│POLE  │
   │ N-1  │  Receives  │  N   │ Cascades  │ N+1  │  │ N+2  │  │ N+3  │
   │      │  Hazard    │  ●   │ Warning   │  ●   │  │  ●   │  │  ●   │
   └──────┘            └──────┘           └──────┘  └──────┘  └──────┘
                       (Source)            ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
                                          Warnings cascade upstream
                                          to alert approaching drivers


Component Responsibilities
===========================

┌─────────────────────────────────────────────────────────────────┐
│ Config (config.py)                                              │
│ - System-wide configuration                                     │
│ - Hazard types and LED color mappings                           │
│ - Network, sensor, and warning timing parameters                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ HazardDetector (hazard_detector.py)                             │
│ - Edge AI simulation for real-time hazard detection             │
│ - Classification of hazard types                                │
│ - Confidence threshold validation                               │
│ - Location tracking (GPS simulation)                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ MeshNetwork (mesh_network.py)                                   │
│ - Node registration and neighbor discovery                      │
│ - Message queuing and routing                                   │
│ - Upstream warning propagation                                  │
│ - Hazard broadcasting to all neighbors                          │
│ - Online/Offline mode switching                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ WarningSystem (warning_system.py)                               │
│ - LED warning activation and display                            │
│ - Priority-based warning management                             │
│ - Warning expiration handling                                   │
│ - Status reporting                                              │
│ - Propagation decision logic                                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ OmniSignalPole (pole.py)                                        │
│ - Integration of all components                                 │
│ - Main update loop coordination                                 │
│ - Message processing from mesh network                          │
│ - Local hazard handling                                         │
│ - Warning propagation orchestration                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ OmniSignalSystem (main.py)                                      │
│ - System initialization and deployment                          │
│ - Pole lifecycle management                                     │
│ - System-wide status monitoring                                 │
│ - Mesh network coordination                                     │
└─────────────────────────────────────────────────────────────────┘


F1-Inspired Warning System
============================

Priority Level    Hazard Type          LED Color    Description
─────────────────────────────────────────────────────────────────
5 (Highest)       ACCIDENT             RED          Danger - stop if safe
3                 STOPPED_VEHICLE      YELLOW       Reduce speed
3                 ANIMAL_CROSSING      YELLOW       Reduce speed
2                 DEBRIS               YELLOW       Hazard ahead
2                 ADVERSE_WEATHER      YELLOW       Reduce speed
1 (Lowest)        SLOW_TRAFFIC         GREEN        All clear


Key Design Principles
======================

1. **Extended Perception**: Drivers warned before hazards are visible
2. **Resilient Design**: Functions offline when internet unavailable
3. **Priority-Based**: Critical hazards override minor ones
4. **Cascading Alerts**: Warnings propagate upstream automatically
5. **Real-Time**: Edge AI processing at each pole for low latency
6. **Scalable**: Mesh network grows with additional poles
"""

def print_architecture():
    """Print the system architecture diagram."""
    print(ARCHITECTURE)


if __name__ == "__main__":
    print_architecture()
