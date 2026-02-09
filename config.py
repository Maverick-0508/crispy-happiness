"""
Configuration module for OmniSignal Intelligent Transport System.
Contains system-wide settings and constants.
"""

class Config:
    """Configuration for OmniSignal system."""
    
    # Network settings
    MESH_NETWORK_RANGE = 1000  # meters
    MESH_PING_INTERVAL = 0.5  # seconds
    MESH_TIMEOUT = 2.0  # seconds
    
    # Sensor settings
    SENSOR_SCAN_INTERVAL = 0.1  # seconds
    SENSOR_DETECTION_THRESHOLD = 0.75  # confidence threshold
    
    # Warning system settings
    WARNING_PROPAGATION_DISTANCE = 5  # number of poles upstream
    WARNING_LED_DURATION = 10  # seconds
    WARNING_CASCADE_DELAY = 0.2  # seconds between pole activations
    
    # Hazard types (inspired by F1 marshalling)
    HAZARD_TYPES = {
        'DEBRIS': {'color': 'YELLOW', 'priority': 2},
        'ACCIDENT': {'color': 'RED', 'priority': 5},
        'STOPPED_VEHICLE': {'color': 'YELLOW', 'priority': 3},
        'ADVERSE_WEATHER': {'color': 'YELLOW', 'priority': 2},
        'ANIMAL_CROSSING': {'color': 'YELLOW', 'priority': 3},
        'SLOW_TRAFFIC': {'color': 'GREEN', 'priority': 1},
    }
    
    # LED Colors (F1 flag system inspired)
    LED_COLORS = {
        'GREEN': 'All clear / Slow traffic ahead',
        'YELLOW': 'Hazard ahead - reduce speed',
        'RED': 'Danger - stop if safe',
        'BLUE': 'Faster vehicle approaching',
    }
