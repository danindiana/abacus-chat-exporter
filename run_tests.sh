#!/bin/bash
# Test runner script for abacus-chat-exporter
# Provides convenient shortcuts for common testing tasks

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Abacus Chat Exporter - Test Runner   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo "   Activating: source venv/bin/activate"
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        echo -e "${RED}❌ Virtual environment not found. Run: python3 -m venv venv${NC}"
        exit 1
    fi
fi

# Check if test dependencies are installed
if ! python -c "import pytest" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Test dependencies not installed${NC}"
    echo "   Installing: pip install -r requirements-test.txt"
    pip install -q -r requirements-test.txt
fi

# Parse command line arguments
COMMAND=${1:-help}

case "$COMMAND" in
    all)
        echo -e "${GREEN}🧪 Running all tests...${NC}"
        pytest -v
        ;;

    unit)
        echo -e "${GREEN}🧪 Running unit tests only...${NC}"
        pytest -v -m unit
        ;;

    integration)
        echo -e "${GREEN}🧪 Running integration tests...${NC}"
        pytest -v -m integration
        ;;

    fast)
        echo -e "${GREEN}⚡ Running fast tests (unit, not slow)...${NC}"
        pytest -v -m "unit and not slow" --tb=short
        ;;

    coverage)
        echo -e "${GREEN}📊 Running tests with coverage report...${NC}"
        pytest --cov=. --cov-report=html --cov-report=term-missing
        echo ""
        echo -e "${BLUE}📁 Coverage report: htmlcov/index.html${NC}"
        ;;

    watch)
        echo -e "${GREEN}👀 Running tests in watch mode...${NC}"
        echo -e "${YELLOW}   (tests will re-run when files change)${NC}"
        pytest-watch
        ;;

    sanitizers)
        echo -e "${GREEN}🧪 Running sanitizer tests...${NC}"
        pytest -v tests/unit/test_sanitizers.py
        ;;

    exporters)
        echo -e "${GREEN}🧪 Running exporter tests...${NC}"
        pytest -v tests/unit/test_exporters.py
        ;;

    pdf)
        echo -e "${GREEN}🧪 Running PDF processor tests...${NC}"
        pytest -v tests/unit/test_pdf_processor.py
        ;;

    workflows)
        echo -e "${GREEN}🧪 Running workflow integration tests...${NC}"
        pytest -v tests/integration/test_workflows.py
        ;;

    failed)
        echo -e "${GREEN}🔄 Re-running only failed tests...${NC}"
        pytest --lf -v
        ;;

    verbose)
        echo -e "${GREEN}🧪 Running tests with maximum verbosity...${NC}"
        pytest -vv --tb=long
        ;;

    debug)
        echo -e "${GREEN}🐛 Running tests with debugging output...${NC}"
        pytest -vv --tb=long --capture=no
        ;;

    parallel)
        echo -e "${GREEN}⚡ Running tests in parallel...${NC}"
        pytest -n auto -v
        ;;

    quality)
        echo -e "${GREEN}🔍 Running code quality checks...${NC}"
        echo ""
        echo -e "${BLUE}→ Black (formatting)${NC}"
        black --check --diff .
        echo ""
        echo -e "${BLUE}→ isort (import sorting)${NC}"
        isort --check-only --diff .
        echo ""
        echo -e "${BLUE}→ flake8 (linting)${NC}"
        flake8 . --count --statistics
        echo ""
        echo -e "${GREEN}✅ All quality checks passed!${NC}"
        ;;

    fix)
        echo -e "${GREEN}🔧 Auto-fixing code style issues...${NC}"
        echo ""
        echo -e "${BLUE}→ Running black...${NC}"
        black .
        echo ""
        echo -e "${BLUE}→ Running isort...${NC}"
        isort .
        echo ""
        echo -e "${GREEN}✅ Code formatted!${NC}"
        ;;

    clean)
        echo -e "${YELLOW}🧹 Cleaning test artifacts...${NC}"
        rm -rf .pytest_cache/ htmlcov/ .coverage coverage.xml
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete
        echo -e "${GREEN}✅ Clean complete!${NC}"
        ;;

    install)
        echo -e "${GREEN}📦 Installing all dependencies...${NC}"
        pip install -r requirements.txt
        pip install -r requirements-test.txt
        echo ""
        echo -e "${GREEN}✅ Dependencies installed!${NC}"
        ;;

    hooks)
        echo -e "${GREEN}🪝 Installing pre-commit hooks...${NC}"
        pip install pre-commit
        pre-commit install
        echo ""
        echo -e "${GREEN}✅ Pre-commit hooks installed!${NC}"
        echo -e "${BLUE}   Run: pre-commit run --all-files${NC}"
        ;;

    ci)
        echo -e "${GREEN}🚀 Running CI/CD checks locally...${NC}"
        echo ""
        echo -e "${BLUE}→ Step 1: Syntax check${NC}"
        python -m py_compile *.py
        echo ""
        echo -e "${BLUE}→ Step 2: Code quality${NC}"
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        echo ""
        echo -e "${BLUE}→ Step 3: Unit tests${NC}"
        pytest -v -m unit --tb=short
        echo ""
        echo -e "${BLUE}→ Step 4: Integration tests${NC}"
        pytest -v -m integration --tb=short
        echo ""
        echo -e "${BLUE}→ Step 5: Coverage check${NC}"
        pytest --cov=. --cov-fail-under=80 --cov-report=term-missing
        echo ""
        echo -e "${GREEN}✅ All CI checks passed!${NC}"
        ;;

    report)
        echo -e "${GREEN}📊 Generating test report...${NC}"
        pytest --html=test_report.html --self-contained-html
        echo ""
        echo -e "${BLUE}📁 Report: test_report.html${NC}"
        ;;

    help|*)
        echo -e "${BLUE}Usage: ./run_tests.sh [command]${NC}"
        echo ""
        echo -e "${GREEN}Test Commands:${NC}"
        echo "  all           - Run all tests"
        echo "  unit          - Run unit tests only"
        echo "  integration   - Run integration tests"
        echo "  fast          - Run fast tests (unit, not slow)"
        echo "  coverage      - Run tests with coverage report"
        echo "  watch         - Run tests in watch mode (auto-rerun on changes)"
        echo ""
        echo -e "${GREEN}Specific Test Suites:${NC}"
        echo "  sanitizers    - Run sanitizer tests"
        echo "  exporters     - Run exporter tests"
        echo "  pdf           - Run PDF processor tests"
        echo "  workflows     - Run workflow integration tests"
        echo ""
        echo -e "${GREEN}Test Control:${NC}"
        echo "  failed        - Re-run only failed tests"
        echo "  verbose       - Run with maximum verbosity"
        echo "  debug         - Run with debugging output"
        echo "  parallel      - Run tests in parallel (faster)"
        echo ""
        echo -e "${GREEN}Code Quality:${NC}"
        echo "  quality       - Run all code quality checks"
        echo "  fix           - Auto-fix code style issues"
        echo ""
        echo -e "${GREEN}Utilities:${NC}"
        echo "  clean         - Clean test artifacts and cache"
        echo "  install       - Install all dependencies"
        echo "  hooks         - Install pre-commit hooks"
        echo "  ci            - Run full CI/CD checks locally"
        echo "  report        - Generate HTML test report"
        echo ""
        echo -e "${GREEN}Examples:${NC}"
        echo "  ./run_tests.sh fast       # Quick test run"
        echo "  ./run_tests.sh coverage   # Full coverage report"
        echo "  ./run_tests.sh ci         # Simulate CI/CD pipeline"
        ;;
esac

# Exit with test exit code
exit $?
