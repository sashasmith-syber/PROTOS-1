"""
PROTOS-1 Protocol Implementation

This package provides the PROTOS-1 enforcement system with three core directives:
- Sanctuary: Access control and source validation
- Synthesis: Data packet integrity verification
- Logic: Multi-node consensus reconciliation

For application integration, use the gateway functions:
    from protos.protos1_gateway import enforce_sanctuary, enforce_synthesis, enforce_logic
"""

# Version information
__version__ = "1.0.0"
__author__ = "PROTOS-1 Integration Team"

# Public API exports
from protos.protos1_gateway import (
    enforce_sanctuary,
    enforce_synthesis,
    enforce_logic,
    get_enforcer_status,
    reset_enforcer
)

__all__ = [
    'enforce_sanctuary',
    'enforce_synthesis',
    'enforce_logic',
    'get_enforcer_status',
    'reset_enforcer'
]
