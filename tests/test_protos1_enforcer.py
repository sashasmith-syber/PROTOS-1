"""
PROTOS-1 Enforcer Unit Tests

Comprehensive test suite for all three PROTOS-1 directives.
Tests both success and failure cases, including edge cases.

SAFETY:
- Uses only test data
- No external dependencies
- No network calls
- Safe to run in any environment
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from protos.protos1_enforcer import Protos1Enforcer


class TestProtos1Enforcer(unittest.TestCase):
    """Test suite for Protos1Enforcer core functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.allowlist_path = os.path.join(self.test_dir, 'test_allowlist.conf')
        
        # Create test allowlist
        with open(self.allowlist_path, 'w') as f:
            f.write("# Test allowlist\n")
            f.write("node-alpha\n")
            f.write("node-beta\n")
            f.write("test-agent\n")
    
    def tearDown(self):
        """Clean up test fixtures after each test."""
        # Remove test files
        if os.path.exists(self.allowlist_path):
            os.remove(self.allowlist_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_enforcer_initialization(self):
        """Test enforcer initializes correctly with valid config."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf',
            consensus_threshold=0.66
        )
        
        self.assertIsNotNone(enforcer)
        status = enforcer.get_status()
        self.assertEqual(status['allowlist_size'], 3)
        self.assertEqual(status['consensus_threshold'], 0.66)
    
    def test_enforcer_invalid_base_dir(self):
        """Test enforcer rejects invalid base directory."""
        with self.assertRaises(ValueError):
            Protos1Enforcer(
                base_dir='/nonexistent/path/12345',
                allowlist_path='test_allowlist.conf'
            )
    
    def test_enforcer_invalid_threshold(self):
        """Test enforcer rejects invalid consensus threshold."""
        with self.assertRaises(ValueError):
            Protos1Enforcer(
                base_dir=self.test_dir,
                allowlist_path='test_allowlist.conf',
                consensus_threshold=1.5  # Invalid: > 1.0
            )
    
    def test_path_traversal_protection(self):
        """Test enforcer prevents path traversal attacks."""
        with self.assertRaises(ValueError):
            Protos1Enforcer(
                base_dir=self.test_dir,
                allowlist_path='../../../etc/passwd',  # Path traversal attempt
                consensus_threshold=0.66
            )
    
    def test_sanctuary_allowed_source(self):
        """Test sanctuary allows sources in allowlist."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        allowed, msg = enforcer.enforce_sanctuary('node-alpha')
        self.assertTrue(allowed)
        self.assertIn('granted', msg.lower())
    
    def test_sanctuary_denied_source(self):
        """Test sanctuary denies sources not in allowlist."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        allowed, msg = enforcer.enforce_sanctuary('unknown-node')
        self.assertFalse(allowed)
        self.assertIn('denied', msg.lower())
    
    def test_sanctuary_empty_source(self):
        """Test sanctuary rejects empty source identifier."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        allowed, msg = enforcer.enforce_sanctuary('')
        self.assertFalse(allowed)
        self.assertIn('invalid', msg.lower())
    
    def test_sanctuary_missing_allowlist(self):
        """Test sanctuary fails closed when allowlist missing."""
        # Don't create allowlist file
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='nonexistent.conf'
        )
        
        # Should deny all sources when allowlist missing
        allowed, msg = enforcer.enforce_sanctuary('node-alpha')
        self.assertFalse(allowed)
    
    def test_synthesis_valid_packet(self):
        """Test synthesis accepts valid packet structure."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        packet = {
            'source': 'node-alpha',
            'action': 'process_data',
            'data': {'key': 'value'}
        }
        
        valid, msg = enforcer.enforce_synthesis(packet)
        self.assertTrue(valid)
        self.assertIn('validated', msg.lower())
    
    def test_synthesis_missing_fields(self):
        """Test synthesis rejects packets with missing required fields."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        # Missing 'data' field
        packet = {
            'source': 'node-alpha',
            'action': 'process_data'
        }
        
        valid, msg = enforcer.enforce_synthesis(packet)
        self.assertFalse(valid)
        self.assertIn('missing', msg.lower())
    
    def test_synthesis_empty_source(self):
        """Test synthesis rejects packet with empty source."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        packet = {
            'source': '',
            'action': 'process_data',
            'data': {}
        }
        
        valid, msg = enforcer.enforce_synthesis(packet)
        self.assertFalse(valid)
        self.assertIn('source', msg.lower())
    
    def test_synthesis_invalid_action(self):
        """Test synthesis rejects packet with invalid action."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        packet = {
            'source': 'node-alpha',
            'action': '',  # Empty action
            'data': {}
        }
        
        valid, msg = enforcer.enforce_synthesis(packet)
        self.assertFalse(valid)
        self.assertIn('action', msg.lower())
    
    def test_synthesis_not_dict(self):
        """Test synthesis rejects non-dictionary packets."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        valid, msg = enforcer.enforce_synthesis("not a dict")
        self.assertFalse(valid)
        self.assertIn('dictionary', msg.lower())
    
    def test_logic_consensus_reached(self):
        """Test logic detects consensus when threshold met."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf',
            consensus_threshold=0.66
        )
        
        # 3 out of 4 agree (75% > 66%)
        responses = [
            {'result': 'approve'},
            {'result': 'approve'},
            {'result': 'approve'},
            {'result': 'deny'}
        ]
        
        consensus, msg = enforcer.enforce_logic(responses)
        self.assertTrue(consensus)
        self.assertIn('consensus reached', msg.lower())
    
    def test_logic_no_consensus(self):
        """Test logic detects lack of consensus when threshold not met."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf',
            consensus_threshold=0.66
        )
        
        # 2 out of 4 agree (50% < 66%)
        responses = [
            {'result': 'approve'},
            {'result': 'approve'},
            {'result': 'deny'},
            {'result': 'deny'}
        ]
        
        consensus, msg = enforcer.enforce_logic(responses)
        self.assertFalse(consensus)
        self.assertIn('not reached', msg.lower())
    
    def test_logic_single_response(self):
        """Test logic handles single response (automatic consensus)."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        responses = [{'result': 'approve'}]
        
        consensus, msg = enforcer.enforce_logic(responses)
        self.assertTrue(consensus)
        self.assertIn('single response', msg.lower())
    
    def test_logic_empty_responses(self):
        """Test logic rejects empty response list."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        consensus, msg = enforcer.enforce_logic([])
        self.assertFalse(consensus)
        self.assertIn('no responses', msg.lower())
    
    def test_logic_invalid_response_type(self):
        """Test logic rejects non-dictionary responses."""
        enforcer = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf'
        )
        
        responses = [
            {'result': 'approve'},
            'not a dict',  # Invalid
            {'result': 'approve'}
        ]
        
        consensus, msg = enforcer.enforce_logic(responses)
        self.assertFalse(consensus)
        self.assertIn('dictionaries', msg.lower())
    
    def test_logic_different_thresholds(self):
        """Test logic with different consensus thresholds."""
        # Test with 50% threshold
        enforcer_50 = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf',
            consensus_threshold=0.50
        )
        
        responses = [
            {'result': 'approve'},
            {'result': 'deny'}
        ]
        
        # 50% should reach consensus
        consensus, _ = enforcer_50.enforce_logic(responses)
        self.assertTrue(consensus)
        
        # Test with 100% threshold
        enforcer_100 = Protos1Enforcer(
            base_dir=self.test_dir,
            allowlist_path='test_allowlist.conf',
            consensus_threshold=1.0
        )
        
        # 50% should NOT reach consensus with 100% threshold
        consensus, _ = enforcer_100.enforce_logic(responses)
        self.assertFalse(consensus)


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestProtos1Enforcer)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
