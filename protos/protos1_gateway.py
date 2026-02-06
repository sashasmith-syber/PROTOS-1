"""
PROTOS-1 Gateway Module

Thin wrapper interface for integrating PROTOS-1 enforcement into applications.
Provides three simple functions that handle enforcer instantiation and configuration.

SECURITY:
- All configuration read from environment or safe defaults
- No secrets logged or printed
- Fail-closed behavior on configuration errors
- No external I/O beyond reading config files within project
"""

import os
from pathlib import Path
from typing import Tuple, Dict, Any, List, Optional

from protos.protos1_enforcer import Protos1Enforcer


# Module-level enforcer instance (lazy-initialized)
_enforcer_instance: Optional[Protos1Enforcer] = None


def _get_enforcer() -> Protos1Enforcer:
    """
    Get or create the singleton enforcer instance.
    
    Configuration is read from environment variables with safe defaults:
    - PROTOS_BASE_DIR: Project root (defaults to parent of this file)
    - PROTOS_ALLOWLIST_PATH: Relative path to allowlist (defaults to config/sanctuary.conf)
    - PROTOS_CONSENSUS_THRESHOLD: Consensus ratio 0.0-1.0 (defaults to 0.66)
    
    Returns:
        Configured Protos1Enforcer instance
        
    Raises:
        RuntimeError: If configuration is invalid
    """
    global _enforcer_instance
    
    if _enforcer_instance is not None:
        return _enforcer_instance
    
    # Read configuration from environment with safe defaults
    base_dir = os.environ.get('PROTOS_BASE_DIR')
    if not base_dir:
        # Default to project root (parent of protos/ directory)
        base_dir = str(Path(__file__).parent.parent)
    
    allowlist_path = os.environ.get('PROTOS_ALLOWLIST_PATH', 'config/sanctuary.conf')
    
    # Parse consensus threshold with validation
    threshold_str = os.environ.get('PROTOS_CONSENSUS_THRESHOLD', '0.66')
    try:
        consensus_threshold = float(threshold_str)
    except ValueError:
        raise RuntimeError(f"Invalid PROTOS_CONSENSUS_THRESHOLD: {threshold_str}")
    
    # Validate threshold range
    if not 0.0 <= consensus_threshold <= 1.0:
        raise RuntimeError(f"PROTOS_CONSENSUS_THRESHOLD must be 0.0-1.0, got {consensus_threshold}")
    
    # Initialize enforcer
    try:
        _enforcer_instance = Protos1Enforcer(
            base_dir=base_dir,
            allowlist_path=allowlist_path,
            consensus_threshold=consensus_threshold
        )
        return _enforcer_instance
    except Exception as e:
        raise RuntimeError(f"Failed to initialize PROTOS-1 enforcer: {e}")


def enforce_sanctuary(source_identifier: str) -> Tuple[bool, str]:
    """
    GATEWAY FUNCTION: Sanctuary Enforcement
    
    Validates that a source identifier is authorized to access the system.
    Use this at entry points where requests/commands arrive.
    
    Args:
        source_identifier: Non-sensitive identifier (node name, IP, logical ID)
                          MUST NOT contain secrets or sensitive data
    
    Returns:
        Tuple of (is_allowed, message)
        - is_allowed: True if source is authorized
        - message: Status message (safe for logging)
    
    Example:
        allowed, msg = enforce_sanctuary("node-alpha")
        if not allowed:
            return error_response(msg)
    """
    try:
        enforcer = _get_enforcer()
        return enforcer.enforce_sanctuary(source_identifier)
    except Exception as e:
        # Fail closed on any error
        return False, f"Sanctuary check failed: {str(e)}"


def enforce_synthesis(packet: Dict[str, Any]) -> Tuple[bool, str]:
    """
    GATEWAY FUNCTION: Synthesis Enforcement
    
    Validates data packet structure and integrity before processing.
    Use this before executing commands or processing data payloads.
    
    Args:
        packet: Dictionary containing:
                - source: Source identifier
                - action: Action to perform
                - data: Payload data (any type)
                - consensus (optional): Consensus metadata
    
    Returns:
        Tuple of (is_valid, message)
        - is_valid: True if packet passes validation
        - message: Status message (safe for logging)
    
    Example:
        packet = {
            'source': 'node-alpha',
            'action': 'process_request',
            'data': request_data
        }
        valid, msg = enforce_synthesis(packet)
        if not valid:
            return error_response(msg)
    """
    try:
        enforcer = _get_enforcer()
        return enforcer.enforce_synthesis(packet)
    except Exception as e:
        # Fail closed on any error
        return False, f"Synthesis check failed: {str(e)}"


def enforce_logic(responses: List[Dict[str, Any]]) -> Tuple[bool, str]:
    """
    GATEWAY FUNCTION: Logic Enforcement
    
    Reconciles multiple node/agent responses using consensus voting.
    Use this when you have multiple responses that need agreement validation.
    
    Args:
        responses: List of response dictionaries from different nodes/agents
                  Each should contain a 'result' field or be comparable
    
    Returns:
        Tuple of (consensus_reached, message)
        - consensus_reached: True if consensus threshold met
        - message: Status with vote details (safe for logging)
    
    Example:
        responses = [
            {'result': 'approve', 'node': 'alpha'},
            {'result': 'approve', 'node': 'beta'},
            {'result': 'deny', 'node': 'gamma'}
        ]
        consensus, msg = enforce_logic(responses)
        if not consensus:
            return error_response(msg)
    """
    try:
        enforcer = _get_enforcer()
        return enforcer.enforce_logic(responses)
    except Exception as e:
        # Fail closed on any error
        return False, f"Logic check failed: {str(e)}"


def get_enforcer_status() -> Dict[str, Any]:
    """
    Get current PROTOS-1 enforcer configuration status.
    
    Returns:
        Dictionary with configuration details (no sensitive data)
        
    Example:
        status = get_enforcer_status()
        print(f"Allowlist size: {status['allowlist_size']}")
    """
    try:
        enforcer = _get_enforcer()
        return enforcer.get_status()
    except Exception as e:
        return {
            'error': str(e),
            'status': 'not_initialized'
        }


def reset_enforcer():
    """
    Reset the enforcer instance (useful for testing or config reload).
    
    WARNING: This will cause the next enforcement call to re-read configuration.
    Use with caution in production environments.
    """
    global _enforcer_instance
    _enforcer_instance = None
