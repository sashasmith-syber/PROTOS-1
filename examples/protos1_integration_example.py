"""
PROTOS-1 Integration Example

This module demonstrates how to integrate PROTOS-1 enforcement into an application.
It shows a minimal request handler that uses all three directives.

SECURITY:
- This is example code only - adapt to your specific use case
- Never log sensitive data from packets
- Always fail closed on enforcement failures
"""

from typing import Dict, Any, Optional
from protos import enforce_sanctuary, enforce_synthesis, enforce_logic


def handle_request(
    source: str,
    action: str,
    data: Any,
    enable_multi_node: bool = False
) -> Dict[str, Any]:
    """
    Example request handler with PROTOS-1 enforcement.
    
    This demonstrates the typical integration pattern:
    1. Sanctuary check on source
    2. Synthesis check on packet
    3. Logic check on responses (if multi-node)
    
    Args:
        source: Source identifier (non-sensitive)
        action: Action to perform
        data: Request payload
        enable_multi_node: Whether to simulate multi-node consensus
    
    Returns:
        Response dictionary with status and result/error
    """
    
    # STEP 1: SANCTUARY - Validate source is authorized
    allowed, sanctuary_msg = enforce_sanctuary(source)
    if not allowed:
        return {
            'status': 'denied',
            'error': sanctuary_msg,
            'directive': 'sanctuary'
        }
    
    # STEP 2: SYNTHESIS - Validate packet structure
    packet = {
        'source': source,
        'action': action,
        'data': data
    }
    
    valid, synthesis_msg = enforce_synthesis(packet)
    if not valid:
        return {
            'status': 'invalid',
            'error': synthesis_msg,
            'directive': 'synthesis'
        }
    
    # STEP 3: Process the request (your application logic here)
    try:
        result = process_action(action, data)
    except Exception as e:
        return {
            'status': 'error',
            'error': f"Processing failed: {str(e)}"
        }
    
    # STEP 4: LOGIC - If multi-node, check consensus
    if enable_multi_node:
        # Simulate multiple node responses (in real system, these come from actual nodes)
        responses = simulate_multi_node_responses(action, data, result)
        
        consensus, logic_msg = enforce_logic(responses)
        if not consensus:
            return {
                'status': 'no_consensus',
                'error': logic_msg,
                'directive': 'logic'
            }
    
    # All checks passed
    return {
        'status': 'success',
        'result': result,
        'directives_passed': ['sanctuary', 'synthesis', 'logic'] if enable_multi_node else ['sanctuary', 'synthesis']
    }


def process_action(action: str, data: Any) -> Any:
    """
    Placeholder for actual application logic.
    Replace this with your real processing code.
    
    Args:
        action: Action to perform
        data: Input data
    
    Returns:
        Processing result
    """
    # Example: simple action dispatcher
    if action == 'echo':
        return data
    elif action == 'uppercase':
        if isinstance(data, str):
            return data.upper()
        return data
    elif action == 'count':
        if isinstance(data, (list, str, dict)):
            return len(data)
        return 0
    else:
        raise ValueError(f"Unknown action: {action}")


def simulate_multi_node_responses(action: str, data: Any, local_result: Any) -> list:
    """
    Simulate responses from multiple nodes for consensus testing.
    
    In a real system, you would:
    1. Send the request to multiple nodes
    2. Collect their responses
    3. Pass them to enforce_logic()
    
    Args:
        action: Action performed
        data: Input data
        local_result: Result from local processing
    
    Returns:
        List of response dictionaries
    """
    # Simulate 3 nodes agreeing with local result
    return [
        {'result': local_result, 'node': 'node-alpha'},
        {'result': local_result, 'node': 'node-beta'},
        {'result': local_result, 'node': 'node-gamma'}
    ]


def main():
    """
    Example usage of the PROTOS-1 integrated request handler.
    """
    print("PROTOS-1 Integration Example")
    print("=" * 60)
    print()
    
    # Example 1: Valid request from authorized source
    print("Example 1: Valid request")
    response = handle_request(
        source='test-agent',
        action='echo',
        data={'message': 'Hello PROTOS-1'}
    )
    print(f"Response: {response}")
    print()
    
    # Example 2: Request from unauthorized source
    print("Example 2: Unauthorized source")
    response = handle_request(
        source='unknown-node',
        action='echo',
        data={'message': 'Hello'}
    )
    print(f"Response: {response}")
    print()
    
    # Example 3: Invalid packet (missing data)
    print("Example 3: Invalid packet structure")
    # This would fail in enforce_synthesis
    # We'll simulate by passing empty action
    response = handle_request(
        source='test-agent',
        action='',  # Invalid: empty action
        data=None
    )
    print(f"Response: {response}")
    print()
    
    # Example 4: Multi-node with consensus
    print("Example 4: Multi-node consensus")
    response = handle_request(
        source='test-agent',
        action='count',
        data=[1, 2, 3, 4, 5],
        enable_multi_node=True
    )
    print(f"Response: {response}")
    print()


if __name__ == "__main__":
    main()
