## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

Please check the relevant option(s):

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🔧 Configuration change
- [ ] ♻️ Code refactoring
- [ ] ✅ Test addition/modification
- [ ] 🎨 Style/formatting change

## Related Issues

<!-- Link any related issues using keywords like "Fixes #123" or "Closes #456" -->

Fixes #
Related to #

## Changes Made

<!-- List the main changes made in this PR -->

-
-
-

## Testing

### Test Coverage

- [ ] Tests added for new functionality
- [ ] All existing tests pass
- [ ] Coverage maintained or improved (80%+ required)
- [ ] Integration tests added (if applicable)

### How Has This Been Tested?

<!-- Describe the tests you ran to verify your changes -->

```bash
# Example commands run
./run_tests.sh fast
./run_tests.sh coverage
```

**Test Configuration**:
- OS: <!-- e.g., Ubuntu 22.04, macOS 13, Windows 11 -->
- Python version: <!-- e.g., 3.11.5 -->
- Virtual environment: <!-- yes/no -->

## Code Quality

- [ ] Code follows project style guidelines (Black, isort)
- [ ] Pre-commit hooks pass (`pre-commit run --all-files`)
- [ ] No new linting warnings (`flake8 .`)
- [ ] Type hints added where appropriate
- [ ] Security scan passes (`bandit -r .`)
- [ ] No secrets committed (`detect-secrets scan`)

## Documentation

- [ ] Code comments added for complex logic
- [ ] Docstrings updated/added for public functions
- [ ] README.md updated (if needed)
- [ ] TESTING.md updated (if test changes)
- [ ] DEVELOPMENT.md updated (if dev process changes)
- [ ] Inline documentation added

## Screenshots (if applicable)

<!-- Add screenshots to help explain your changes -->

## Checklist

### Before Creating PR

- [ ] Rebased on latest `main` branch
- [ ] Ran `./run_tests.sh ci` locally (all checks pass)
- [ ] Reviewed own code changes
- [ ] Removed debug code and console logs
- [ ] Updated version numbers (if applicable)

### PR Quality

- [ ] Title follows conventional commits format (e.g., `feat:`, `fix:`, `docs:`)
- [ ] Description is clear and complete
- [ ] Linked related issues
- [ ] Requested reviews from appropriate team members
- [ ] Added labels (bug, enhancement, documentation, etc.)

## Breaking Changes

<!-- If this PR introduces breaking changes, describe them here and provide migration guide -->

**Does this PR introduce breaking changes?** <!-- Yes/No -->

If yes, describe:
- What breaks:
- Why it's necessary:
- Migration path:

## Performance Impact

<!-- Describe any performance implications of your changes -->

- [ ] No significant performance impact
- [ ] Performance improved
- [ ] Performance degraded (with justification):

## Security Considerations

<!-- Describe any security implications of your changes -->

- [ ] No security implications
- [ ] Security improved
- [ ] Potential security concerns (describe):

## Deployment Notes

<!-- Any special deployment considerations? -->

- [ ] No special deployment steps needed
- [ ] Environment variables added/changed (document below)
- [ ] Database migrations required
- [ ] Configuration changes required

## Additional Context

<!-- Add any other context about the PR here -->

## Reviewer Notes

<!-- Specific areas you'd like reviewers to focus on -->

Please pay special attention to:
-
-

---

## For Maintainers

### Merge Checklist

- [ ] All CI checks passing
- [ ] At least one approval
- [ ] No merge conflicts
- [ ] Version bumped (if applicable)
- [ ] Changelog updated (if applicable)
- [ ] Documentation deployed (if applicable)

### Post-Merge Tasks

- [ ] Deploy to staging (if applicable)
- [ ] Monitor for issues
- [ ] Update project board
- [ ] Close related issues
