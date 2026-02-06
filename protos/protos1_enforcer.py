"""
PROTOS-1 Enforcer Core Module

This module implements the three core directives of the PROTOS-1 protocol:
1. Sanctuary - Access control and node validation
2. Synthesis - Data packet integrity and consensus verification
3. Logic - Multi-node response reconciliation

SECURITY CONSTRAINTS:
- No network calls beyond local file system access
- No OS-level secret access (no ~/.ssh, cloud credentials, etc.)
- No global state or background processes
- All operations are stateless and side-effect free on import
- Base directory is locked to project workspace
"""

import os
import json
import hashlib
from typing import Tuple, List, Dict, Any, Optional
from pathlib import Path


class Protos1Enforcer:
    """
    Core enforcement engine for PROTOS-1 protocol directives.
    
    This class provides three primary enforcement mechanisms:
    - Sanctuary: Validates that a source is authorized to access the system
    - Synthesis: Ensures data packets meet consensus requirements
    - Logic: Reconciles multiple responses using consensus voting
    """
    
    def __init__(
        self,
        base_dir: str,
        allowlist_path: str,
        consensus_threshold: float = 0.66
    ):
        """
        Initialize the PROTOS-1 Enforcer.
        
        Args:
            base_dir: Absolute path to project root (locked boundary)
            allowlist_path: Path to sanctuary allowlist file (relative to base_dir)
            consensus_threshold: Minimum agreement ratio for consensus (0.0-1.0)
        
        Raises:
            ValueError: If paths are invalid or threshold out of range
        """
        # Validate and lock base directory
        self.base_dir = Path(base_dir).resolve()
        if not self.base_dir.exists() or not self.base_dir.is_dir():
            raise ValueError(f"Invalid base directory: {base_dir}")
        
        # Validate consensus threshold
        if not 0.0 <= consensus_threshold <= 1.0:
            raise ValueError(f"Consensus threshold must be 0.0-1.0, got {consensus_threshold}")
        self.consensus_threshold = consensus_threshold
        
        # Resolve and validate allowlist path (must be within base_dir)
        self.allowlist_path = self._resolve_safe_path(allowlist_path)
        
        # Load allowlist on initialization
        self._allowlist = self._load_allowlist()
    
    def _resolve_safe_path(self, relative_path: str) -> Path:
        """
        Resolve a path relative to base_dir and ensure it stays within bounds.
        
        Args:
            relative_path: Path relative to base_dir
            
        Returns:
            Resolved absolute Path object
            
        Raises:
            ValueError: If resolved path escapes base_dir
        """
        target = (self.base_dir / relative_path).resolve()
        
        # Ensure the resolved path is within base_dir (prevent path traversal)
        if not str(target).startswith(str(self.base_dir)):
            raise ValueError(f"Path traversal detected: {relative_path} escapes {self.base_dir}")
        
        return target
    
    def _load_allowlist(self) -> set:
        """
        Load the sanctuary allowlist from disk.
        
        Returns:
            Set of allowed source identifiers
            
        Note:
            If file doesn't exist, returns empty set (fail-closed behavior)
        """
        if not self.allowlist_path.exists():
            return set()
        
        try:
            with open(self.allowlist_path, 'r', encoding='utf-8') as f:
                # Each line is a source identifier, strip whitespace and ignore comments
                lines = [
                    line.strip()
                    for line in f
                    if line.strip() and not line.strip().startswith('#')
                ]
                return set(lines)
        except Exception:
            # On any read error, fail closed with empty allowlist
            return set()
    
    def _hash_identifier(self, identifier: str) -> str:
        """
        Create a non-reversible hash of an identifier for logging.
        
        Args:
            identifier: Source identifier to hash
            
        Returns:
            SHA256 hash (first 16 chars) for safe logging
        """
        return hashlib.sha256(identifier.encode('utf-8')).hexdigest()[:16]
    
    def enforce_sanctuary(self, source_identifier: str) -> Tuple[bool, str]:
        """
        DIRECTIVE 1: SANCTUARY
        
        Validates that a source identifier is on the allowlist.
        This provides access control at the entry point.
        
        Args:
            source_identifier: Non-sensitive identifier (node name, logical ID, etc.)
            
        Returns:
            Tuple of (is_allowed, message)
            - is_allowed: True if source is in allowlist
            - message: Human-readable status message
        """
        if not source_identifier or not isinstance(source_identifier, str):
            return False, "Invalid source identifier"
        
        # Check allowlist
        is_allowed = source_identifier in self._allowlist
        
        if is_allowed:
            # Hash for logging to avoid exposing full identifier
            id_hash = self._hash_identifier(source_identifier)
            return True, f"Sanctuary granted (hash: {id_hash})"
        else:
            return False, "Sanctuary denied: source not in allowlist"
    
    def enforce_synthesis(self, packet: Dict[str, Any]) -> Tuple[bool, str]:
        """
        DIRECTIVE 2: SYNTHESIS
        
        Validates data packet integrity and structure before processing.
        Ensures packets meet minimum requirements for consensus.
        
        Args:
            packet: Dictionary containing data to be processed
            
        Returns:
            Tuple of (is_valid, message)
            - is_valid: True if packet passes validation
            - message: Human-readable status message
        """
        if not isinstance(packet, dict):
            return False, "Synthesis failed: packet must be a dictionary"
        
        # Check for required fields
        required_fields = ['source', 'action', 'data']
        missing_fields = [field for field in required_fields if field not in packet]
        
        if missing_fields:
            return False, f"Synthesis failed: missing fields {missing_fields}"
        
        # Validate source is non-empty
        if not packet.get('source'):
            return False, "Synthesis failed: source cannot be empty"
        
        # Validate action is non-empty string
        if not isinstance(packet.get('action'), str) or not packet['action']:
            return False, "Synthesis failed: action must be non-empty string"
        
        # Validate data exists (can be any type including None)
        if 'data' not in packet:
            return False, "Synthesis failed: data field required"
        
        # Optional: Check for consensus metadata if present
        if 'consensus' in packet:
            consensus = packet['consensus']
            if not isinstance(consensus, dict):
                return False, "Synthesis failed: consensus must be a dictionary"
            
            # Validate consensus structure
            if 'votes' in consensus and not isinstance(consensus['votes'], (int, float)):
                return False, "Synthesis failed: consensus votes must be numeric"
        
        return True, "Synthesis validated"
    
    def enforce_logic(self, responses: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        DIRECTIVE 3: LOGIC
        
        Reconciles multiple node/agent responses using consensus voting.
        Determines if sufficient agreement exists among responses.
        
        Args:
            responses: List of response dictionaries from multiple nodes
            
        Returns:
            Tuple of (consensus_reached, message)
            - consensus_reached: True if consensus threshold met
            - message: Human-readable status with vote details
        """
        if not isinstance(responses, list):
            return False, "Logic failed: responses must be a list"
        
        if len(responses) == 0:
            return False, "Logic failed: no responses to evaluate"
        
        if len(responses) == 1:
            # Single response always has consensus
            return True, "Logic: single response (consensus by default)"
        
        # Extract response values for comparison
        # We'll use the 'result' field or the entire response if no result field
        response_values = []
        for resp in responses:
            if not isinstance(resp, dict):
                return False, "Logic failed: all responses must be dictionaries"
            
            # Use 'result' field if present, otherwise serialize entire response
            if 'result' in resp:
                value = resp['result']
            else:
                value = json.dumps(resp, sort_keys=True)
            
            response_values.append(value)
        
        # Count occurrences of each unique response
        from collections import Counter
        vote_counts = Counter(response_values)
        
        # Find the most common response
        most_common_value, most_common_count = vote_counts.most_common(1)[0]
        
        # Calculate consensus ratio
        total_responses = len(responses)
        consensus_ratio = most_common_count / total_responses
        
        # Check if threshold met
        consensus_reached = consensus_ratio >= self.consensus_threshold
        
        if consensus_reached:
            message = (
                f"Logic: consensus reached ({most_common_count}/{total_responses} = "
                f"{consensus_ratio:.2%}, threshold: {self.consensus_threshold:.2%})"
            )
            return True, message
        else:
            message = (
                f"Logic: consensus NOT reached ({most_common_count}/{total_responses} = "
                f"{consensus_ratio:.2%}, threshold: {self.consensus_threshold:.2%})"
            )
            return False, message
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current enforcer configuration status.
        
        Returns:
            Dictionary with configuration details (no sensitive data)
        """
        return {
            'base_dir': str(self.base_dir),
            'allowlist_path': str(self.allowlist_path),
            'allowlist_size': len(self._allowlist),
            'consensus_threshold': self.consensus_threshold,
            'allowlist_exists': self.allowlist_path.exists()
        }
