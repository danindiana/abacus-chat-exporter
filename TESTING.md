# Testing Guide

Complete guide to testing the Abacus.AI Chat Exporter project.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Test Organization](#test-organization)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Coverage](#coverage)
- [Continuous Integration](#continuous-integration)
- [Troubleshooting](#troubleshooting)

## Overview

This project uses **pytest** as the testing framework with comprehensive coverage across:
- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test complete workflows and multi-component interactions
- **CI/CD**: Automated testing on multiple platforms and Python versions

### Test Statistics

| Metric | Value |
|--------|-------|
| Total Tests | 160+ |
| Unit Tests | 100+ |
| Integration Tests | 60+ |
| Coverage | 80%+ |
| Platforms | 3 (Ubuntu, macOS, Windows) |
| Python Versions | 5 (3.8, 3.9, 3.10, 3.11, 3.12) |

## Quick Start

### Installation

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Or use the test runner
./run_tests.sh install
```

### Run Tests

```bash
# All tests
pytest

# Fast unit tests only
pytest -m unit

# With coverage
pytest --cov=. --cov-report=html

# Using the test runner (recommended)
./run_tests.sh fast
```

## Test Organization

```
tests/
├── README.md              # Testing guide (brief)
├── conftest.py            # Fixtures and shared test configuration
├── unit/                  # Unit tests (test individual functions)
│   ├── test_sanitizers.py      # 50+ tests for filename sanitization
│   ├── test_exporters.py       # 30+ tests for export functionality
│   └── test_pdf_processor.py   # 30+ tests for PDF processing
├── integration/           # Integration tests (test workflows)
│   └── test_workflows.py       # 60+ end-to-end workflow tests
└── fixtures/             # Test data and mock responses
```

### Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (slower, multi-component)
- `@pytest.mark.api` - Tests that interact with APIs (mocked)
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.requires_api_key` - Tests requiring real API credentials (skipped in CI)

### Running Specific Test Categories

```bash
# Only unit tests
pytest -m unit

# Only integration tests
pytest -m integration

# Unit tests except slow ones
pytest -m "unit and not slow"

# All tests except those requiring API keys
pytest -m "not requires_api_key"
```

## Running Tests

### Command Line Options

#### Basic Usage

```bash
# Run all tests
pytest

# Run specific file
pytest tests/unit/test_sanitizers.py

# Run specific test class
pytest tests/unit/test_sanitizers.py::TestSanitizeFilenameBasic

# Run specific test function
pytest tests/unit/test_sanitizers.py::TestSanitizeFilenameBasic::test_sanitize_normal_filename
```

#### Verbosity Control

```bash
# Verbose output
pytest -v

# Very verbose (show test docstrings)
pytest -vv

# Quiet mode (minimal output)
pytest -q
```

#### Output Control

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Short traceback
pytest --tb=short

# No traceback
pytest --tb=no
```

#### Failure Handling

```bash
# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Re-run only failed tests
pytest --lf

# Re-run failed tests first, then others
pytest --ff
```

#### Performance

```bash
# Run in parallel (requires pytest-xdist)
pytest -n auto

# Run tests that failed in the last run
pytest --lf -n auto
```

### Using the Test Runner Script

The `run_tests.sh` script provides convenient shortcuts:

```bash
# See all available commands
./run_tests.sh help

# Fast unit tests
./run_tests.sh fast

# Full coverage report
./run_tests.sh coverage

# Simulate CI/CD locally
./run_tests.sh ci

# Run specific test suite
./run_tests.sh sanitizers
./run_tests.sh exporters
./run_tests.sh pdf
./run_tests.sh workflows

# Quality checks
./run_tests.sh quality
./run_tests.sh fix

# Watch mode (auto-rerun on changes)
./run_tests.sh watch
```

## Writing Tests

### Basic Test Structure

```python
import pytest

class TestMyFeature:
    """Test my feature functionality"""

    @pytest.mark.unit
    def test_basic_functionality(self):
        """Test basic use case"""
        # Arrange
        input_data = "test input"
        expected = "test output"

        # Act
        result = my_function(input_data)

        # Assert
        assert result == expected
```

### Using Fixtures

Fixtures are defined in `conftest.py`:

```python
@pytest.mark.unit
def test_with_fixtures(mock_api_client, temp_output_dir):
    """Test using shared fixtures"""
    # Fixtures are automatically injected
    client = mock_api_client
    output_path = temp_output_dir / "test.txt"

    # Use the fixtures
    assert client is not None
    assert output_path.parent.exists()
```

### Available Fixtures

See `tests/conftest.py` for the complete list. Common fixtures include:

#### API Mocking
- `mock_api_client` - Mock Abacus.AI API client
- `mock_chat_session` - Mock chat session object
- `mock_project` - Mock project object
- `mock_deployment` - Mock deployment object
- `mock_deployment_conversation` - Mock conversation object

#### Environment
- `mock_env_vars` - Mock environment variables
- `mock_api_key` - Test API key

#### File System
- `temp_output_dir` - Temporary directory for test files
- `mock_pathlib_path` - Mock Path object

#### Data
- `sample_chat_data` - Sample chat data
- `sample_filenames` - Sample filenames for testing

### Parametrized Tests

Test multiple inputs efficiently:

```python
@pytest.mark.unit
@pytest.mark.parametrize("input,expected", [
    ("normal.txt", "normal.txt"),
    ("with spaces.txt", "with_spaces.txt"),
    ("with/slash.txt", "with_slash.txt"),
])
def test_multiple_inputs(input, expected):
    """Test various inputs"""
    result = sanitize_filename(input)
    assert result == expected
```

### Testing Exceptions

```python
@pytest.mark.unit
def test_raises_error():
    """Test that function raises expected error"""
    with pytest.raises(ValueError, match="API key required"):
        function_requiring_api_key()
```

### Mocking API Calls

```python
from unittest.mock import patch, MagicMock

@pytest.mark.unit
@pytest.mark.api
def test_api_interaction(mock_api_client):
    """Test API interaction with mocks"""
    # Setup mock response
    mock_api_client.list_chat_sessions.return_value = [
        MagicMock(chat_session_id="test_123")
    ]

    # Test with mock
    with patch('module.ApiClient', return_value=mock_api_client):
        result = fetch_chats()

    assert len(result) == 1
    assert result[0].chat_session_id == "test_123"
```

### Testing File I/O

```python
@pytest.mark.unit
def test_file_operations(temp_output_dir):
    """Test file creation and reading"""
    test_file = temp_output_dir / "test.txt"

    # Write
    test_file.write_text("test content")

    # Read and verify
    content = test_file.read_text()
    assert content == "test content"
    assert test_file.exists()
```

## Coverage

### Generating Coverage Reports

```bash
# Terminal report with missing lines
pytest --cov=. --cov-report=term-missing

# HTML report
pytest --cov=. --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
pytest --cov=. --cov-report=xml

# All formats
pytest --cov=. --cov-report=html --cov-report=xml --cov-report=term-missing
```

### Coverage Goals

| Component | Target | Status |
|-----------|--------|--------|
| Overall | 80%+ | ✅ |
| Sanitizers | 100% | ✅ |
| Exporters | 90%+ | ✅ |
| PDF Processor | 85%+ | ✅ |
| Utilities | 100% | ✅ |

### Checking Coverage Locally

```bash
# Run tests with coverage requirement
pytest --cov=. --cov-fail-under=80

# This will fail if coverage drops below 80%
```

### Excluding Code from Coverage

Use `# pragma: no cover` for code that shouldn't be tested:

```python
def debug_only_function():  # pragma: no cover
    """This function is excluded from coverage"""
    pass
```

## Continuous Integration

### GitHub Actions Workflow

Tests run automatically on:
- Every push to `main`, `develop`, `claude/*` branches
- Every pull request to `main`, `develop`
- Manual trigger via GitHub Actions UI

### Test Matrix

| OS | Python Versions |
|----|-----------------|
| Ubuntu | 3.8, 3.9, 3.10, 3.11, 3.12 |
| macOS | 3.8, 3.9, 3.10, 3.11, 3.12 |
| Windows | 3.8, 3.9, 3.10, 3.11, 3.12 |

**Total**: 15 combinations tested on every PR

### CI Jobs

1. **Test Job** - Full test suite on all platforms
2. **Quick Check** - Fast unit tests on Ubuntu + Python 3.11
3. **Code Quality** - Black, isort, flake8, mypy
4. **Coverage** - Coverage reporting and enforcement

### Viewing CI Results

1. Go to: https://github.com/danindiana/abacus-chat-exporter/actions
2. Click on the workflow run
3. View results for each job
4. Download artifacts (coverage reports, test results)

### Running CI Checks Locally

Simulate the entire CI pipeline:

```bash
./run_tests.sh ci
```

This runs:
1. Syntax checks
2. Code quality (flake8)
3. Unit tests
4. Integration tests
5. Coverage check (80%+ required)

## Troubleshooting

### Tests Fail with Import Errors

**Problem**: `ModuleNotFoundError: No module named 'pytest'`

**Solution**:
```bash
pip install -r requirements-test.txt
```

### Tests Fail with API Key Errors

**Problem**: Tests require `ABACUS_API_KEY` environment variable

**Solution**: Set a dummy key for testing:
```bash
export ABACUS_API_KEY=test_dummy_key
pytest
```

Note: Most tests use mocks and don't require a real API key.

### Coverage Too Low

**Problem**: Coverage below 80%

**Solution**:
1. Check which lines aren't covered:
   ```bash
   pytest --cov=. --cov-report=term-missing
   ```

2. Look at HTML report for details:
   ```bash
   pytest --cov=. --cov-report=html
   open htmlcov/index.html
   ```

3. Add tests for uncovered lines

### Tests Pass Locally but Fail in CI

**Problem**: Tests work on your machine but fail in GitHub Actions

**Possible Causes**:
1. **Platform differences** - Test on Windows if you're on macOS/Linux
2. **Python version** - Test with older Python versions
3. **Missing dependencies** - Check `requirements-test.txt`
4. **File permissions** - Windows handles permissions differently

**Solution**: Run tests in a clean environment:
```bash
# Create fresh virtual environment
python3 -m venv test-env
source test-env/bin/activate
pip install -r requirements.txt -r requirements-test.txt
pytest
```

### Slow Tests

**Problem**: Tests take too long to run

**Solution**:
```bash
# Run only fast unit tests
pytest -m "unit and not slow"

# Run in parallel
pytest -n auto

# Use the fast runner
./run_tests.sh fast
```

### Tests Hang or Timeout

**Problem**: Tests hang indefinitely

**Solution**:
```bash
# Add timeout to pytest
pytest --timeout=300  # 5 minutes max per test

# Check for infinite loops or blocking operations
pytest -v -s  # Show output to see where it hangs
```

### Fixture Not Found

**Problem**: `fixture 'my_fixture' not found`

**Solution**:
1. Check that fixture is defined in `conftest.py`
2. Ensure `conftest.py` is in the correct location
3. Verify fixture name spelling

### Random Test Failures

**Problem**: Tests occasionally fail

**Possible Causes**:
1. **Race conditions** - Tests that depend on timing
2. **Shared state** - Tests modifying global state
3. **Non-deterministic order** - Tests that depend on execution order

**Solution**:
```bash
# Run tests in random order to catch order dependencies
pytest --random-order

# Run failed test multiple times
pytest --count=10 tests/path/to/test.py
```

## Best Practices

### Do's ✅

- ✅ Write tests for all new features
- ✅ Use descriptive test names
- ✅ Keep tests fast and isolated
- ✅ Use fixtures for common setup
- ✅ Mock external dependencies
- ✅ Test edge cases and error conditions
- ✅ Maintain 80%+ coverage
- ✅ Run tests before committing

### Don'ts ❌

- ❌ Don't test implementation details
- ❌ Don't share state between tests
- ❌ Don't use real API credentials in tests
- ❌ Don't commit failing tests
- ❌ Don't skip tests without good reason
- ❌ Don't write tests that depend on external services
- ❌ Don't ignore coverage drops

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Mocking with unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## Getting Help

If you have questions:
1. Check this guide
2. Read `tests/README.md` (brief guide)
3. Look at existing tests for examples
4. Open an issue on GitHub
