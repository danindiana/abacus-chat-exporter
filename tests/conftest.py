"""Pytest configuration and shared fixtures for abacus-chat-exporter tests"""

import os
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest

# Add the parent directory to the Python path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing"""
    return "test_api_key_1234567890abcdefghijklmnopqrstuvwxyz"


@pytest.fixture
def mock_env_vars(mock_api_key, monkeypatch):
    """Setup mock environment variables"""
    monkeypatch.setenv("ABACUS_API_KEY", mock_api_key)
    return {"ABACUS_API_KEY": mock_api_key}


@pytest.fixture
def mock_api_client():
    """Create a mock Abacus.AI API client with common methods"""
    client = MagicMock()

    # Mock common API methods
    client.list_chat_sessions = Mock(return_value=[])
    client.list_projects = Mock(return_value=[])
    client.list_deployments = Mock(return_value=[])
    client.list_deployment_conversations = Mock(return_value=[])
    client.list_agents = Mock(return_value=[])
    client.get_chat_session = Mock(return_value=None)
    client.describe_deployment_conversation = Mock(return_value=None)

    return client


@pytest.fixture
def mock_chat_session():
    """Create a mock chat session object"""
    session = MagicMock()
    session.chat_session_id = "chat_session_123"
    session.name = "Test Chat Session"
    session.created_at = "2024-01-01T00:00:00Z"
    session.chat_history = [
        MagicMock(role="user", text="Hello"),
        MagicMock(role="assistant", text="Hi there!")
    ]
    return session


@pytest.fixture
def mock_project():
    """Create a mock project object"""
    project = MagicMock()
    project.project_id = "project_123"
    project.name = "Test Project"
    project.use_case = "CHAT_LLM"
    project.created_at = "2024-01-01T00:00:00Z"
    return project


@pytest.fixture
def mock_deployment():
    """Create a mock deployment object"""
    deployment = MagicMock()
    deployment.deployment_id = "deployment_123"
    deployment.name = "Test Deployment"
    deployment.status = "ACTIVE"
    deployment.created_at = "2024-01-01T00:00:00Z"
    return deployment


@pytest.fixture
def mock_deployment_conversation():
    """Create a mock deployment conversation object"""
    conversation = MagicMock()
    conversation.deployment_conversation_id = "conv_123"
    conversation.name = "Test Conversation"
    conversation.external_session_id = "session_123"
    conversation.created_at = "2024-01-01T00:00:00Z"

    # Mock conversation history
    conversation.messages = [
        MagicMock(
            is_user_message=True,
            text="What is AI?",
            timestamp="2024-01-01T00:00:00Z"
        ),
        MagicMock(
            is_user_message=False,
            text="AI is artificial intelligence.",
            timestamp="2024-01-01T00:01:00Z"
        )
    ]

    return conversation


@pytest.fixture
def mock_agent():
    """Create a mock AI agent object"""
    agent = MagicMock()
    agent.agent_id = "agent_123"
    agent.name = "Test Agent"
    agent.agent_type = "CONVERSATIONAL"
    agent.created_at = "2024-01-01T00:00:00Z"
    return agent


@pytest.fixture
def mock_pdf_document():
    """Create a mock PDF document response"""
    doc = MagicMock()
    doc.document_id = "doc_123"
    doc.name = "test_document.pdf"
    doc.size = 1024000  # 1MB
    doc.status = "UPLOADED"
    return doc


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory for tests"""
    output_dir = tmp_path / "test_output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_chat_data():
    """Provide sample chat data for testing"""
    return {
        "chat_session_id": "chat_123",
        "messages": [
            {"role": "user", "content": "Hello", "timestamp": "2024-01-01T00:00:00Z"},
            {"role": "assistant", "content": "Hi!", "timestamp": "2024-01-01T00:01:00Z"}
        ],
        "metadata": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:01:00Z"
        }
    }


@pytest.fixture
def sample_filenames():
    """Provide sample filenames for sanitization testing"""
    return {
        "safe": "normal_filename.txt",
        "with_spaces": "filename with spaces.txt",
        "with_slashes": "path/to/filename.txt",
        "with_colons": "2024-01-01:filename.txt",
        "with_special_chars": "file@name#with$special%chars.txt",
        "very_long": "a" * 300 + ".txt",
        "unicode": "файл_名前_文件.txt",
        "empty": "",
        "path_traversal": "../../../etc/passwd",
        "windows_reserved": "CON.txt",
    }


@pytest.fixture(autouse=True)
def reset_env_vars(monkeypatch):
    """Reset environment variables after each test"""
    yield
    # Cleanup is automatic with monkeypatch


@pytest.fixture
def mock_pathlib_path(tmp_path):
    """Create a mock pathlib.Path for file operations"""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("test content")
    return test_file


@pytest.fixture
def capture_stdout(monkeypatch):
    """Capture stdout for testing print statements"""
    from io import StringIO
    captured_output = StringIO()

    class MockStdout:
        def write(self, text):
            captured_output.write(text)

        def flush(self):
            pass

    monkeypatch.setattr(sys, 'stdout', MockStdout())
    return captured_output


# Markers configuration
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual functions"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests for workflows"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take a long time"
    )
    config.addinivalue_line(
        "markers", "api: Tests that interact with APIs"
    )
    config.addinivalue_line(
        "markers", "requires_api_key: Tests requiring real API credentials"
    )
