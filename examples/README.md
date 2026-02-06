# Examples Directory

This directory contains example code demonstrating how to use various components of the system.

## Available Examples

### protos1_integration_example.py

Demonstrates how to integrate PROTOS-1 enforcement into a request handler.

**Shows:**
- Sanctuary access control
- Synthesis packet validation
- Logic consensus reconciliation
- Complete request flow with all three directives
- Error handling and fail-closed behavior

**Run:**
```bash
python examples/protos1_integration_example.py
```

**Output:**
The example runs several test scenarios showing successful and failed enforcement checks.

## Using Examples

Examples are designed to be:

- **Self-contained**: Run without additional setup
- **Educational**: Include comments explaining each step
- **Safe**: Use only test data, no real secrets or external calls
- **Adaptable**: Copy and modify for your specific use case

## Adding New Examples

When adding examples:

1. Use descriptive filenames (e.g., `feature_name_example.py`)
2. Include a docstring explaining the example's purpose
3. Add comments for non-obvious code sections
4. Ensure the example runs without errors
5. Update this README with a description
6. Keep examples focused on one feature or integration pattern

## Security

Examples should never:

- Access real secrets or credentials
- Make external network calls (except localhost)
- Modify files outside the examples directory
- Require elevated privileges
- Include hardcoded sensitive data
