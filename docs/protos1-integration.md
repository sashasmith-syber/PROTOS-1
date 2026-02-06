# PROTOS-1 Integration Documentation

**Author**: Sasha Smith (sashasmith-syber)

## Overview

PROTOS-1 is a security enforcement protocol that provides three core directives for validating and controlling system access and data flow. This document explains how PROTOS-1 can be integrated into AI agent systems and how to configure it safely.

PROTOS-1 is designed to work with external prompt collections and AI architectures without including any third-party prompt data. It provides a security layer that can be applied to various AI systems while maintaining separation from proprietary prompt content.

## The Three Directives

### Sanctuary (Access Control)

Sanctuary validates that a source identifier is authorized to access the system. It acts as the first line of defense by checking incoming requests against an allowlist of approved sources. When a request arrives, Sanctuary determines whether the source should be granted entry or denied access. This prevents unauthorized nodes, agents, or users from interacting with protected functionality.

### Synthesis (Data Integrity)

Synthesis ensures that data packets meet structural and integrity requirements before processing. It validates that incoming packets contain all required fields, that field types are correct, and that the data structure conforms to expected patterns. Synthesis prevents malformed or incomplete data from reaching core processing logic, reducing the risk of errors or exploitation through crafted inputs.

### Logic (Consensus Reconciliation)

Logic reconciles multiple responses from different nodes or agents using consensus voting. When you have distributed processing where multiple entities provide responses, Logic determines whether sufficient agreement exists among them. It calculates the consensus ratio and compares it against a configurable threshold to decide if the collective response should be accepted or rejected.

## Integration Points in the Codebase

### Core Module Location

The PROTOS-1 enforcer is implemented in `protos/protos1_enforcer.py`. This module contains the `Protos1Enforcer` class which implements all three directives. The enforcer is stateless on import and performs no side effects during module loading, making it safe to import anywhere in the codebase.

### Gateway Interface

Application code should not instantiate `Protos1Enforcer` directly. Instead, use the gateway functions provided in `protos/protos1_gateway.py`. These functions handle enforcer initialization, configuration loading, and provide a clean API for enforcement checks. The gateway maintains a singleton enforcer instance and automatically reads configuration from environment variables or uses safe defaults.

### Request Flow Integration

PROTOS-1 enforcement is typically wired into the request handling flow at the point where commands or actions are dispatched. The standard integration pattern follows this sequence: First, call `enforce_sanctuary()` with the source identifier to verify authorization. If sanctuary is denied, abort the request immediately with an error. Second, construct a packet dictionary containing source, action, and data fields, then call `enforce_synthesis()` to validate the packet structure. If synthesis fails, abort with a validation error. Third, process the request using your application logic. Finally, if you have multiple node responses, call `enforce_logic()` to verify consensus before accepting the result.

An example integration can be found in `examples/protos1_integration_example.py` which demonstrates a complete request handler with all three directives.

## Configuration

### Environment Variables

PROTOS-1 reads configuration from environment variables with safe defaults:

`PROTOS_BASE_DIR` specifies the project root directory. This is locked as the boundary for all file operations. If not set, it defaults to the parent directory of the protos module, which should be your project root.

`PROTOS_ALLOWLIST_PATH` specifies the path to the sanctuary allowlist file, relative to the base directory. The default is `config/sanctuary.conf`. This file contains one authorized source identifier per line.

`PROTOS_CONSENSUS_THRESHOLD` sets the minimum consensus ratio required for Logic enforcement. It must be a decimal between 0.0 and 1.0. The default is 0.66, meaning at least 66% of responses must agree for consensus to be reached.

### Sanctuary Allowlist

The allowlist file at `config/sanctuary.conf` defines which source identifiers are authorized. Each line in this file represents one allowed source. Lines starting with # are treated as comments. Empty lines are ignored. The file uses exact string matching with no wildcards or patterns.

Important security notes for the allowlist: Use non-sensitive identifiers such as node names or logical IDs. Do not use IP addresses if they could be spoofed in your environment. Never include secrets, credentials, or sensitive data in this file. The allowlist should be version controlled since it contains no secrets and defines your security policy.

### Adjusting Consensus Threshold

The consensus threshold determines how much agreement is required among multiple responses. A threshold of 0.66 means at least 66% of responses must match for consensus to be reached. A threshold of 0.50 requires simple majority. A threshold of 1.0 requires unanimous agreement. Lower thresholds are more permissive but may accept minority opinions. Higher thresholds are more strict but may reject valid responses due to minor disagreements.

To adjust the threshold, set the `PROTOS_CONSENSUS_THRESHOLD` environment variable before the enforcer is initialized. For example, `export PROTOS_CONSENSUS_THRESHOLD=0.75` would require 75% agreement.

## Usage Examples

### Basic Sanctuary Check

```python
from protos import enforce_sanctuary

allowed, message = enforce_sanctuary('test-agent')
if not allowed:
    return {'error': message, 'status': 'denied'}
```

### Synthesis Validation

```python
from protos import enforce_synthesis

packet = {
    'source': 'test-agent',
    'action': 'process_request',
    'data': request_payload
}

valid, message = enforce_synthesis(packet)
if not valid:
    return {'error': message, 'status': 'invalid'}
```

### Consensus Reconciliation

```python
from protos import enforce_logic

responses = [
    {'result': 'approve', 'node': 'alpha'},
    {'result': 'approve', 'node': 'beta'},
    {'result': 'deny', 'node': 'gamma'}
]

consensus, message = enforce_logic(responses)
if not consensus:
    return {'error': message, 'status': 'no_consensus'}
```

## Security Considerations

### Fail-Closed Behavior

All PROTOS-1 enforcement functions fail closed. If configuration is missing, malformed, or an error occurs during enforcement, the check fails and access is denied. This ensures that security failures do not accidentally grant unauthorized access.

### No Sensitive Data Logging

The enforcer never logs full packet contents or sensitive identifiers. When logging is necessary, source identifiers are hashed using SHA256 before being included in messages. Error messages contain only minimal context needed for debugging without exposing sensitive data.

### Path Traversal Protection

The enforcer validates all file paths to prevent path traversal attacks. Any path that resolves outside the configured base directory is rejected with an error. This ensures that configuration files and allowlists cannot be used to access arbitrary system files.

### No External Dependencies

PROTOS-1 enforcement operates entirely within the project workspace. It makes no network calls, accesses no OS-level secrets, and creates no global state or background processes. All operations are stateless and deterministic.

## Testing

### Unit Tests

Comprehensive unit tests are provided in `tests/test_protos1_enforcer.py`. These tests cover all three directives, edge cases, error conditions, and security protections. Run the tests with:

```bash
python tests/test_protos1_enforcer.py
```

### Self-Test

A standalone self-test module is available at `protos/protos1_selftest.py`. This performs end-to-end validation of the enforcer with dummy data. Run it with:

```bash
python protos/protos1_selftest.py
```

### Integration Example

The integration example at `examples/protos1_integration_example.py` demonstrates a complete request handler with all three directives. Run it to see PROTOS-1 in action:

```bash
python examples/protos1_integration_example.py
```

## Troubleshooting

### Sanctuary Always Denies

If sanctuary denies all sources, check that the allowlist file exists at the configured path and contains the source identifiers you're testing. Verify the file has no syntax errors and that identifiers match exactly (case-sensitive).

### Synthesis Validation Fails

If synthesis rejects valid-looking packets, ensure all required fields are present: source, action, and data. Check that source is non-empty, action is a non-empty string, and the data field exists even if its value is None or empty.

### Logic Never Reaches Consensus

If logic consistently fails to reach consensus, verify your threshold is appropriate for the number of nodes. With a 0.66 threshold and 3 nodes, at least 2 must agree. Check that response dictionaries contain a 'result' field or are otherwise comparable.

### Configuration Not Loading

If environment variables don't seem to take effect, ensure they're set before the first enforcement call. The gateway initializes the enforcer lazily on first use. To reload configuration, call `reset_enforcer()` from the gateway module.

## Maintenance

### Adding Authorized Sources

To authorize a new source, add its identifier to `config/sanctuary.conf` on a new line. Changes take effect on the next enforcer initialization. In production, you may need to restart the application or call `reset_enforcer()` to reload the allowlist.

### Rotating Configuration

If you need to change the consensus threshold or allowlist path, update the environment variables and restart the application. For testing configuration changes, use the self-test or integration example to verify behavior before deploying.

### Monitoring Enforcement

The gateway provides a `get_enforcer_status()` function that returns current configuration details without sensitive data. Use this for health checks or monitoring dashboards to verify the enforcer is properly configured.

## Advanced Topics

### Custom Packet Fields

While the enforcer requires source, action, and data fields, you can include additional fields in packets. The synthesis directive validates required fields but allows extra fields for application-specific metadata.

### Multi-Node Response Format

The logic directive expects a list of response dictionaries. Each dictionary should contain a 'result' field with the response value. If no 'result' field is present, the entire dictionary is serialized for comparison. Ensure response format is consistent across nodes for accurate consensus detection.

### Threshold Tuning

Choosing the right consensus threshold depends on your use case. For critical operations, use higher thresholds (0.75-1.0) to ensure strong agreement. For less critical operations or systems with many nodes, lower thresholds (0.51-0.66) may be appropriate. Monitor false rejections and adjust accordingly.
