"""
Core PROTOS-1 Enforcement Engine

Implements the three core security directives: Sanctuary, Synthesis, and Logic.
All checks are fail-closed (deny by default on any error).

This module provides deterministic, stateless enforcement with no external dependencies.
"""

import hashlib
import os
import json
from pathlib import Path
from typing import Tuple, Dict, List, Any


class Protos1Enforcer:
    """
    Core enforcement engine for PROTOS-1 security directives.
    
    Implements fail-closed security checks for:
    - Sanctuary: Access control via source authorization
    - Synthesis: Data packet integrity and structure validation
    - Logic: Consensus voting among multiple responses
    
    All methods return (success: bool, message: str) tuples.
    On any error, enforcement denies access (fail-closed).
    """
    
    def __init__(self, base_dir: str = None, allowlist_path: str = None, 
                 consensus_threshold: float = 0.66):
        """
        Initialize the PROTOS-1 enforcer.
        
        Args:
            base_dir (str): Base directory for configuration (default: PROTOS_BASE_DIR env)
            allowlist_path (str): Relative path to sanctuary allowlist 
                                (default: config/sanctuary.conf)
            consensus_threshold (float): Consensus ratio threshold 0.0-1.0 
                                       (default: 0.66 from PROTOS_CONSENSUS_THRESHOLD)
        
        Raises:
            ValueError: If configuration is invalid or missing.
        """
        self.base_dir = base_dir or os.getenv('PROTOS_BASE_DIR', os.getcwd())
        self.allowlist_path = allowlist_path or os.getenv(
            'PROTOS_ALLOWLIST_PATH', 'config/sanctuary.conf'
        )
        self.consensus_threshold = consensus_threshold or float(
            os.getenv('PROTOS_CONSENSUS_THRESHOLD', '0.66')
        )
        
        # Validate configuration
        if not isinstance(self.base_dir, str) or not self.base_dir:
            raise ValueError('base_dir must be a non-empty string')
        
        if not isinstance(self.allowlist_path, str) or not self.allowlist_path:
            raise ValueError('allowlist_path must be a non-empty string')
        
        if not (0.0 <= self.consensus_threshold <= 1.0):
            raise ValueError('consensus_threshold must be between 0.0 and 1.0')
        
        self._allowlist_cache = None
    
    def _get_allowlist(self) -> set:
        """
        Load and cache the sanctuary allowlist.
        
        Returns:
            set: Set of authorized source identifiers.
        
        Raises:
            IOError: If allowlist cannot be read.
        """
        if self._allowlist_cache is not None:
            return self._allowlist_cache
        
        try:
            full_path = os.path.join(self.base_dir, self.allowlist_path)
            full_path = os.path.abspath(full_path)
            
            # Prevent path traversal: ensure path is within base_dir
            base_abs = os.path.abspath(self.base_dir)
            if not full_path.startswith(base_abs):
                raise ValueError('Allowlist path escapes base directory')
            
            with open(full_path, 'r') as f:
                lines = f.readlines()
            
            allowlist = set()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    allowlist.add(line)
            
            self._allowlist_cache = allowlist
            return allowlist
        
        except Exception as e:
            raise IOError(f'Failed to load allowlist: {str(e)}')
    
    def _hash_source(self, source_id: str) -> str:
        """
        Hash a source identifier (for secure logging).
        
        Args:
            source_id (str): The source identifier to hash.
        
        Returns:
            str: SHA256 hash of the source identifier (first 8 chars).
        """
        h = hashlib.sha256(source_id.encode()).hexdigest()
        return h[:8]
    
    def enforce_sanctuary(self, source_id: str) -> Tuple[bool, str]:
        """
        Sanctuary Directive: Validate source authorization.
        
        Checks if the source identifier is in the authorized allowlist.
        Fails closed: denies access on any error or if source not found.
        
        Args:
            source_id (str): The source identifier to authorize.
        
        Returns:
            tuple: (allowed, message)
                - allowed (bool): True if source is authorized, False otherwise
                - message (str): Descriptive message (reason for denial on failure)
        """
        try:
            if not isinstance(source_id, str) or not source_id:
                return False, 'Source ID must be a non-empty string'
            
            allowlist = self._get_allowlist()
            
            if source_id in allowlist:
                hashed = self._hash_source(source_id)
                return True, f'Sanctuary check passed for source {hashed}'
            
            hashed = self._hash_source(source_id)
            return False, f'Source {hashed} not in allowlist'
        
        except Exception as e:
            return False, f'Sanctuary check failed: {str(e)}'
    
    def enforce_synthesis(self, packet: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Synthesis Directive: Validate packet structure and integrity.
        
        Checks:
        - packet is a dictionary
        - required fields present: 'source', 'action', 'data'
        - all required fields are non-empty strings (except 'data')
        - 'data' field is a dictionary or None
        - no extraneous fields beyond expected ones
        
        Fails closed: denies on any validation failure.
        
        Args:
            packet (dict): The data packet to validate.
        
        Returns:
            tuple: (valid, message)
                - valid (bool): True if packet is valid, False otherwise
                - message (str): Descriptive message
        """
        try:
            if not isinstance(packet, dict):
                return False, 'Packet must be a dictionary'
            
            # Check required fields
            required_fields = {'source', 'action', 'data'}
            if not required_fields.issubset(packet.keys()):
                missing = required_fields - packet.keys()
                return False, f'Missing required fields: {missing}'
            
            # Validate 'source' and 'action' are non-empty strings
            if not isinstance(packet['source'], str) or not packet['source']:
                return False, 'Field "source" must be a non-empty string'
            
            if not isinstance(packet['action'], str) or not packet['action']:
                return False, 'Field "action" must be a non-empty string'
            
            # Validate 'data' is dict or None
            if packet['data'] is not None and not isinstance(packet['data'], dict):
                return False, 'Field "data" must be a dictionary or None'
            
            # Check for unexpected fields
            expected_fields = {'source', 'action', 'data', 'timestamp', 'metadata'}
            unexpected = set(packet.keys()) - expected_fields
            if unexpected:
                return False, f'Unexpected fields: {unexpected}'
            
            return True, 'Synthesis check passed'
        
        except Exception as e:
            return False, f'Synthesis check failed: {str(e)}'
    
    def enforce_logic(self, responses: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Logic Directive: Consensus reconciliation across responses.
        
        Determines consensus by checking for 'result' field in responses:
        - Counts responses with 'result' == 'approve'
        - Calculates ratio of approvals / total responses
        - Passes if ratio >= consensus_threshold
        
        Fails closed: denies if responses empty, invalid, or consensus not reached.
        
        Args:
            responses (list): List of response dictionaries, each with 'result' field.
        
        Returns:
            tuple: (consensus_reached, message)
                - consensus_reached (bool): True if consensus threshold met, False otherwise
                - message (str): Descriptive message with consensus details
        """
        try:
            if not isinstance(responses, list):
                return False, 'Responses must be a list'
            
            if len(responses) == 0:
                return False, 'Responses list cannot be empty'
            
            # Validate each response
            approvals = 0
            for i, resp in enumerate(responses):
                if not isinstance(resp, dict):
                    return False, f'Response {i} is not a dictionary'
                
                if 'result' not in resp:
                    return False, f'Response {i} missing "result" field'
                
                if resp['result'] == 'approve':
                    approvals += 1
            
            consensus_ratio = approvals / len(responses)
            
            if consensus_ratio >= self.consensus_threshold:
                return True, f'Logic consensus passed: {approvals}/{len(responses)} approvals'
            
            return False, (f'Logic consensus failed: {approvals}/{len(responses)} approvals '
                          f'({consensus_ratio:.2%}) below threshold ({self.consensus_threshold:.2%})')
        
        except Exception as e:
            return False, f'Logic check failed: {str(e)}'
    
    def reset_cache(self):
        """
        Reset the allowlist cache (useful for testing after config changes).
        """
        self._allowlist_cache = None