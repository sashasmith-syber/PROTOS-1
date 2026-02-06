"""
PROTOS-1 Self-Test Module

Standalone self-test for the Protos1Enforcer core functionality.
This module can be run directly to verify the enforcer works correctly.

SAFETY:
- Uses only temporary test data
- No external I/O beyond console output
- No network calls
- Safe to run multiple times
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from protos.protos1_enforcer import Protos1Enforcer


def run_self_test():
    """
    Execute comprehensive self-tests for all three PROTOS-1 directives.
    """
    print("=" * 60)
    print("PROTOS-1 ENFORCER SELF-TEST")
    print("=" * 60)
    print()
    
    # Setup test environment
    test_base_dir = Path(__file__).parent.parent
    test_allowlist_path = "config/sanctuary.conf"
    
    print(f"Test base directory: {test_base_dir}")
    print(f"Test allowlist path: {test_allowlist_path}")
    print()
    
    try:
        # Initialize enforcer
        print("[1/4] Initializing enforcer...")
        enforcer = Protos1Enforcer(
            base_dir=str(test_base_dir),
            allowlist_path=test_allowlist_path,
            consensus_threshold=0.66
        )
        print("✓ Enforcer initialized successfully")
        print()
        
        # Display status
        status = enforcer.get_status()
        print("Enforcer Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
        print()
        
        # Test Sanctuary directive
        print("[2/4] Testing SANCTUARY directive...")
        
        # Test with non-existent source (should fail)
        allowed, msg = enforcer.enforce_sanctuary("test-node-999")
        print(f"  Test 1 (unknown source): {'✓ PASS' if not allowed else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        # Test with empty source (should fail)
        allowed, msg = enforcer.enforce_sanctuary("")
        print(f"  Test 2 (empty source): {'✓ PASS' if not allowed else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        print()
        
        # Test Synthesis directive
        print("[3/4] Testing SYNTHESIS directive...")
        
        # Test with valid packet
        valid_packet = {
            'source': 'test-node-1',
            'action': 'process_data',
            'data': {'key': 'value'}
        }
        valid, msg = enforcer.enforce_synthesis(valid_packet)
        print(f"  Test 1 (valid packet): {'✓ PASS' if valid else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        # Test with missing fields
        invalid_packet = {
            'source': 'test-node-1',
            'action': 'process_data'
            # Missing 'data' field
        }
        valid, msg = enforcer.enforce_synthesis(invalid_packet)
        print(f"  Test 2 (missing field): {'✓ PASS' if not valid else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        # Test with invalid type
        valid, msg = enforcer.enforce_synthesis("not a dict")
        print(f"  Test 3 (invalid type): {'✓ PASS' if not valid else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        print()
        
        # Test Logic directive
        print("[4/4] Testing LOGIC directive...")
        
        # Test with consensus (3/4 agree)
        responses_with_consensus = [
            {'result': 'approve'},
            {'result': 'approve'},
            {'result': 'approve'},
            {'result': 'deny'}
        ]
        consensus, msg = enforcer.enforce_logic(responses_with_consensus)
        print(f"  Test 1 (consensus reached): {'✓ PASS' if consensus else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        # Test without consensus (2/4 split)
        responses_without_consensus = [
            {'result': 'approve'},
            {'result': 'approve'},
            {'result': 'deny'},
            {'result': 'deny'}
        ]
        consensus, msg = enforcer.enforce_logic(responses_without_consensus)
        print(f"  Test 2 (no consensus): {'✓ PASS' if not consensus else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        # Test with single response
        single_response = [{'result': 'approve'}]
        consensus, msg = enforcer.enforce_logic(single_response)
        print(f"  Test 3 (single response): {'✓ PASS' if consensus else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        # Test with empty list
        consensus, msg = enforcer.enforce_logic([])
        print(f"  Test 4 (empty list): {'✓ PASS' if not consensus else '✗ FAIL'}")
        print(f"    Result: {msg}")
        
        print()
        print("=" * 60)
        print("SELF-TEST COMPLETE")
        print("=" * 60)
        print()
        print("Note: Some tests may show warnings about missing allowlist file.")
        print("This is expected if config/sanctuary.conf doesn't exist yet.")
        
        return True
        
    except Exception as e:
        print(f"✗ SELF-TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_self_test()
    sys.exit(0 if success else 1)
