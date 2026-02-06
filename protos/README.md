# PROTOS-1 Protocol Implementation

This directory contains the complete PROTOS-1 enforcement system.

## Directory Structure

- `protos1_enforcer.py` - Core enforcement engine implementing the three directives
- `protos1_gateway.py` - Application integration interface (use this in your code)
- `protos1_selftest.py` - Standalone self-test module
- `__init__.py` - Package initialization and public API exports

## Quick Start

```python
from protos import enforce_sanctuary, enforce_synthesis, enforce_logic

# Check if source is authorized
allowed, msg = enforce_sanctuary('test-agent')

# Validate packet structure
packet = {'source': 'test-agent', 'action': 'test', 'data': {}}
valid, msg = enforce_synthesis(packet)

# Check consensus among responses
responses = [{'result': 'ok'}, {'result': 'ok'}, {'result': 'ok'}]
consensus, msg = enforce_logic(responses)
```

## Documentation

See `docs/protos1-integration.md` for complete documentation.

## Testing

Run self-test:
```bash
python protos/protos1_selftest.py
```

Run unit tests:
```bash
python tests/test_protos1_enforcer.py
```

## Security

- No network calls
- No OS-level secret access
- Fail-closed behavior
- Path traversal protection
- No sensitive data logging
