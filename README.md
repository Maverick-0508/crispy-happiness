# OmniSignal - Intelligent Transport System

**Extended Perception for Highway Safety**

OmniSignal is an Intelligent Transport System (ITS) that grants drivers "extended perception" by bringing Formula 1 marshalling logic to public highways. The system targets blind spot and highway safety through extended perception, using an offline mesh network to aid vulnerable drivers through universal visual cues.

## 🎯 Overview

OmniSignal uses Edge AI sensors to detect hazards in real-time. Each pole pings its neighbors via an offline and, if possible, online mesh network, triggering a cascading LED warning upstream to alert approaching drivers of dangers ahead.

### Key Features

- **Edge AI Hazard Detection**: Real-time detection of road hazards using AI sensors
- **Mesh Network Communication**: Hybrid offline/online mesh network for reliable pole-to-pole communication
- **Cascading LED Warnings**: F1-inspired visual warning system that propagates upstream
- **Extended Perception**: Drivers receive advance warning of hazards beyond their line of sight
- **Resilient Design**: Works in offline mode when internet connectivity is unavailable

## 🏗️ System Architecture

The OmniSignal system consists of several integrated components:

### Components

1. **Hazard Detector** (`hazard_detector.py`)
   - Edge AI sensor for real-time hazard detection
   - Classifies hazards by type and priority
   - Simulates computer vision/AI detection capabilities

2. **Mesh Network** (`mesh_network.py`)
   - Hybrid offline/online communication system
   - Automatic neighbor discovery
   - Warning propagation and hazard broadcasting

3. **Warning System** (`warning_system.py`)
   - LED warning management and display
   - Priority-based warning activation
   - Time-based warning expiration

4. **OmniSignal Pole** (`pole.py`)
   - Individual pole/node integrating all components
   - Message processing and state management
   - Cascading warning propagation

5. **Main System** (`main.py`)
   - System orchestration and coordination
   - Pole deployment and management
   - Status monitoring and reporting

## 🚦 Hazard Types & LED Colors

Based on F1 marshalling flag system:

| Hazard Type | LED Color | Priority | Description |
|-------------|-----------|----------|-------------|
| Accident | RED | 5 | Danger - stop if safe |
| Stopped Vehicle | YELLOW | 3 | Hazard ahead - reduce speed |
| Animal Crossing | YELLOW | 3 | Hazard ahead - reduce speed |
| Debris | YELLOW | 2 | Hazard ahead - reduce speed |
| Adverse Weather | YELLOW | 2 | Hazard ahead - reduce speed |
| Slow Traffic | GREEN | 1 | All clear / Slow traffic ahead |

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses Python standard library)

### Installation

```bash
# Clone the repository
git clone https://github.com/Maverick-0508/crispy-happiness.git
cd crispy-happiness

# Run the system
python main.py
```

### Running Tests

```bash
# Run all tests
python -m unittest test_omnisignal.py -v

# Run specific test class
python -m unittest test_omnisignal.TestMeshNetwork -v
```

## 📊 Usage Example

```python
from main import OmniSignalSystem

# Create system with 10 poles
system = OmniSignalSystem(num_poles=10)

# Display initial status
system.display_status()

# Start the system (runs for 10 seconds)
system.start(duration=10)

# Display final status
system.display_status()
```

## 🔧 Configuration

System parameters can be adjusted in `config.py`:

```python
# Network settings
MESH_NETWORK_RANGE = 1000  # meters
MESH_PING_INTERVAL = 0.5   # seconds

# Sensor settings
SENSOR_SCAN_INTERVAL = 0.1  # seconds
SENSOR_DETECTION_THRESHOLD = 0.75  # confidence threshold

# Warning system settings
WARNING_PROPAGATION_DISTANCE = 5  # number of poles upstream
WARNING_LED_DURATION = 10  # seconds
WARNING_CASCADE_DELAY = 0.2  # seconds between pole activations
```

## 🎮 System Workflow

1. **Detection**: Edge AI sensors continuously scan for hazards
2. **Activation**: When a hazard is detected, the local pole activates its LED
3. **Broadcasting**: Hazard information is broadcast to neighboring poles
4. **Propagation**: Warnings cascade upstream to alert approaching drivers
5. **Display**: LED colors indicate hazard type and severity
6. **Expiration**: Warnings automatically expire after configured duration

## 🌐 Mesh Network

The mesh network supports both online and offline operation:

- **Online Mode**: Full connectivity with all neighbors
- **Offline Mode**: Degraded but functional mesh using only local communication
- **Automatic Neighbor Discovery**: Poles automatically find and connect to adjacent poles
- **Upstream Propagation**: Warnings propagate to poles with higher position numbers

## 📈 Benefits

- **Proactive Safety**: Drivers warned before hazards are visible
- **Reduced Accidents**: Early warning allows more reaction time
- **Vulnerable Road Users**: Helps drivers with limited perception
- **All-Weather Operation**: Works in fog, rain, and low visibility
- **Resilient**: Functions without internet connectivity

## 🛠️ Development

### Project Structure

```
crispy-happiness/
├── config.py              # System configuration
├── hazard_detector.py     # Edge AI sensor module
├── mesh_network.py        # Mesh network communication
├── warning_system.py      # LED warning management
├── pole.py                # Individual pole/node
├── main.py                # Main orchestration system
├── test_omnisignal.py     # Unit tests
└── README.md              # This file
```

### Running the Demo

```bash
python main.py
```

This will:
1. Deploy 10 OmniSignal poles along a simulated highway
2. Run the system for 10 seconds
3. Display status updates showing hazard detection and warning propagation
4. Show final system status

## 📝 License

This project is part of the crispy-happiness repository.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.
