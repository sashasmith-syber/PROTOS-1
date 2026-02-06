# Contributing to PROTOS-1

Thank you for your interest in contributing to PROTOS-1! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a code of conduct (see `CODE_OF_CONDUCT.md`). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

If you find a bug:

1. **Check existing issues** to see if it's already reported
2. **Create a new issue** with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Python version and OS
   - Relevant code snippets or error messages

### Suggesting Enhancements

For feature requests or enhancements:

1. **Open an issue** with the "enhancement" label
2. **Describe**:
   - The problem you're trying to solve
   - Your proposed solution
   - Alternative solutions considered
   - Impact on existing functionality

### Security Vulnerabilities

**Do NOT report security vulnerabilities via public issues.** See `SECURITY.md` for responsible disclosure guidelines.

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- No external dependencies required (Python stdlib only)

### Setting Up Your Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/PROTOS-1.git
cd PROTOS-1

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify setup
python protos/protos1_selftest.py
python tests/test_protos1_enforcer.py
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Use descriptive branch names:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation
- `test/` for test improvements

### 2. Make Your Changes

Follow these guidelines:

#### Code Style

- **PEP 8** compliance for Python code
- **Docstrings** for all public functions and classes
- **Type hints** where appropriate
- **Comments** for complex logic
- **No external dependencies** - use Python stdlib only

#### Code Quality

- **Small, focused commits** - One logical change per commit
- **Clear commit messages** - Follow conventional commits format
- **No secrets** - Never commit API keys, passwords, or credentials
- **No network calls** - PROTOS-1 is local-only by design
- **Fail closed** - All security checks must deny on errors

#### Testing

- **Write tests** for all new features
- **Update tests** when fixing bugs
- **Ensure all tests pass** before submitting
- **Test edge cases** and error conditions
- **No external dependencies** in tests

### 3. Run Tests

```bash
# Run self-test
python protos/protos1_selftest.py

# Run unit tests
python tests/test_protos1_enforcer.py

# Run integration example
python examples/protos1_integration_example.py
```

All tests must pass before submitting a pull request.

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature

Detailed description of what changed and why."
```

Use conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `test:` - Test improvements
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- **Clear title** describing the change
- **Description** explaining what and why
- **Link to related issues** (if any)
- **Screenshots** (if UI-related)

## Pull Request Guidelines

### Before Submitting

- ✅ All tests pass
- ✅ Code follows style guidelines
- ✅ Documentation is updated
- ✅ Commit messages are clear
- ✅ No merge conflicts
- ✅ Branch is up to date with main

### Review Process

1. **Automated checks** run on your PR
2. **Maintainer review** - May request changes
3. **Discussion** - Address feedback
4. **Approval** - Once approved, PR is merged
5. **Credit** - You'll be listed as a contributor

### What We Look For

- **Correctness** - Does it work as intended?
- **Security** - Does it maintain fail-closed behavior?
- **Testing** - Are there adequate tests?
- **Documentation** - Is it well-documented?
- **Style** - Does it follow project conventions?
- **Scope** - Is the change focused and minimal?

## Testing Guidelines

### Unit Tests

- Test individual functions in isolation
- Use deterministic test data
- Cover success and failure cases
- Test edge cases and boundaries
- No external dependencies

### Integration Tests

- Test multiple components together
- Verify directive interactions
- Test realistic scenarios
- Ensure fail-closed behavior

### Test Data

- Use temporary files/directories
- Clean up in `tearDown()`
- No real secrets or credentials
- Reproducible across environments

## Documentation Guidelines

### Code Documentation

- **Docstrings** for all public APIs
- **Inline comments** for complex logic
- **Type hints** for function signatures
- **Examples** in docstrings where helpful

### User Documentation

- Update `README.md` for user-facing changes
- Update `docs/` for conceptual changes
- Keep examples up to date
- Maintain `CHANGELOG.md`

## Style Expectations

### Python Code

```python
def enforce_sanctuary(source_identifier: str) -> Tuple[bool, str]:
    """
    Validate source authorization.
    
    Args:
        source_identifier: Non-sensitive identifier
        
    Returns:
        Tuple of (is_allowed, message)
    """
    if not source_identifier:
        return False, "Invalid source"
    # Implementation...
```

### Commit Messages

```
feat: add consensus threshold validation

- Validate threshold is between 0.0 and 1.0
- Add unit tests for edge cases
- Update documentation

Closes #123
```

## Questions?

- **GitHub Issues**: For bugs and features
- **GitHub Discussions**: For questions and ideas
- **Security**: See `SECURITY.md` for vulnerability reporting

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to PROTOS-1! 🎉
