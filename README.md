# PROTOS-1 Security Framework

A security enforcement protocol for validating and controlling access to AI systems and agents.

## Overview

PROTOS-1 provides three core security directives for protecting AI agent systems and managing distributed consensus. It is designed to work with external prompt collections and AI architectures without including any third-party prompt data.

## Three Core Directives

- **Sanctuary**: Access control and source authorization
- **Synthesis**: Data packet integrity and validation  
- **Logic**: Multi-node consensus reconciliation

## Features

- **Fail-closed security**: All enforcement checks deny access on errors
- **Path traversal protection**: Validates all file paths to prevent escape
- **No sensitive logging**: Source identifiers are hashed before logging
- **Stateless operation**: No global state or background processes
- **Zero external dependencies**: Uses only Python standard library
- **Local operation only**: No network calls beyond local file system

## Installation

```bash
# Clone the repository
git clone https://github.com/sashasmith-syber/protos-1.git
cd protos-1

# No external dependencies required - uses Python stdlib only
python3 -m pytest tests/  # Run tests
```

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

## Usage

### Configuration

Set environment variables to configure PROTOS-1:

```bash
export PROTOS_BASE_DIR=/path/to/project
export PROTOS_ALLOWLIST_PATH=config/sanctuary.conf
export PROTOS_CONSENSUS_THRESHOLD=0.66
```

### Sanctuary (Access Control)

Validate that a source identifier is authorized:

```python
from protos import enforce_sanctuary

allowed, message = enforce_sanctuary('node-alpha')
if not allowed:
    return {'error': message, 'status': 'denied'}
```

### Synthesis (Packet Validation)

Validate data packet structure before processing:

```python
from protos import enforce_synthesis

packet = {
    'source': 'node-alpha',
    'action': 'process_request',
    'data': request_payload
}

valid, message = enforce_synthesis(packet)
if not valid:
    return {'error': message, 'status': 'invalid'}
```

### Logic (Consensus Reconciliation)

Reconcile multiple responses using consensus voting:

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

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python tests/test_protos1_enforcer.py

# Run self-test
python protos/protos1_selftest.py

# Run integration example
python examples/protos1_integration_example.py
```

## Documentation

- **Integration Guide**: `docs/protos1-integration.md` - Complete integration documentation
- **Integration Summary**: `PROTOS1_INTEGRATION_SUMMARY.md` - Implementation review and security analysis
- **Examples**: `examples/` - Working code examples
- **Tests**: `tests/` - Comprehensive test suite

## Project Structure

```
protos-1/
├── protos/                  # Core PROTOS-1 implementation
│   ├── __init__.py
│   ├── protos1_enforcer.py  # Core enforcement engine
│   ├── protos1_gateway.py   # Application integration interface
│   └── protos1_selftest.py  # Self-test module
├── config/                  # Configuration files
│   ├── sanctuary.conf       # Sanctuary allowlist
│   └── README.md
├── tests/                   # Test suite
│   ├── test_protos1_enforcer.py
│   └── README.md
├── examples/                # Usage examples
│   ├── protos1_integration_example.py
│   └── README.md
├── docs/                    # Documentation
│   └── protos1-integration.md
├── LICENSE                  # MIT License
└── README.md               # This file
```

## Security

PROTOS-1 is a security enforcement layer, not a complete defense system. Users must:

- Keep sensitive data and credentials out of the repository
- Protect the sanctuary allowlist with appropriate file permissions
- Review all AI-generated code before execution
- Use PROTOS-1 as part of a defense-in-depth strategy

See `docs/protos1-integration.md` for detailed security considerations.

## Authors

**Primary Author**: Sasha Smith ([@sashasmith-syber](https://github.com/sashasmith-syber))

## Citation

If you use PROTOS-1 in academic work, please cite:

```
Smith, S. (2026). PROTOS-1: A Security Framework for AI Agent Systems.
GitHub repository: https://github.com/sashasmith-syber/protos-1
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Sasha Smith (sashasmith-syber)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Compatibility

PROTOS-1 is designed to work with external prompt collections and AI agent systems. It does not include any third-party prompt data and can be integrated into various AI architectures.
