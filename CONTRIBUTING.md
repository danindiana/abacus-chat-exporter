# Contributing to Abacus Chat Exporter

Thank you for your interest in contributing to this project! This guide will help you understand the development workflow and git practices.

## 📋 Table of Contents

- [Development Workflow](#development-workflow)
- [Git Workflow](#git-workflow)
- [Branching Strategy](#branching-strategy)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)

## 🔄 Development Workflow

### Git Branching Workflow

```mermaid
gitGraph
    commit id: "Initial commit"
    commit id: "Add export tools"
    branch feature/pdf-processor
    checkout feature/pdf-processor
    commit id: "Add PDF processor"
    commit id: "Add tests"
    checkout main
    merge feature/pdf-processor
    branch feature/diagnostic-tools
    checkout feature/diagnostic-tools
    commit id: "Add chat finder"
    commit id: "Add API explorer"
    checkout main
    merge feature/diagnostic-tools
    commit id: "Release v1.0"
```

### Contribution Flow

```mermaid
flowchart TD
    Start([Start Contributing]) --> Fork[Fork Repository]
    Fork --> Clone[Clone Your Fork]
    Clone --> Branch[Create Feature Branch]
    Branch --> Code[Write Code]
    Code --> Test[Run Tests]
    Test --> TestPass{Tests Pass?}
    TestPass -->|No| Fix[Fix Issues]
    Fix --> Test
    TestPass -->|Yes| Commit[Commit Changes]
    Commit --> Push[Push to Fork]
    Push --> PR[Create Pull Request]
    PR --> Review{Code Review}
    Review -->|Changes Requested| Code
    Review -->|Approved| Merge[Merge to Main]
    Merge --> End([Contribution Complete])
```

## 🌿 Branching Strategy

### Branch Types

```mermaid
graph TD
    A[main] --> B[feature/*]
    A --> C[bugfix/*]
    A --> D[hotfix/*]
    A --> E[docs/*]
    A --> F[refactor/*]

    B --> B1[feature/new-exporter]
    B --> B2[feature/improved-logging]

    C --> C1[bugfix/api-timeout]
    C --> C2[bugfix/encoding-issue]

    D --> D1[hotfix/critical-auth-bug]

    E --> E1[docs/update-readme]
    E --> E2[docs/add-examples]

    F --> F1[refactor/extract-utils]
    F --> F2[refactor/modularize-code]
```

### Branch Naming Convention

- **feature/**: New features or enhancements
  - Example: `feature/add-csv-export`

- **bugfix/**: Bug fixes
  - Example: `bugfix/fix-encoding-error`

- **hotfix/**: Critical fixes that need immediate deployment
  - Example: `hotfix/auth-vulnerability`

- **docs/**: Documentation updates
  - Example: `docs/improve-quickstart`

- **refactor/**: Code refactoring without changing functionality
  - Example: `refactor/extract-api-client`

- **claude/**: Automated branches created by Claude Code
  - Example: `claude/add-git-mermaid-diagrams-01PX6RZWMiQhzbikYDiBGzEw`
  - These follow the pattern: `claude/<description>-<session-id>`

## 📝 Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
# Good commit messages
feat: add CSV export format support
fix: resolve encoding error in chat export
docs: update installation instructions
refactor: extract API client into separate module

# Bad commit messages
update stuff
fix bug
changes
```

### Commit Workflow Diagram

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Local as Local Repo
    participant Remote as Remote Repo
    participant CI as CI/CD Pipeline

    Dev->>Local: Stage changes (git add)
    Dev->>Local: Commit (git commit)
    Local->>Local: Pre-commit hooks run
    Dev->>Remote: Push (git push)
    Remote->>CI: Trigger CI/CD
    CI->>CI: Run tests
    CI->>CI: Run linters
    CI->>Remote: Report status
    Remote-->>Dev: CI status notification
```

## 🔀 Pull Request Process

### PR Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft: Create PR
    Draft --> Open: Mark ready for review
    Open --> InReview: Reviewer assigned
    InReview --> ChangesRequested: Issues found
    ChangesRequested --> InReview: Updates pushed
    InReview --> Approved: Review passed
    Approved --> Merged: Merge to main
    Merged --> [*]

    Draft --> Closed: Abandoned
    Open --> Closed: Abandoned
    ChangesRequested --> Closed: Abandoned
```

### Creating a Pull Request

1. **Ensure your branch is up to date**
   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Push your changes**
   ```bash
   git push origin your-feature-branch
   ```

3. **Create PR with descriptive title and body**
   ```markdown
   ## Summary
   Brief description of changes

   ## Changes Made
   - Added feature X
   - Fixed bug Y
   - Updated documentation Z

   ## Testing
   - [ ] Unit tests pass
   - [ ] Manual testing completed
   - [ ] Documentation updated

   ## Related Issues
   Closes #123
   ```

### Review Process

```mermaid
flowchart LR
    A[PR Submitted] --> B{Automated Checks}
    B -->|Pass| C[Code Review]
    B -->|Fail| D[Fix Issues]
    D --> A
    C --> E{Review Status}
    E -->|Approved| F[Merge]
    E -->|Changes Requested| G[Update Code]
    G --> C
    F --> H[Delete Branch]
    H --> I[Done]
```

## 🎨 Code Style

### Python Code Style

- Follow PEP 8
- Use type hints where applicable
- Maximum line length: 100 characters
- Use meaningful variable names

### Example

```python
from typing import List, Optional
from pathlib import Path


def export_chat_session(
    session_id: str,
    output_dir: Path,
    format: str = "html"
) -> Optional[Path]:
    """
    Export a chat session to the specified format.

    Args:
        session_id: The ID of the chat session to export
        output_dir: Directory to save the exported file
        format: Export format ('html' or 'json')

    Returns:
        Path to the exported file, or None if export failed
    """
    # Implementation here
    pass
```

## 🔧 Development Setup

### Initial Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/abacus-chat-exporter.git
cd abacus-chat-exporter

# Add upstream remote
git remote add upstream https://github.com/danindiana/abacus-chat-exporter.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -e .[dev]
```

### Keeping Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Update your main branch
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

### Git Sync Workflow

```mermaid
sequenceDiagram
    participant F as Your Fork
    participant L as Local Repo
    participant U as Upstream

    U->>L: git fetch upstream
    L->>L: git checkout main
    L->>L: git merge upstream/main
    L->>F: git push origin main
    L->>L: git checkout feature-branch
    L->>L: git rebase main
    L->>F: git push origin feature-branch
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_exporters.py
```

### Testing Workflow

```mermaid
flowchart TD
    A[Write Code] --> B[Write Tests]
    B --> C[Run Tests Locally]
    C --> D{Tests Pass?}
    D -->|No| E[Debug & Fix]
    E --> C
    D -->|Yes| F[Commit Changes]
    F --> G[Push to Remote]
    G --> H[CI Runs Tests]
    H --> I{CI Pass?}
    I -->|No| J[Check CI Logs]
    J --> E
    I -->|Yes| K[Ready for Review]
```

## 📊 Release Process

### Release Workflow

```mermaid
gitGraph
    commit id: "v1.0.0"
    branch develop
    checkout develop
    commit id: "Add feature A"
    commit id: "Add feature B"
    branch release/v1.1.0
    checkout release/v1.1.0
    commit id: "Update version"
    commit id: "Update changelog"
    checkout main
    merge release/v1.1.0 tag: "v1.1.0"
    checkout develop
    merge release/v1.1.0
```

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Example: `v1.2.3`
- 1 = Major version
- 2 = Minor version
- 3 = Patch version

## 🤝 Getting Help

### Communication Channels

```mermaid
flowchart TD
    A[Need Help?] --> B{Type of Issue}
    B -->|Bug| C[GitHub Issues]
    B -->|Feature Request| D[GitHub Discussions]
    B -->|Question| E[GitHub Discussions]
    B -->|Security| F[Security Policy]

    C --> G[Maintainer Reviews]
    D --> G
    E --> G
    F --> H[Private Disclosure]
```

- **Bugs**: Open a GitHub Issue
- **Feature Requests**: Start a GitHub Discussion
- **Questions**: GitHub Discussions or Issue comments
- **Security**: Follow responsible disclosure in SECURITY.md

## ✅ Checklist Before Submitting PR

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] Added tests for new features
- [ ] Updated documentation
- [ ] Commit messages follow guidelines
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] PR description is clear and complete

## 📚 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

Thank you for contributing! 🎉
