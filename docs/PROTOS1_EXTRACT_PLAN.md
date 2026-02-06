# PROTOS-1 Extraction Plan

This document provides instructions for extracting PROTOS-1 into its own standalone repository, separate from any external prompt collections.

## Purpose

PROTOS-1 is a security framework designed to work with AI agent systems and external prompt collections, but it does not include any third-party prompt data. This extraction creates a clean repository containing only the PROTOS-1 security enforcement code and documentation.

## Files to Copy

The following directories and files should be copied to the new PROTOS-1 repository:

### Core Implementation
- `protos/` - Complete directory containing all PROTOS-1 code
  - `__init__.py`
  - `protos1_enforcer.py`
  - `protos1_gateway.py`
  - `protos1_selftest.py`
  - `README.md` (internal module documentation)
  - `LICENSE` (MIT license for PROTOS-1)
  - `README_STANDALONE.md` (rename to `../README.md` in new repo)

### Configuration
- `config/` - Complete directory
  - `sanctuary.conf`
  - `README.md`

### Tests
- `tests/` - Complete directory
  - `test_protos1_enforcer.py`
  - `README.md`

### Examples
- `examples/` - Complete directory
  - `protos1_integration_example.py`
  - `README.md`

### Documentation
- `docs/protos1-integration.md` - Integration guide
- `PROTOS1_INTEGRATION_SUMMARY.md` - Implementation review

### Infrastructure
- `.gitignore` - Python/IDE ignore rules (can be copied or recreated)
- `CHANGELOG.md` - Extract only PROTOS-1 sections

## Files and Directories to Exclude

Do NOT copy any directories containing external prompt collections or third-party AI system prompts. These are separate projects and should not be included in the PROTOS-1 repository.

Specifically exclude all vendor-specific directories that contain proprietary prompt data from various AI systems and platforms. The PROTOS-1 framework is designed to work alongside such collections but remains independent and does not embed their content.

Also exclude:
- `docs/local-llm-setup.md` - This is specific to Ollama integration, not core PROTOS-1
- `scripts/` - Ollama-specific helper scripts
- `tools/` - Ollama test client
- `.env.example` - Ollama configuration template

## Extraction Steps

### Step 1: Create New Repository Structure

```bash
# Create new directory for PROTOS-1
mkdir protos-1
cd protos-1

# Initialize git repository
git init
```

### Step 2: Copy PROTOS-1 Files

```bash
# From the source directory, copy PROTOS-1 files
# Adjust paths based on your source location

# Copy core implementation
cp -r /path/to/source/protos ./

# Copy configuration
cp -r /path/to/source/config ./

# Copy tests
cp -r /path/to/source/tests ./

# Copy examples
cp -r /path/to/source/examples ./

# Create docs directory and copy documentation
mkdir docs
cp /path/to/source/docs/protos1-integration.md ./docs/

# Copy top-level documentation
cp /path/to/source/PROTOS1_INTEGRATION_SUMMARY.md ./

# Copy infrastructure files
cp /path/to/source/.gitignore ./
```

### Step 3: Rename and Organize

```bash
# Move the standalone README to root
mv protos/README_STANDALONE.md README.md

# Move LICENSE to root
mv protos/LICENSE LICENSE

# The protos/README.md can stay as internal module documentation
```

### Step 4: Update CHANGELOG

Create a new `CHANGELOG.md` in the root with only PROTOS-1 version history. Extract the relevant sections from the source CHANGELOG.md that pertain to PROTOS-1 features and security updates.

### Step 5: Verify Structure

Your new repository should have this structure:

```
protos-1/
├── protos/
│   ├── __init__.py
│   ├── protos1_enforcer.py
│   ├── protos1_gateway.py
│   ├── protos1_selftest.py
│   └── README.md
├── config/
│   ├── sanctuary.conf
│   └── README.md
├── tests/
│   ├── test_protos1_enforcer.py
│   └── README.md
├── examples/
│   ├── protos1_integration_example.py
│   └── README.md
├── docs/
│   └── protos1-integration.md
├── PROTOS1_INTEGRATION_SUMMARY.md
├── CHANGELOG.md
├── LICENSE
├── README.md
└── .gitignore
```

### Step 6: Run Tests

Verify everything works in the new repository:

```bash
# Run self-test
python protos/protos1_selftest.py

# Run unit tests
python tests/test_protos1_enforcer.py

# Run integration example
python examples/protos1_integration_example.py
```

All tests should pass without modification since PROTOS-1 has no external dependencies beyond Python's standard library.

### Step 7: Initialize Git

```bash
# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: PROTOS-1 Security Framework v1.0.0"

# Add remote (update URL to your repository)
git remote add origin https://github.com/sashasmith-syber/protos-1.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 8: GitHub Repository Setup

On GitHub, configure the repository:

1. Add repository description: "A security enforcement protocol for AI agent systems"
2. Add topics: `security`, `ai`, `python`, `consensus`, `access-control`
3. Enable security features:
   - Dependabot alerts (though PROTOS-1 has no dependencies)
   - Secret scanning
   - Code scanning (optional)
4. Create a release tag for v1.0.0

## Post-Extraction Verification

After extraction, verify:

1. All tests pass in the new repository
2. No references to external prompt collections in the code
3. LICENSE file is present and correct
4. README.md clearly states authorship
5. Documentation is complete and self-contained
6. No sensitive data or credentials are present

## Maintenance

The extracted PROTOS-1 repository is now independent and can be maintained separately. Any updates to PROTOS-1 should be made in the standalone repository, not in collections that may include external prompt data.

## Security Note

PROTOS-1 is designed as a security layer that can be integrated with various AI systems. It does not include proprietary prompts or system instructions from external sources. Users who wish to combine PROTOS-1 with external prompt collections should do so in their own integration repositories, keeping the components properly separated.
