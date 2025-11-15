# Development Guide

Complete guide for developers contributing to the Abacus.AI Chat Exporter project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Git Workflow](#git-workflow)
- [Pull Request Process](#pull-request-process)
- [Code Review Guidelines](#code-review-guidelines)
- [Release Process](#release-process)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)
- Text editor or IDE (VSCode, PyCharm, etc.)

### Initial Setup

```bash
# 1. Clone the repository
git clone https://github.com/danindiana/abacus-chat-exporter.git
cd abacus-chat-exporter

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-test.txt

# 4. Install pre-commit hooks
pip install pre-commit
pre-commit install

# 5. Verify setup
./run_tests.sh fast
```

## Development Environment

### Recommended Tools

#### Code Editors

**VSCode** (Recommended)
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true,
  "editor.rulers": [100]
}
```

**PyCharm** (Alternative)
- Enable Black formatter
- Configure pytest as test runner
- Set line length to 100

#### Extensions/Plugins

- **VSCode**:
  - Python (Microsoft)
  - Pylance
  - Python Test Explorer
  - GitLens
  - YAML

- **PyCharm**:
  - Black Formatter
  - pytest runner (built-in)

### Environment Variables

Create a `.env` file for local development (do NOT commit):

```bash
# .env (local only - do not commit!)
ABACUS_API_KEY=your_test_api_key_here
DEPLOYMENT_ID=your_test_deployment_id
```

Load environment variables:
```bash
# Using python-dotenv
pip install python-dotenv

# In your code
from dotenv import load_dotenv
load_dotenv()
```

## Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length**: 100 characters (not 79)
- **Strings**: Double quotes preferred
- **Imports**: Grouped and sorted with isort
- **Formatting**: Automated with Black

### Formatting Tools

#### Black (Code Formatter)

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check --diff .

# Format specific file
black path/to/file.py
```

Configuration in `pyproject.toml`:
```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']
```

#### isort (Import Sorting)

```bash
# Sort imports in all files
isort .

# Check without making changes
isort --check-only --diff .

# Sort specific file
isort path/to/file.py
```

Configuration in `pyproject.toml`:
```toml
[tool.isort]
profile = "black"
line_length = 100
```

### Linting Tools

#### flake8

```bash
# Run flake8 on all files
flake8 .

# Run on specific file
flake8 path/to/file.py
```

Common warnings to fix:
- `E501` - Line too long (over 100 chars)
- `F401` - Imported but unused
- `E302` - Expected 2 blank lines
- `W503` - Line break before binary operator (ignored)

#### mypy (Type Checking - Optional)

```bash
# Run type checking
mypy *.py

# Ignore missing imports
mypy --ignore-missing-imports *.py
```

Configuration in `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.8"
ignore_missing_imports = true
```

### Code Quality Commands

```bash
# Run all quality checks
./run_tests.sh quality

# Auto-fix what can be fixed
./run_tests.sh fix

# Manual commands
black .
isort .
flake8 .
mypy *.py
```

## Testing

### Test-Driven Development (TDD)

Follow this workflow:

1. **Write failing test** - Test the feature you want to add
2. **Run test** - Verify it fails (proves test is needed)
3. **Write minimal code** - Make the test pass
4. **Run test** - Verify it passes
5. **Refactor** - Improve code while keeping tests green

Example:
```python
# 1. Write failing test
def test_new_feature():
    result = new_function("input")
    assert result == "expected"

# 2. Run test - it fails (function doesn't exist)
# 3. Write minimal code
def new_function(input):
    return "expected"

# 4. Run test - it passes
# 5. Refactor if needed
```

### Running Tests During Development

```bash
# Fast feedback loop
./run_tests.sh fast

# Watch mode (auto-rerun on changes)
./run_tests.sh watch

# Run tests for specific module
pytest tests/unit/test_sanitizers.py -v

# Re-run only failed tests
pytest --lf
```

### Test Coverage Requirements

- **Minimum**: 80% overall coverage
- **New code**: 100% coverage for new functions
- **Critical paths**: 100% coverage

Check coverage:
```bash
./run_tests.sh coverage
open htmlcov/index.html
```

### Writing Good Tests

**Good Test Example**:
```python
@pytest.mark.unit
def test_sanitize_removes_slashes():
    """Test that forward slashes are replaced with underscores"""
    # Arrange
    filename = "path/to/file.txt"

    # Act
    result = sanitize_filename(filename)

    # Assert
    assert "/" not in result
    assert result == "path_to_file.txt"
```

**Characteristics of Good Tests**:
- ✅ Clear, descriptive name
- ✅ Tests one thing
- ✅ Fast (< 1 second)
- ✅ Isolated (no external dependencies)
- ✅ Repeatable (same result every time)
- ✅ Has assertion
- ✅ Well-documented

See [TESTING.md](TESTING.md) for comprehensive testing guide.

## Pre-commit Hooks

### What Are Pre-commit Hooks?

Automated checks that run before each commit to ensure code quality.

### Installing Hooks

```bash
# Install pre-commit package
pip install pre-commit

# Install git hooks
pre-commit install

# Hooks now run automatically on git commit
```

### What Gets Checked

Before each commit, these checks run:

1. **Trailing whitespace** - Removed automatically
2. **End of file** - Ensures files end with newline
3. **YAML/JSON** - Validates syntax
4. **Python syntax** - Checks for syntax errors
5. **Black** - Formats code
6. **isort** - Sorts imports
7. **flake8** - Lints code
8. **mypy** - Type checks (optional)
9. **bandit** - Security scanner
10. **detect-secrets** - Prevents committing secrets
11. **Fast tests** - Runs quick unit tests

### Manual Hook Execution

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files
pre-commit run pytest-check --all-files

# Skip hooks for one commit (not recommended)
git commit --no-verify -m "message"
```

### Updating Hooks

```bash
# Update to latest hook versions
pre-commit autoupdate

# Clean and reinstall
pre-commit clean
pre-commit install
```

## Git Workflow

### Branch Naming

Follow this pattern: `<type>/<description>`

**Types**:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/changes

**Examples**:
```bash
feature/add-csv-export
bugfix/fix-unicode-handling
docs/update-api-docs
refactor/simplify-sanitizer
```

### Development Workflow

```bash
# 1. Create branch from main
git checkout main
git pull origin main
git checkout -b feature/my-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add my feature"

# 3. Keep branch updated
git fetch origin
git rebase origin/main

# 4. Push to remote
git push -u origin feature/my-feature

# 5. Create pull request on GitHub
```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance

**Examples**:
```bash
feat: add CSV export functionality
fix: handle unicode characters in filenames
docs: update installation instructions
test: add tests for PDF processing
refactor: simplify sanitize_filename function
```

**Good Commit**:
```
feat(export): add support for CSV export format

- Add CSV writer utility function
- Update export functions to support CSV
- Add tests for CSV export
- Update documentation

Closes #123
```

## Pull Request Process

### Before Creating PR

1. **Run all checks**:
   ```bash
   ./run_tests.sh ci
   ```

2. **Update documentation** if needed

3. **Rebase on latest main**:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. **Squash commits** if needed:
   ```bash
   git rebase -i origin/main
   ```

### Creating Pull Request

1. **Push branch**:
   ```bash
   git push -u origin feature/my-feature
   ```

2. **On GitHub**:
   - Click "Compare & pull request"
   - Fill in PR template
   - Link related issues
   - Request reviewers

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Coverage maintained/improved

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
```

### After PR Creation

1. **Wait for CI** - Ensure all checks pass
2. **Address feedback** - Respond to review comments
3. **Update if needed** - Push additional commits
4. **Get approval** - Need at least 1 approval
5. **Squash and merge** - Maintainer will merge

## Code Review Guidelines

### For Authors

**Before Requesting Review**:
- ✅ All tests pass
- ✅ Code is self-documented
- ✅ No unnecessary changes
- ✅ Commit messages are clear
- ✅ PR description is complete

**Responding to Feedback**:
- Respond to all comments
- Ask questions if unclear
- Push fixes as new commits
- Mark conversations as resolved
- Thank reviewers

### For Reviewers

**What to Review**:
1. **Correctness** - Does it work?
2. **Tests** - Are there adequate tests?
3. **Style** - Follows project standards?
4. **Documentation** - Is it clear?
5. **Performance** - Any concerns?
6. **Security** - Any vulnerabilities?

**How to Review**:
- Be kind and constructive
- Explain reasoning
- Suggest alternatives
- Approve when ready
- Use "Request changes" for issues

**Review Checklist**:
- [ ] Code is clear and maintainable
- [ ] Tests cover new functionality
- [ ] No security vulnerabilities
- [ ] Documentation is updated
- [ ] No breaking changes (or noted)
- [ ] Performance is acceptable

## Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** - Breaking changes (v1.0.0 → v2.0.0)
- **MINOR** - New features (v1.0.0 → v1.1.0)
- **PATCH** - Bug fixes (v1.0.0 → v1.0.1)

### Creating a Release

```bash
# 1. Update version in appropriate files
# 2. Update CHANGELOG.md
# 3. Commit changes
git add .
git commit -m "chore: bump version to v1.2.0"

# 4. Create tag
git tag -a v1.2.0 -m "Version 1.2.0"

# 5. Push tag
git push origin v1.2.0

# 6. Create GitHub release from tag
# 7. Publish to PyPI (if applicable)
```

## Development Tips

### Debugging

```bash
# Run tests with debugging output
pytest -vv -s --tb=long

# Use pdb debugger
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Print debug info in tests
import pytest; pytest.set_trace()
```

### Performance Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest
```

### Common Tasks

```bash
# Clean build artifacts
./run_tests.sh clean

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check for outdated packages
pip list --outdated

# Update dependencies
pip install --upgrade -r requirements.txt
```

### IDE Configuration

**VSCode** (`settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Args": ["--max-line-length=100"],
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["-v"],
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
```

## Security

### Handling Secrets

**Never commit**:
- API keys
- Passwords
- Private keys
- Tokens
- `.env` files

**If you accidentally commit a secret**:
1. Rotate the secret immediately
2. Remove from git history
3. Force push to remote
4. Notify maintainers

### Security Scanning

```bash
# Run security scan
bandit -r .

# Check dependencies for vulnerabilities
safety check

# Both are run automatically by pre-commit hooks
```

## Getting Help

**Resources**:
- 📖 [README.md](README.md) - Project overview
- 🧪 [TESTING.md](TESTING.md) - Testing guide
- 🔀 [GIT_WORKFLOW.md](GIT_WORKFLOW.md) - Git workflow
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture docs
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guide

**Support**:
- Open an issue on GitHub
- Ask in pull request comments
- Check existing issues for similar problems

## Additional Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

---

Happy coding! 🎉
