# Configuration Directory

This directory contains configuration files for PROTOS-1 and other system components.

## Files

### sanctuary.conf

The PROTOS-1 Sanctuary allowlist. This file defines which source identifiers are authorized to access the system.

**Format:**
- One identifier per line
- Lines starting with # are comments
- Empty lines are ignored
- Exact string matching (no wildcards)

**Security:**
- Use non-sensitive identifiers only (node names, logical IDs)
- Do NOT include secrets or credentials
- This file should be version controlled
- Changes require enforcer reload or application restart

**Example:**
```
# Production nodes
node-alpha
node-beta

# Development
localhost
cursor-agent
```

## Adding New Configuration

When adding new configuration files:

1. Document the file format and purpose in this README
2. Provide an example or template
3. Add sensitive config files to .gitignore if they contain secrets
4. Use safe defaults that fail closed on missing configuration
5. Validate all configuration values before use

## Security Notes

- Configuration files in this directory should NOT contain secrets
- Use environment variables for sensitive values (API keys, passwords, etc.)
- All paths are validated to prevent traversal attacks
- Configuration is read-only at runtime (no writes to this directory)
