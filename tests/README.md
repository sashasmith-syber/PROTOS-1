# Tests Directory

This directory contains test suites for the project components.

## Available Tests

### test_protos1_enforcer.py

Comprehensive unit tests for the PROTOS-1 enforcement system.

**Coverage:**
- Enforcer initialization and configuration
- Sanctuary directive (access control)
- Synthesis directive (packet validation)
- Logic directive (consensus reconciliation)
- Security protections (path traversal, fail-closed behavior)
- Edge cases and error conditions

**Run:**
```bash
python tests/test_protos1_enforcer.py
```

**Expected Output:**
All tests should pass. The test suite uses temporary files and cleans up after itself.

## Test Philosophy

Tests in this project follow these principles:

- **Isolation**: Each test is independent and doesn't affect others
- **Determinism**: Tests produce the same result every time
- **Safety**: Tests use temporary files and test data only
- **Clarity**: Test names clearly describe what is being tested
- **Coverage**: Both success and failure cases are tested

## Running Tests

### Run All Tests
```bash
python -m unittest discover tests
```

### Run Specific Test File
```bash
python tests/test_protos1_enforcer.py
```

### Run with Verbose Output
```bash
python tests/test_protos1_enforcer.py -v
```

## Adding New Tests

When adding tests:

1. Use descriptive test method names (e.g., `test_sanctuary_denies_unknown_source`)
2. Include docstrings explaining what is being tested
3. Use setUp/tearDown for test fixtures
4. Clean up any temporary files or resources
5. Test both success and failure cases
6. Test edge cases and boundary conditions
7. Update this README if adding a new test file

## Test Data

- Use temporary directories for file-based tests
- Never use real secrets or credentials
- Generate test data programmatically when possible
- Clean up all test data in tearDown methods

## Security Testing

Security-related tests should verify:

- Fail-closed behavior on errors
- Path traversal protection
- Input validation
- No sensitive data in error messages
- Proper handling of missing/malformed configuration
