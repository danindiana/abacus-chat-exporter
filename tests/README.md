# Test Suite for Abacus.AI Chat Exporter

This directory contains the comprehensive test suite for the Abacus.AI Chat Exporter project.

## Structure

```
tests/
├── README.md                 # This file
├── conftest.py              # Pytest configuration and shared fixtures
├── unit/                    # Unit tests
│   ├── test_sanitizers.py   # Tests for filename sanitization
│   ├── test_exporters.py    # Tests for export functions
│   └── test_pdf_processor.py # Tests for PDF processing
├── integration/             # Integration tests
└── fixtures/                # Test fixtures and mock data
```

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only API-related tests
pytest -m api

# Run tests for a specific module
pytest tests/unit/test_sanitizers.py

# Run a specific test class
pytest tests/unit/test_sanitizers.py::TestSanitizeFilenameBasic

# Run a specific test function
pytest tests/unit/test_sanitizers.py::TestSanitizeFilenameBasic::test_sanitize_normal_filename
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Tests in Parallel

```bash
# Run tests in parallel (faster)
pytest -n auto
```

## Test Markers

The test suite uses markers to categorize tests:

- `@pytest.mark.unit` - Unit tests for individual functions
- `@pytest.mark.integration` - Integration tests for workflows
- `@pytest.mark.api` - Tests that interact with APIs (mocked)
- `@pytest.mark.slow` - Tests that take a long time
- `@pytest.mark.requires_api_key` - Tests requiring real API credentials (skipped in CI)

### Running Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run all tests except slow ones
pytest -m "not slow"

# Run unit tests that don't require API
pytest -m "unit and not api"
```

## Writing Tests

### Basic Test Structure

```python
import pytest

class TestMyFeature:
    @pytest.mark.unit
    def test_something(self):
        # Arrange
        input_data = "test"

        # Act
        result = my_function(input_data)

        # Assert
        assert result == expected_output
```

### Using Fixtures

```python
@pytest.mark.unit
def test_with_fixture(mock_api_client, temp_output_dir):
    # Fixtures are automatically injected
    client = mock_api_client
    output = temp_output_dir / "test.txt"

    # Use the fixtures in your test
    assert client is not None
    assert output.parent.exists()
```

### Parametrized Tests

```python
@pytest.mark.unit
@pytest.mark.parametrize("input,expected", [
    ("test", "test"),
    ("test/path", "test_path"),
    ("test:name", "test-name"),
])
def test_multiple_inputs(input, expected):
    result = sanitize_filename(input)
    assert result == expected
```

## Available Fixtures

See `conftest.py` for the complete list of fixtures. Common ones include:

- `mock_api_key` - A test API key
- `mock_env_vars` - Mock environment variables
- `mock_api_client` - Mock Abacus.AI API client
- `mock_chat_session` - Mock chat session object
- `mock_project` - Mock project object
- `mock_deployment` - Mock deployment object
- `temp_output_dir` - Temporary directory for test outputs
- `sample_chat_data` - Sample chat data for testing

## Coverage Goals

- **Overall Coverage**: 80%+
- **Critical Functions**: 90%+
- **Utility Functions**: 100%

Current coverage status:
- Sanitizers: ~95% (comprehensive tests)
- Exporters: ~60% (basic tests, needs more edge cases)
- PDF Processor: ~55% (basic tests, needs integration tests)

## CI/CD Integration

Tests run automatically on:
- Every push to `main`, `develop`, and `claude/*` branches
- Every pull request to `main` and `develop`
- Can be triggered manually via GitHub Actions

### GitHub Actions Workflow

The `.github/workflows/tests.yml` workflow:
1. Runs tests on multiple OS (Ubuntu, macOS, Windows)
2. Tests against Python 3.8, 3.9, 3.10, 3.11, 3.12
3. Generates coverage reports
4. Uploads artifacts
5. Runs code quality checks

## Troubleshooting

### Tests Fail with Import Errors

Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Tests Fail with API Key Errors

Some tests require the `ABACUS_API_KEY` environment variable. In CI, a dummy key is provided. For local testing:
```bash
export ABACUS_API_KEY=test_dummy_key
pytest
```

### Coverage Too Low

To see which lines aren't covered:
```bash
pytest --cov=. --cov-report=term-missing
```

This will show line numbers that need test coverage.

## Adding New Tests

1. **Identify the module** to test (e.g., `new_feature.py`)
2. **Create test file** in appropriate directory (e.g., `tests/unit/test_new_feature.py`)
3. **Import the module** to test
4. **Write test classes** grouping related tests
5. **Add markers** (`@pytest.mark.unit`, etc.)
6. **Use fixtures** from `conftest.py` where appropriate
7. **Run tests** to verify they pass
8. **Check coverage** to ensure adequate coverage

## Best Practices

1. **One assertion per test** (when possible)
2. **Clear test names** describing what is being tested
3. **Use fixtures** for common setup
4. **Mock external dependencies** (API calls, file I/O)
5. **Test edge cases** (empty inputs, very long inputs, special characters)
6. **Test error handling** (exceptions, invalid inputs)
7. **Keep tests fast** (mock slow operations)
8. **Document complex tests** with comments

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## Questions?

If you have questions about the test suite, please:
1. Check this README
2. Review `conftest.py` for available fixtures
3. Look at existing tests for examples
4. Open an issue on GitHub
