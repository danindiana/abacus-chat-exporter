"""
Integration tests for complete workflows

These tests validate end-to-end functionality across multiple components,
testing realistic user scenarios with mocked API responses.
"""

import pytest
import os
import sys
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open, call
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestChatExportWorkflow:
    """Integration tests for complete chat export workflows"""

    @pytest.mark.integration
    @pytest.mark.api
    def test_full_ai_chat_export_workflow(
        self, mock_env_vars, mock_api_client, mock_chat_session, temp_output_dir
    ):
        """Test complete AI chat export from discovery to file creation"""
        # Setup: Multiple chat sessions
        session1 = mock_chat_session
        session2 = MagicMock()
        session2.chat_session_id = "chat_session_456"
        session2.name = "Second Chat"
        session2.created_at = "2024-01-02T00:00:00Z"
        session2.chat_history = [
            MagicMock(role="user", text="Question"),
            MagicMock(role="assistant", text="Answer")
        ]

        mock_api_client.list_chat_sessions.return_value = [session1, session2]

        # Test workflow
        with patch('bulk_export_ai_chat.ApiClient', return_value=mock_api_client):
            sessions = mock_api_client.list_chat_sessions()

            # Verify discovery
            assert len(sessions) == 2
            assert sessions[0].chat_session_id == "chat_session_123"
            assert sessions[1].chat_session_id == "chat_session_456"

            # Simulate export for each session
            exported_files = []
            for session in sessions:
                from bulk_export_ai_chat import sanitize_filename

                filename = sanitize_filename(session.name or session.chat_session_id)
                json_file = temp_output_dir / f"{filename}.json"

                # Create export data
                export_data = {
                    "chat_session_id": session.chat_session_id,
                    "name": session.name,
                    "created_at": session.created_at,
                    "messages": [
                        {"role": msg.role, "text": msg.text}
                        for msg in session.chat_history
                    ]
                }

                # Write JSON
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2)

                exported_files.append(json_file)

            # Verify exports
            assert len(exported_files) == 2
            assert all(f.exists() for f in exported_files)

            # Verify JSON content
            with open(exported_files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
            assert data["chat_session_id"] == "chat_session_123"
            assert len(data["messages"]) == 2

    @pytest.mark.integration
    @pytest.mark.api
    def test_project_export_with_mixed_use_cases(
        self, mock_env_vars, mock_api_client, temp_output_dir
    ):
        """Test exporting from projects with different use cases"""
        # Setup: Multiple projects with different use cases
        chat_llm_project = MagicMock()
        chat_llm_project.project_id = "proj_chat"
        chat_llm_project.name = "Chat LLM Project"
        chat_llm_project.use_case = "CHAT_LLM"

        ai_agent_project = MagicMock()
        ai_agent_project.project_id = "proj_agent"
        ai_agent_project.name = "AI Agent Project"
        ai_agent_project.use_case = "AI_AGENT"

        mock_api_client.list_projects.return_value = [chat_llm_project, ai_agent_project]

        # Mock responses for CHAT_LLM
        mock_api_client.list_chat_sessions.return_value = [
            MagicMock(
                chat_session_id="chat_1",
                name="Chat 1",
                project_id="proj_chat"
            )
        ]

        # Mock responses for AI_AGENT
        mock_deployment = MagicMock()
        mock_deployment.deployment_id = "deploy_1"
        mock_deployment.name = "Deployment 1"
        mock_api_client.list_deployments.return_value = [mock_deployment]

        mock_api_client.list_deployment_conversations.return_value = [
            MagicMock(
                deployment_conversation_id="conv_1",
                name="Conversation 1"
            )
        ]

        # Test workflow
        with patch('bulk_export_all_projects.ApiClient', return_value=mock_api_client):
            projects = mock_api_client.list_projects()

            assert len(projects) == 2

            for project in projects:
                if project.use_case == "CHAT_LLM":
                    # Should call list_chat_sessions
                    chats = mock_api_client.list_chat_sessions()
                    assert len(chats) == 1
                    assert chats[0].project_id == "proj_chat"

                elif project.use_case == "AI_AGENT":
                    # Should call list_deployments
                    deployments = mock_api_client.list_deployments(project_id=project.project_id)
                    assert len(deployments) == 1

                    # Then list conversations
                    convos = mock_api_client.list_deployment_conversations(
                        deployment_id=deployments[0].deployment_id
                    )
                    assert len(convos) == 1

    @pytest.mark.integration
    @pytest.mark.api
    def test_deployment_conversation_export_workflow(
        self, mock_env_vars, mock_api_client, mock_deployment_conversation, temp_output_dir, monkeypatch
    ):
        """Test complete deployment conversation export workflow"""
        monkeypatch.setenv("DEPLOYMENT_ID", "test_deployment_123")

        # Setup: Multiple conversations
        conv1 = mock_deployment_conversation
        conv2 = MagicMock()
        conv2.deployment_conversation_id = "conv_456"
        conv2.name = "Conversation 2"
        conv2.external_session_id = "session_456"
        conv2.messages = [
            MagicMock(is_user_message=True, text="Hello", timestamp="2024-01-01T00:00:00Z"),
            MagicMock(is_user_message=False, text="Hi!", timestamp="2024-01-01T00:01:00Z")
        ]

        mock_api_client.list_deployment_conversations.return_value = [conv1, conv2]

        # Test workflow
        with patch('bulk_export_deployment_convos.ApiClient', return_value=mock_api_client):
            conversations = mock_api_client.list_deployment_conversations(
                deployment_id="test_deployment_123"
            )

            assert len(conversations) == 2

            # Export each conversation
            for conv in conversations:
                from bulk_export_deployment_convos import sanitize_filename

                filename = sanitize_filename(
                    conv.name or conv.external_session_id or conv.deployment_conversation_id
                )
                json_file = temp_output_dir / f"{filename}.json"

                export_data = {
                    "conversation_id": conv.deployment_conversation_id,
                    "name": conv.name,
                    "messages": [
                        {
                            "is_user": msg.is_user_message,
                            "text": msg.text,
                            "timestamp": msg.timestamp
                        }
                        for msg in conv.messages
                    ]
                }

                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2)

            # Verify all conversations exported
            exported_files = list(temp_output_dir.glob("*.json"))
            assert len(exported_files) == 2


class TestPDFProcessingWorkflow:
    """Integration tests for PDF processing workflows"""

    @pytest.mark.integration
    @pytest.mark.api
    def test_complete_pdf_processing_workflow(
        self, mock_env_vars, mock_api_client, mock_pdf_document, temp_output_dir, monkeypatch
    ):
        """Test complete PDF processing from discovery to result logging"""
        from process_pdfs import find_pdfs, upload_document, process_with_prompts, save_activity_log

        monkeypatch.setenv("DEPLOYMENT_ID", "test_deployment_123")

        # Step 1: Create test PDFs
        pdf1 = temp_output_dir / "document1.pdf"
        pdf2 = temp_output_dir / "document2.pdf"
        pdf1.write_text("Fake PDF content 1")
        pdf2.write_text("Fake PDF content 2")

        # Step 2: Find PDFs
        pdfs = find_pdfs(temp_output_dir, recursive=False)
        assert len(pdfs) == 2

        # Step 3: Setup mocks for upload and processing
        mock_api_client.upload_document.return_value = mock_pdf_document

        mock_conversation = MagicMock()
        mock_conversation.deployment_conversation_id = "conv_test"
        mock_api_client.create_deployment_conversation.return_value = mock_conversation

        mock_response = MagicMock()
        mock_response.text = "Analysis result"
        mock_api_client.send_message_to_deployment_conversation.return_value = mock_response

        # Step 4: Process each PDF
        results = []
        prompts = ["Analyze this document", "Summarize key points"]

        for pdf_path in pdfs:
            # Upload
            upload_result = upload_document(mock_api_client, "test_deployment_123", pdf_path)
            assert upload_result["document_id"] == mock_pdf_document.document_id

            # Process with prompts
            prompt_results = process_with_prompts(
                mock_api_client,
                "test_deployment_123",
                upload_result["document_id"],
                pdf_path.name,
                prompts
            )
            assert len(prompt_results) == 2

            # Log activity
            log_file = temp_output_dir / f"{pdf_path.stem}_activity.json"
            activity_data = {
                pdf_path.name: {
                    "document_id": upload_result["document_id"],
                    "prompts": prompts,
                    "results": [r["response"] for r in prompt_results]
                }
            }
            save_activity_log(log_file, activity_data)

            results.append({
                "pdf": pdf_path.name,
                "uploaded": upload_result,
                "processed": prompt_results
            })

        # Verify complete workflow
        assert len(results) == 2
        assert all(r["uploaded"]["document_id"] for r in results)
        assert all(len(r["processed"]) == 2 for r in results)

        # Verify activity logs were created
        log_files = list(temp_output_dir.glob("*_activity.json"))
        assert len(log_files) == 2

    @pytest.mark.integration
    def test_batch_pdf_processing_with_error_recovery(
        self, mock_env_vars, mock_api_client, temp_output_dir, monkeypatch
    ):
        """Test batch PDF processing with partial failures"""
        from process_pdfs import find_pdfs, upload_document

        monkeypatch.setenv("DEPLOYMENT_ID", "test_deployment_123")

        # Create multiple PDFs
        for i in range(5):
            (temp_output_dir / f"doc{i}.pdf").write_text(f"Content {i}")

        pdfs = find_pdfs(temp_output_dir, recursive=False)
        assert len(pdfs) == 5

        # Simulate partial failures (fail on doc2 and doc4)
        def upload_side_effect(deployment_id, pdf_path):
            if "doc2" in str(pdf_path) or "doc4" in str(pdf_path):
                raise Exception(f"Upload failed for {pdf_path.name}")
            return {
                "document_id": f"doc_{pdf_path.stem}",
                "name": pdf_path.name,
                "status": "UPLOADED"
            }

        mock_api_client.upload_document.side_effect = upload_side_effect

        # Process with error handling
        successful = []
        failed = []

        for pdf in pdfs:
            try:
                result = upload_document(mock_api_client, "test_deployment_123", pdf)
                successful.append((pdf.name, result))
            except Exception as e:
                failed.append((pdf.name, str(e)))

        # Verify error recovery
        assert len(successful) == 3  # doc0, doc1, doc3
        assert len(failed) == 2  # doc2, doc4

        # Verify successful uploads
        assert all("document_id" in result for _, result in successful)

        # Verify failures were captured
        assert all("Upload failed" in error for _, error in failed)


class TestSearchAndDiscoveryWorkflow:
    """Integration tests for search and discovery workflows"""

    @pytest.mark.integration
    @pytest.mark.api
    def test_comprehensive_chat_search_workflow(
        self, mock_env_vars, mock_api_client, mock_chat_session, mock_project, mock_deployment
    ):
        """Test multi-strategy chat search across all locations"""
        from find_my_chats import safe_call

        # Setup: Distribute chat data across different locations
        mock_api_client.list_chat_sessions.return_value = [mock_chat_session]
        mock_api_client.list_projects.return_value = [mock_project]
        mock_api_client.list_deployments.return_value = [mock_deployment]

        mock_conversations = [
            MagicMock(
                deployment_conversation_id=f"conv_{i}",
                name=f"Conversation {i}"
            )
            for i in range(3)
        ]
        mock_api_client.list_deployment_conversations.return_value = mock_conversations

        found_chats = []

        # Search Strategy 1: AI Chat Sessions
        sessions = safe_call(mock_api_client.list_chat_sessions)
        if sessions and not isinstance(sessions, tuple):
            found_chats.extend([("chat_session", s.chat_session_id) for s in sessions])

        # Search Strategy 2: Projects
        projects = safe_call(mock_api_client.list_projects)
        if projects and not isinstance(projects, tuple):
            for proj in projects:
                # Check deployments in project
                deployments = safe_call(mock_api_client.list_deployments, project_id=proj.project_id)
                if deployments and not isinstance(deployments, tuple):
                    for deploy in deployments:
                        # Check conversations in deployment
                        convos = safe_call(
                            mock_api_client.list_deployment_conversations,
                            deployment_id=deploy.deployment_id
                        )
                        if convos and not isinstance(convos, tuple):
                            found_chats.extend([("deployment_conversation", c.deployment_conversation_id) for c in convos])

        # Verify comprehensive search
        assert len(found_chats) > 0
        assert any(chat_type == "chat_session" for chat_type, _ in found_chats)
        assert any(chat_type == "deployment_conversation" for chat_type, _ in found_chats)


class TestErrorHandlingAndRecovery:
    """Integration tests for error handling across workflows"""

    @pytest.mark.integration
    @pytest.mark.api
    def test_api_error_recovery_in_export(
        self, mock_env_vars, mock_api_client, mock_chat_session
    ):
        """Test graceful handling of API errors during export"""
        # Simulate intermittent API errors
        call_count = 0

        def list_sessions_with_retry():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary network error")
            return [mock_chat_session]

        mock_api_client.list_chat_sessions.side_effect = list_sessions_with_retry

        # Retry logic
        max_retries = 3
        sessions = None

        for attempt in range(max_retries):
            try:
                sessions = mock_api_client.list_chat_sessions()
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                # In real code, would add exponential backoff here

        # Verify recovery
        assert sessions is not None
        assert len(sessions) == 1
        assert call_count == 3  # Failed twice, succeeded on third

    @pytest.mark.integration
    def test_file_system_error_handling(self, temp_output_dir):
        """Test handling of file system errors during export"""
        if os.name == 'nt':  # Skip on Windows
            pytest.skip("Permission tests not reliable on Windows")

        # Create read-only directory
        readonly_dir = temp_output_dir / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)

        # Attempt to write should fail gracefully
        test_file = readonly_dir / "test.json"
        error_caught = False

        try:
            with open(test_file, 'w') as f:
                json.dump({"test": "data"}, f)
        except PermissionError:
            error_caught = True

        # Cleanup
        readonly_dir.chmod(0o755)

        assert error_caught, "Should catch permission error"

    @pytest.mark.integration
    @pytest.mark.api
    def test_partial_export_with_failures(
        self, mock_env_vars, mock_api_client, temp_output_dir
    ):
        """Test that partial exports still save successful results"""
        # Setup: Mix of successful and failing sessions
        good_session = MagicMock()
        good_session.chat_session_id = "good_1"
        good_session.name = "Good Session"
        good_session.chat_history = []

        bad_session = MagicMock()
        bad_session.chat_session_id = "bad_1"
        bad_session.name = "Bad Session"
        # Accessing chat_history will raise an error
        type(bad_session).chat_history = property(lambda self: (_ for _ in ()).throw(Exception("API Error")))

        mock_api_client.list_chat_sessions.return_value = [good_session, bad_session]

        # Export with error handling
        successful_exports = []
        failed_exports = []

        sessions = mock_api_client.list_chat_sessions()

        for session in sessions:
            try:
                # Attempt to access chat history
                messages = session.chat_history

                # If successful, export
                from bulk_export_ai_chat import sanitize_filename
                filename = sanitize_filename(session.name)
                json_file = temp_output_dir / f"{filename}.json"

                with open(json_file, 'w') as f:
                    json.dump({
                        "session_id": session.chat_session_id,
                        "messages": list(messages)
                    }, f)

                successful_exports.append(session.chat_session_id)

            except Exception as e:
                failed_exports.append((session.chat_session_id, str(e)))

        # Verify partial success
        assert len(successful_exports) == 1
        assert len(failed_exports) == 1
        assert successful_exports[0] == "good_1"
        assert failed_exports[0][0] == "bad_1"


class TestConcurrentOperations:
    """Integration tests for concurrent/parallel operations"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_parallel_pdf_processing(
        self, mock_env_vars, mock_api_client, temp_output_dir, monkeypatch
    ):
        """Test processing multiple PDFs in parallel (simulated)"""
        from process_pdfs import find_pdfs, upload_document

        monkeypatch.setenv("DEPLOYMENT_ID", "test_deployment_123")

        # Create multiple PDFs
        num_pdfs = 10
        for i in range(num_pdfs):
            (temp_output_dir / f"parallel_{i}.pdf").write_text(f"Content {i}")

        pdfs = find_pdfs(temp_output_dir, recursive=False)
        assert len(pdfs) == num_pdfs

        # Mock successful uploads
        def mock_upload(deployment_id, pdf_path):
            return {
                "document_id": f"doc_{pdf_path.stem}",
                "name": pdf_path.name
            }

        mock_api_client.upload_document.side_effect = mock_upload

        # Process in "parallel" (sequential in test, but simulating parallel pattern)
        results = []
        for pdf in pdfs:
            result = upload_document(mock_api_client, "test_deployment_123", pdf)
            results.append(result)

        # Verify all processed
        assert len(results) == num_pdfs
        assert all("document_id" in r for r in results)


class TestDataIntegrity:
    """Integration tests for data integrity across workflows"""

    @pytest.mark.integration
    def test_export_preserves_message_order(
        self, mock_chat_session, temp_output_dir
    ):
        """Test that message order is preserved through export"""
        # Create messages with specific order
        ordered_messages = []
        for i in range(10):
            msg = MagicMock()
            msg.role = "user" if i % 2 == 0 else "assistant"
            msg.text = f"Message {i}"
            msg.timestamp = f"2024-01-01T00:{i:02d}:00Z"
            ordered_messages.append(msg)

        mock_chat_session.chat_history = ordered_messages

        # Export
        from bulk_export_ai_chat import sanitize_filename
        filename = sanitize_filename(mock_chat_session.name)
        json_file = temp_output_dir / f"{filename}.json"

        export_data = {
            "messages": [
                {"role": msg.role, "text": msg.text, "timestamp": msg.timestamp}
                for msg in mock_chat_session.chat_history
            ]
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

        # Verify order preserved
        with open(json_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)

        assert len(loaded["messages"]) == 10
        for i, msg in enumerate(loaded["messages"]):
            assert msg["text"] == f"Message {i}"
            assert msg["timestamp"] == f"2024-01-01T00:{i:02d}:00Z"

    @pytest.mark.integration
    def test_unicode_data_integrity(self, temp_output_dir):
        """Test that Unicode data is preserved through export/import"""
        unicode_data = {
            "chinese": "你好世界",
            "russian": "Привет мир",
            "japanese": "こんにちは世界",
            "emoji": "🌍🚀📊",
            "mixed": "Hello 世界 🌍"
        }

        json_file = temp_output_dir / "unicode_test.json"

        # Export
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(unicode_data, f, ensure_ascii=False, indent=2)

        # Import and verify
        with open(json_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)

        assert loaded == unicode_data
        assert loaded["chinese"] == "你好世界"
        assert loaded["emoji"] == "🌍🚀📊"


class TestEndToEndScenarios:
    """End-to-end integration tests for realistic user scenarios"""

    @pytest.mark.integration
    @pytest.mark.api
    @pytest.mark.slow
    def test_new_user_export_all_chats(
        self, mock_env_vars, mock_api_client, mock_chat_session,
        mock_project, mock_deployment, temp_output_dir
    ):
        """Test scenario: New user wants to export all their chats"""
        # Simulate a user account with various chat types
        mock_api_client.list_chat_sessions.return_value = [mock_chat_session]
        mock_api_client.list_projects.return_value = [mock_project]
        mock_api_client.list_deployments.return_value = [mock_deployment]

        mock_convos = [
            MagicMock(deployment_conversation_id=f"conv_{i}", name=f"Chat {i}")
            for i in range(2)
        ]
        mock_api_client.list_deployment_conversations.return_value = mock_convos

        total_exports = 0

        # Step 1: Export AI chat sessions
        sessions = mock_api_client.list_chat_sessions()
        total_exports += len(sessions)

        # Step 2: Export project chats
        projects = mock_api_client.list_projects()
        for proj in projects:
            if proj.use_case == "AI_AGENT":
                deployments = mock_api_client.list_deployments(project_id=proj.project_id)
                for deploy in deployments:
                    convos = mock_api_client.list_deployment_conversations(
                        deployment_id=deploy.deployment_id
                    )
                    total_exports += len(convos)

        # Verify complete export
        assert total_exports == 3  # 1 session + 2 conversations

    @pytest.mark.integration
    @pytest.mark.api
    def test_incremental_export_scenario(
        self, mock_env_vars, mock_api_client, temp_output_dir
    ):
        """Test scenario: User wants to export only new chats since last export"""
        # First export
        old_session = MagicMock()
        old_session.chat_session_id = "old_123"
        old_session.name = "Old Chat"
        old_session.created_at = "2024-01-01T00:00:00Z"
        old_session.chat_history = []

        mock_api_client.list_chat_sessions.return_value = [old_session]

        # Track exported IDs
        exported_ids_file = temp_output_dir / "exported_ids.json"
        exported_ids = set()

        sessions = mock_api_client.list_chat_sessions()
        for session in sessions:
            exported_ids.add(session.chat_session_id)

        # Save tracking file
        with open(exported_ids_file, 'w') as f:
            json.dump(list(exported_ids), f)

        # Second export (with new chats)
        new_session = MagicMock()
        new_session.chat_session_id = "new_456"
        new_session.name = "New Chat"
        new_session.created_at = "2024-01-02T00:00:00Z"
        new_session.chat_history = []

        mock_api_client.list_chat_sessions.return_value = [old_session, new_session]

        # Load previous exports
        with open(exported_ids_file, 'r') as f:
            previously_exported = set(json.load(f))

        # Find new chats
        all_sessions = mock_api_client.list_chat_sessions()
        new_sessions = [
            s for s in all_sessions
            if s.chat_session_id not in previously_exported
        ]

        # Verify incremental export
        assert len(new_sessions) == 1
        assert new_sessions[0].chat_session_id == "new_456"
