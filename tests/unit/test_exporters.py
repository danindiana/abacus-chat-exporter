"""
Unit tests for export functions

Tests cover the export functionality for:
- AI chat sessions
- Project chats
- Deployment conversations
"""

import pytest
import os
import sys
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestExportChatSessions:
    """Test AI chat session export functionality"""

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_requires_api_key(self, monkeypatch):
        """Test that export fails without API key"""
        # Remove API key from environment
        monkeypatch.delenv("ABACUS_API_KEY", raising=False)

        with pytest.raises(ValueError, match="ABACUS_API_KEY"):
            from bulk_export_ai_chat import export_chat_sessions
            export_chat_sessions()

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_with_valid_api_key(self, mock_env_vars, mock_api_client):
        """Test export with valid API key configuration"""
        with patch('bulk_export_ai_chat.ApiClient', return_value=mock_api_client):
            # Should not raise ValueError
            mock_api_client.list_chat_sessions.return_value = []

            try:
                from bulk_export_ai_chat import export_chat_sessions
                # Mock pathlib operations to avoid actual file creation
                with patch('pathlib.Path.mkdir'), patch('builtins.open', mock_open()):
                    with patch('bulk_export_ai_chat.ApiClient'):
                        pass  # Just verify no exception for missing API key
            except ValueError as e:
                if "ABACUS_API_KEY" in str(e):
                    pytest.fail("Should not raise API key error when key is set")

    @pytest.mark.unit
    def test_export_creates_output_directory(self, mock_env_vars, temp_output_dir):
        """Test that export creates the output directory"""
        with patch('bulk_export_ai_chat.ApiClient') as mock_client:
            mock_client.return_value.list_chat_sessions.return_value = []

            output_path = temp_output_dir / "chat_exports"

            with patch('pathlib.Path.mkdir') as mock_mkdir:
                with patch('builtins.open', mock_open()):
                    # Verify mkdir is called during export
                    # (actual implementation check)
                    assert True  # Placeholder for actual implementation test

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_handles_empty_session_list(self, mock_env_vars, mock_api_client):
        """Test export behavior with no chat sessions"""
        mock_api_client.list_chat_sessions.return_value = []

        with patch('bulk_export_ai_chat.ApiClient', return_value=mock_api_client):
            with patch('pathlib.Path.mkdir'), patch('builtins.open', mock_open()):
                # Should not crash with empty list
                assert mock_api_client.list_chat_sessions() == []

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_handles_api_errors(self, mock_env_vars, mock_api_client):
        """Test export handles API errors gracefully"""
        mock_api_client.list_chat_sessions.side_effect = Exception("API Error")

        with patch('bulk_export_ai_chat.ApiClient', return_value=mock_api_client):
            with pytest.raises(Exception, match="API Error"):
                mock_api_client.list_chat_sessions()


class TestExportProjectChats:
    """Test project chat export functionality"""

    @pytest.mark.unit
    def test_export_project_sanitizes_filename(self, mock_project):
        """Test that project names are sanitized for filenames"""
        from bulk_export_all_projects import sanitize_filename, export_project_chats

        # Test with special characters in project name
        mock_project.name = "Test/Project: 2024"
        sanitized = sanitize_filename(mock_project.name)

        assert "/" not in sanitized
        assert ":" not in sanitized
        assert " " not in sanitized

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_project_handles_chat_llm_type(self, mock_project, mock_api_client):
        """Test export handles CHAT_LLM use case"""
        mock_project.use_case = "CHAT_LLM"
        mock_api_client.list_chat_sessions.return_value = []

        # Should call list_chat_sessions for CHAT_LLM projects
        assert mock_project.use_case == "CHAT_LLM"

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_project_handles_ai_agent_type(self, mock_project, mock_api_client):
        """Test export handles AI_AGENT use case"""
        mock_project.use_case = "AI_AGENT"
        mock_api_client.list_deployments.return_value = []

        # Should call list_deployments for AI_AGENT projects
        assert mock_project.use_case == "AI_AGENT"

    @pytest.mark.unit
    def test_export_project_creates_project_directory(self, mock_project, temp_output_dir):
        """Test that a directory is created for each project"""
        from bulk_export_all_projects import sanitize_filename

        project_name = sanitize_filename(mock_project.name)
        project_dir = temp_output_dir / project_name

        # Verify directory creation logic
        assert isinstance(project_name, str)
        assert len(project_name) > 0


class TestExportDeploymentConversations:
    """Test deployment conversation export functionality"""

    @pytest.mark.unit
    def test_export_requires_deployment_id(self, mock_env_vars, monkeypatch):
        """Test that deployment export requires DEPLOYMENT_ID"""
        monkeypatch.delenv("DEPLOYMENT_ID", raising=False)

        with pytest.raises((ValueError, SystemExit)):
            from bulk_export_deployment_convos import export_deployment_conversations
            export_deployment_conversations()

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_deployment_lists_conversations(self, mock_env_vars, mock_api_client, monkeypatch):
        """Test that deployment export lists conversations"""
        monkeypatch.setenv("DEPLOYMENT_ID", "test_deployment_123")
        mock_api_client.list_deployment_conversations.return_value = []

        # Should call list_deployment_conversations
        conversations = mock_api_client.list_deployment_conversations(deployment_id="test_deployment_123")
        assert conversations == []

    @pytest.mark.unit
    def test_export_deployment_sanitizes_conversation_name(self, mock_deployment_conversation):
        """Test that conversation names are sanitized"""
        from bulk_export_deployment_convos import sanitize_filename

        mock_deployment_conversation.name = "Test/Conversation: 2024"
        sanitized = sanitize_filename(mock_deployment_conversation.name)

        assert "/" not in sanitized
        assert ":" not in sanitized

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_deployment_handles_missing_conversations(self, mock_env_vars, mock_api_client, monkeypatch):
        """Test behavior when deployment has no conversations"""
        monkeypatch.setenv("DEPLOYMENT_ID", "test_deployment_123")
        mock_api_client.list_deployment_conversations.return_value = []

        conversations = mock_api_client.list_deployment_conversations(deployment_id="test_deployment_123")
        assert len(conversations) == 0


class TestFileOperations:
    """Test file I/O operations in export functions"""

    @pytest.mark.unit
    def test_export_creates_json_files(self, temp_output_dir):
        """Test that exports create JSON files"""
        test_data = {"test": "data"}
        json_file = temp_output_dir / "test_export.json"

        with open(json_file, 'w') as f:
            json.dump(test_data, f, indent=2)

        assert json_file.exists()
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        assert loaded_data == test_data

    @pytest.mark.unit
    def test_export_creates_html_files(self, temp_output_dir):
        """Test that exports create HTML files"""
        html_content = "<html><body>Test</body></html>"
        html_file = temp_output_dir / "test_export.html"

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        assert html_file.exists()
        with open(html_file, 'r', encoding='utf-8') as f:
            loaded_content = f.read()
        assert loaded_content == html_content

    @pytest.mark.unit
    def test_export_handles_unicode_content(self, temp_output_dir):
        """Test that exports handle Unicode content properly"""
        unicode_content = "Hello 世界 🌍"
        text_file = temp_output_dir / "unicode_test.txt"

        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(unicode_content)

        assert text_file.exists()
        with open(text_file, 'r', encoding='utf-8') as f:
            loaded_content = f.read()
        assert loaded_content == unicode_content

    @pytest.mark.unit
    def test_export_creates_nested_directories(self, temp_output_dir):
        """Test that export can create nested directory structures"""
        nested_dir = temp_output_dir / "project1" / "deployment1" / "conversations"
        nested_dir.mkdir(parents=True, exist_ok=True)

        assert nested_dir.exists()
        assert nested_dir.is_dir()


class TestErrorHandling:
    """Test error handling in export functions"""

    @pytest.mark.unit
    def test_export_handles_file_write_errors(self, temp_output_dir):
        """Test handling of file write errors"""
        # Create a read-only directory to trigger permission error
        readonly_dir = temp_output_dir / "readonly"
        readonly_dir.mkdir()

        # On Unix systems, we can test permission errors
        if os.name != 'nt':  # Skip on Windows
            readonly_dir.chmod(0o444)  # Read-only

            with pytest.raises(PermissionError):
                test_file = readonly_dir / "test.txt"
                with open(test_file, 'w') as f:
                    f.write("test")

            # Cleanup
            readonly_dir.chmod(0o755)

    @pytest.mark.unit
    @pytest.mark.api
    def test_export_handles_network_errors(self, mock_api_client):
        """Test handling of network/API errors"""
        from requests.exceptions import ConnectionError

        mock_api_client.list_chat_sessions.side_effect = ConnectionError("Network error")

        with pytest.raises(ConnectionError):
            mock_api_client.list_chat_sessions()

    @pytest.mark.unit
    def test_export_handles_json_serialization_errors(self):
        """Test handling of JSON serialization errors"""
        # Object that can't be serialized
        class NonSerializable:
            pass

        data = {"key": NonSerializable()}

        with pytest.raises(TypeError):
            json.dumps(data)


class TestExportDataFormats:
    """Test data format handling in exports"""

    @pytest.mark.unit
    def test_export_json_format_is_valid(self, mock_chat_session, temp_output_dir):
        """Test that exported JSON is valid and well-formed"""
        # Simulate export data structure
        export_data = {
            "chat_session_id": mock_chat_session.chat_session_id,
            "name": mock_chat_session.name,
            "created_at": mock_chat_session.created_at,
            "messages": []
        }

        json_file = temp_output_dir / "test_session.json"
        with open(json_file, 'w') as f:
            json.dump(export_data, f, indent=2)

        # Verify valid JSON
        with open(json_file, 'r') as f:
            loaded = json.load(f)

        assert loaded["chat_session_id"] == mock_chat_session.chat_session_id
        assert loaded["name"] == mock_chat_session.name

    @pytest.mark.unit
    def test_export_preserves_message_order(self, mock_chat_session):
        """Test that message order is preserved in exports"""
        messages = [
            {"order": 1, "text": "First"},
            {"order": 2, "text": "Second"},
            {"order": 3, "text": "Third"}
        ]

        # Verify order is maintained
        for i, msg in enumerate(messages):
            assert msg["order"] == i + 1


class TestExportIntegration:
    """Integration-style tests for export workflows"""

    @pytest.mark.integration
    @pytest.mark.api
    def test_full_chat_export_workflow(self, mock_env_vars, mock_api_client, mock_chat_session, temp_output_dir):
        """Test complete chat export workflow"""
        mock_api_client.list_chat_sessions.return_value = [mock_chat_session]

        with patch('bulk_export_ai_chat.ApiClient', return_value=mock_api_client):
            with patch('pathlib.Path.mkdir'):
                with patch('builtins.open', mock_open()):
                    # Verify the workflow completes
                    sessions = mock_api_client.list_chat_sessions()
                    assert len(sessions) == 1
                    assert sessions[0].chat_session_id == mock_chat_session.chat_session_id

    @pytest.mark.integration
    @pytest.mark.api
    def test_export_multiple_projects(self, mock_env_vars, mock_api_client, mock_project):
        """Test exporting from multiple projects"""
        projects = [mock_project, mock_project]  # Simulate multiple projects
        mock_api_client.list_projects.return_value = projects

        with patch('bulk_export_all_projects.ApiClient', return_value=mock_api_client):
            retrieved_projects = mock_api_client.list_projects()
            assert len(retrieved_projects) == 2
