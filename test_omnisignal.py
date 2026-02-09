"""
Tests for OmniSignal Intelligent Transport System.
"""

import unittest
import time
from mesh_network import MeshNetwork, MeshNode
from hazard_detector import HazardDetector
from warning_system import WarningSystem
from pole import OmniSignalPole
from config import Config


class TestMeshNetwork(unittest.TestCase):
    """Test cases for mesh network functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.network = MeshNetwork()
    
    def test_node_registration(self):
        """Test node registration in mesh network."""
        node = self.network.register_node("TEST_001", 0)
        
        self.assertIsNotNone(node)
        self.assertEqual(node.node_id, "TEST_001")
        self.assertEqual(node.position, 0)
        self.assertIn("TEST_001", self.network.nodes)
    
    def test_neighbor_discovery(self):
        """Test automatic neighbor discovery."""
        node1 = self.network.register_node("TEST_001", 0)
        node2 = self.network.register_node("TEST_002", 1)
        
        # Adjacent nodes should be neighbors
        self.assertIn("TEST_002", node1.neighbors)
        self.assertIn("TEST_001", node2.neighbors)
    
    def test_warning_propagation(self):
        """Test warning propagation to upstream nodes."""
        node1 = self.network.register_node("TEST_001", 0)
        node2 = self.network.register_node("TEST_002", 1)
        
        warning = {
            'type': 'DEBRIS',
            'priority': 2,
            'hops': 0
        }
        
        self.network.propagate_warning("TEST_001", warning)
        
        # Upstream node should receive warning
        messages = self.network.get_node_messages("TEST_002")
        self.assertTrue(len(messages) > 0)
        self.assertEqual(messages[0]['type'], 'WARNING')
    
    def test_hazard_broadcast(self):
        """Test hazard broadcast to all neighbors."""
        node1 = self.network.register_node("TEST_001", 0)
        node2 = self.network.register_node("TEST_002", 1)
        
        hazard = {
            'type': 'ACCIDENT',
            'priority': 5
        }
        
        self.network.broadcast_hazard("TEST_001", hazard)
        
        messages = self.network.get_node_messages("TEST_002")
        self.assertTrue(len(messages) > 0)
        self.assertEqual(messages[0]['type'], 'HAZARD_DETECTED')


class TestHazardDetector(unittest.TestCase):
    """Test cases for hazard detection."""
    
    def test_detector_initialization(self):
        """Test hazard detector initialization."""
        detector = HazardDetector("POLE_001")
        
        self.assertEqual(detector.pole_id, "POLE_001")
        self.assertIsNone(detector.current_hazard)
    
    def test_scan_throttling(self):
        """Test that scanning is throttled based on interval."""
        detector = HazardDetector("POLE_001")
        
        # First scan
        result1 = detector.scan()
        
        # Immediate second scan should return same result (throttled)
        result2 = detector.scan()
        
        # Results should be consistent
        self.assertEqual(result1, result2)
    
    def test_clear_hazard(self):
        """Test clearing hazard detection."""
        detector = HazardDetector("POLE_001")
        
        # Simulate hazard
        detector.current_hazard = {'type': 'DEBRIS'}
        
        # Clear it
        detector.clear_hazard()
        
        self.assertIsNone(detector.current_hazard)


class TestWarningSystem(unittest.TestCase):
    """Test cases for warning system."""
    
    def test_warning_activation(self):
        """Test warning activation."""
        warning_sys = WarningSystem("POLE_001")
        
        warning = {
            'type': 'DEBRIS',
            'color': 'YELLOW',
            'priority': 2,
            'source': 'POLE_000',
            'detected_at': time.time()
        }
        
        result = warning_sys.activate_warning(warning)
        
        self.assertTrue(result)
        self.assertEqual(warning_sys.led_status, 'ON')
        self.assertEqual(warning_sys.current_color, 'YELLOW')
    
    def test_priority_handling(self):
        """Test that higher priority warnings override lower ones."""
        warning_sys = WarningSystem("POLE_001")
        
        low_priority = {
            'type': 'DEBRIS',
            'color': 'YELLOW',
            'priority': 2,
            'source': 'POLE_000',
            'detected_at': time.time()
        }
        
        high_priority = {
            'type': 'ACCIDENT',
            'color': 'RED',
            'priority': 5,
            'source': 'POLE_000',
            'detected_at': time.time()
        }
        
        warning_sys.activate_warning(low_priority)
        warning_sys.activate_warning(high_priority)
        
        # Should display high priority warning
        self.assertEqual(warning_sys.current_color, 'RED')
    
    def test_warning_expiration(self):
        """Test that warnings expire after duration."""
        warning_sys = WarningSystem("POLE_001")
        
        warning = {
            'type': 'DEBRIS',
            'color': 'YELLOW',
            'priority': 2,
            'source': 'POLE_000',
            'detected_at': time.time()
        }
        
        warning_sys.activate_warning(warning)
        
        # Manually expire the warning
        for warning_id in warning_sys.active_warnings:
            warning_sys.active_warnings[warning_id]['expires_at'] = time.time() - 1
        
        warning_sys.update()
        
        # Warning should be cleared
        self.assertEqual(warning_sys.led_status, 'OFF')
        self.assertIsNone(warning_sys.current_color)
    
    def test_led_status(self):
        """Test LED status reporting."""
        warning_sys = WarningSystem("POLE_001")
        
        status = warning_sys.get_led_status()
        
        self.assertIn('pole_id', status)
        self.assertIn('status', status)
        self.assertIn('color', status)
        self.assertIn('message', status)


class TestOmniSignalPole(unittest.TestCase):
    """Test cases for OmniSignal pole."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.network = MeshNetwork()
    
    def test_pole_initialization(self):
        """Test pole initialization."""
        pole = OmniSignalPole("POLE_001", 0, self.network)
        
        self.assertEqual(pole.pole_id, "POLE_001")
        self.assertEqual(pole.position, 0)
        self.assertTrue(pole.active)
        self.assertIsNotNone(pole.hazard_detector)
        self.assertIsNotNone(pole.warning_system)
    
    def test_pole_status(self):
        """Test pole status reporting."""
        pole = OmniSignalPole("POLE_001", 0, self.network)
        
        status = pole.get_status()
        
        self.assertIn('pole_id', status)
        self.assertIn('position', status)
        self.assertIn('active', status)
        self.assertIn('led_status', status)
    
    def test_pole_deactivation(self):
        """Test pole deactivation."""
        pole = OmniSignalPole("POLE_001", 0, self.network)
        
        pole.deactivate()
        
        self.assertFalse(pole.active)
    
    def test_message_processing(self):
        """Test processing of mesh network messages."""
        pole1 = OmniSignalPole("POLE_001", 0, self.network)
        pole2 = OmniSignalPole("POLE_002", 1, self.network)
        
        # Simulate hazard broadcast
        hazard = {
            'type': 'ACCIDENT',
            'color': 'RED',
            'priority': 5,
            'detected_at': time.time()
        }
        
        self.network.broadcast_hazard("POLE_001", hazard)
        
        # Pole 2 should process the message
        pole2.update()
        
        # Pole 2 should have activated a warning
        self.assertEqual(pole2.warning_system.led_status, 'ON')


class TestConfiguration(unittest.TestCase):
    """Test cases for configuration."""
    
    def test_hazard_types_defined(self):
        """Test that hazard types are properly defined."""
        self.assertIn('DEBRIS', Config.HAZARD_TYPES)
        self.assertIn('ACCIDENT', Config.HAZARD_TYPES)
        self.assertIn('STOPPED_VEHICLE', Config.HAZARD_TYPES)
    
    def test_led_colors_defined(self):
        """Test that LED colors are properly defined."""
        self.assertIn('GREEN', Config.LED_COLORS)
        self.assertIn('YELLOW', Config.LED_COLORS)
        self.assertIn('RED', Config.LED_COLORS)
    
    def test_hazard_priority_structure(self):
        """Test hazard type structure includes priority and color."""
        for hazard_type, info in Config.HAZARD_TYPES.items():
            self.assertIn('color', info)
            self.assertIn('priority', info)


if __name__ == '__main__':
    unittest.main()
