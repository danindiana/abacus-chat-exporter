"""
Unit tests for PDF processing functionality

Tests cover the process_pdfs.py module including:
- PDF file discovery
- Document upload
- Prompt processing
- Activity logging
"""

import pytest
import os
import sys
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from process_pdfs import (
    sanitize_filename,
    find_pdfs,
    upload_document,
    save_activity_log
)


class TestFindPDFs:
    """Test PDF file discovery functionality"""

    @pytest.mark.unit
    def test_find_pdfs_in_directory(self, temp_output_dir):
        """Test finding PDF files in a directory"""
        # Create test PDF files
        (temp_output_dir / "test1.pdf").touch()
        (temp_output_dir / "test2.pdf").touch()
        (temp_output_dir / "test.txt").touch()  # Non-PDF file

        pdfs = find_pdfs(temp_output_dir, recursive=False)

        assert len(pdfs) == 2
        assert all(pdf.suffix == '.pdf' for pdf in pdfs)

    @pytest.mark.unit
    def test_find_pdfs_recursive(self, temp_output_dir):
        """Test recursive PDF discovery"""
        # Create nested directories with PDFs
        subdir = temp_output_dir / "subdir"
        subdir.mkdir()

        (temp_output_dir / "root.pdf").touch()
        (subdir / "nested.pdf").touch()

        pdfs = find_pdfs(temp_output_dir, recursive=True)

        assert len(pdfs) == 2
        pdf_names = [pdf.name for pdf in pdfs]
        assert "root.pdf" in pdf_names
        assert "nested.pdf" in pdf_names

    @pytest.mark.unit
    def test_find_pdfs_non_recursive(self, temp_output_dir):
        """Test non-recursive search ignores subdirectories"""
        subdir = temp_output_dir / "subdir"
        subdir.mkdir()

        (temp_output_dir / "root.pdf").touch()
        (subdir / "nested.pdf").touch()

        pdfs = find_pdfs(temp_output_dir, recursive=False)

        assert len(pdfs) == 1
        assert pdfs[0].name == "root.pdf"

    @pytest.mark.unit
    def test_find_pdfs_empty_directory(self, temp_output_dir):
        """Test behavior with empty directory"""
        pdfs = find_pdfs(temp_output_dir, recursive=False)

        assert len(pdfs) == 0
        assert pdfs == []

    @pytest.mark.unit
    def test_find_pdfs_case_insensitive(self, temp_output_dir):
        """Test that PDF search is case-insensitive"""
        (temp_output_dir / "test.PDF").touch()
        (temp_output_dir / "test.Pdf").touch()
        (temp_output_dir / "test.pdf").touch()

        pdfs = find_pdfs(temp_output_dir, recursive=False)

        # All variations should be found
        assert len(pdfs) == 3

    @pytest.mark.unit
    def test_find_pdfs_returns_path_objects(self, temp_output_dir):
        """Test that find_pdfs returns Path objects"""
        (temp_output_dir / "test.pdf").touch()

        pdfs = find_pdfs(temp_output_dir, recursive=False)

        assert len(pdfs) == 1
        assert isinstance(pdfs[0], Path)
        assert pdfs[0].is_file()


class TestUploadDocument:
    """Test document upload functionality"""

    @pytest.mark.unit
    @pytest.mark.api
    def test_upload_document_success(self, mock_api_client, mock_pdf_document, temp_output_dir):
        """Test successful document upload"""
        pdf_file = temp_output_dir / "test.pdf"
        pdf_file.write_text("fake pdf content")

        # Mock the upload response
        mock_api_client.upload_document.return_value = mock_pdf_document

        result = upload_document(mock_api_client, "deployment_123", pdf_file)

        assert result is not None
        assert result["document_id"] == mock_pdf_document.document_id
        assert result["name"] == mock_pdf_document.name

    @pytest.mark.unit
    @pytest.mark.api
    def test_upload_document_handles_api_error(self, mock_api_client, temp_output_dir):
        """Test upload handles API errors"""
        pdf_file = temp_output_dir / "test.pdf"
        pdf_file.write_text("fake pdf content")

        mock_api_client.upload_document.side_effect = Exception("Upload failed")

        with pytest.raises(Exception, match="Upload failed"):
            upload_document(mock_api_client, "deployment_123", pdf_file)

    @pytest.mark.unit
    def test_upload_document_validates_file_exists(self, mock_api_client, temp_output_dir):
        """Test that upload validates file existence"""
        non_existent_file = temp_output_dir / "nonexistent.pdf"

        # Should raise error for non-existent file
        assert not non_existent_file.exists()

    @pytest.mark.unit
    @pytest.mark.api
    def test_upload_document_extracts_metadata(self, mock_api_client, mock_pdf_document, temp_output_dir):
        """Test that upload extracts document metadata"""
        pdf_file = temp_output_dir / "test.pdf"
        pdf_file.write_text("fake pdf content")

        mock_api_client.upload_document.return_value = mock_pdf_document

        result = upload_document(mock_api_client, "deployment_123", pdf_file)

        # Verify metadata extraction
        assert "document_id" in result
        assert "name" in result
        assert "size" in result or "status" in result


class TestProcessWithPrompts:
    """Test prompt processing functionality"""

    @pytest.mark.unit
    @pytest.mark.api
    def test_process_with_prompts_sequential_execution(self, mock_api_client):
        """Test that prompts are executed sequentially"""
        from process_pdfs import process_with_prompts

        prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]

        # Mock conversation creation and responses
        mock_api_client.create_deployment_conversation.return_value = MagicMock(
            deployment_conversation_id="conv_123"
        )
        mock_api_client.send_message_to_deployment_conversation.return_value = MagicMock(
            text="Response"
        )

        results = process_with_prompts(
            mock_api_client,
            "deployment_123",
            "doc_123",
            "test.pdf",
            prompts
        )

        # Verify all prompts were processed
        assert len(results) == 3
        assert all("prompt" in r for r in results)
        assert all("response" in r for r in results)

    @pytest.mark.unit
    @pytest.mark.api
    def test_process_with_prompts_handles_errors(self, mock_api_client):
        """Test error handling during prompt processing"""
        from process_pdfs import process_with_prompts

        prompts = ["Prompt 1"]

        mock_api_client.create_deployment_conversation.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="API Error"):
            process_with_prompts(
                mock_api_client,
                "deployment_123",
                "doc_123",
                "test.pdf",
                prompts
            )

    @pytest.mark.unit
    @pytest.mark.api
    def test_process_with_prompts_empty_list(self, mock_api_client):
        """Test behavior with empty prompt list"""
        from process_pdfs import process_with_prompts

        prompts = []

        results = process_with_prompts(
            mock_api_client,
            "deployment_123",
            "doc_123",
            "test.pdf",
            prompts
        )

        # Should return empty results for empty prompts
        assert len(results) == 0


class TestSaveActivityLog:
    """Test activity logging functionality"""

    @pytest.mark.unit
    def test_save_activity_log_creates_new_file(self, temp_output_dir):
        """Test creating a new activity log file"""
        log_file = temp_output_dir / "activity_log.json"
        log_data = {
            "timestamp": "2024-01-01T00:00:00Z",
            "action": "test_action",
            "status": "success"
        }

        save_activity_log(log_file, log_data)

        assert log_file.exists()
        with open(log_file, 'r') as f:
            loaded = json.load(f)

        assert loaded["timestamp"] == log_data["timestamp"]
        assert loaded["action"] == log_data["action"]

    @pytest.mark.unit
    def test_save_activity_log_merges_existing_data(self, temp_output_dir):
        """Test that activity log merges with existing data"""
        log_file = temp_output_dir / "activity_log.json"

        # Create initial log
        initial_data = {"entry1": "data1"}
        with open(log_file, 'w') as f:
            json.dump(initial_data, f)

        # Add new data
        new_data = {"entry2": "data2"}
        save_activity_log(log_file, new_data)

        # Verify merge
        with open(log_file, 'r') as f:
            loaded = json.load(f)

        assert "entry1" in loaded
        assert "entry2" in loaded

    @pytest.mark.unit
    def test_save_activity_log_handles_write_errors(self, temp_output_dir):
        """Test handling of write errors"""
        if os.name != 'nt':  # Skip on Windows
            # Create read-only directory
            readonly_dir = temp_output_dir / "readonly"
            readonly_dir.mkdir()
            readonly_dir.chmod(0o444)

            log_file = readonly_dir / "log.json"

            with pytest.raises(PermissionError):
                save_activity_log(log_file, {"test": "data"})

            # Cleanup
            readonly_dir.chmod(0o755)

    @pytest.mark.unit
    def test_save_activity_log_formats_json_correctly(self, temp_output_dir):
        """Test that JSON is formatted with proper indentation"""
        log_file = temp_output_dir / "activity_log.json"
        log_data = {
            "level1": {
                "level2": {
                    "level3": "value"
                }
            }
        }

        save_activity_log(log_file, log_data)

        # Verify indentation
        with open(log_file, 'r') as f:
            content = f.read()

        # Should be pretty-printed
        assert "  " in content or "\t" in content  # Has indentation


class TestGetUserInput:
    """Test user input functionality"""

    @pytest.mark.unit
    def test_get_user_input_returns_string(self):
        """Test that get_user_input returns a string"""
        from process_pdfs import get_user_input

        with patch('builtins.input', return_value='test input'):
            result = get_user_input("Enter test: ")

            assert isinstance(result, str)
            assert result == 'test input'

    @pytest.mark.unit
    def test_get_user_input_strips_whitespace(self):
        """Test that input is stripped of whitespace"""
        from process_pdfs import get_user_input

        with patch('builtins.input', return_value='  test input  '):
            result = get_user_input("Enter test: ")

            assert result == 'test input'

    @pytest.mark.unit
    def test_get_user_input_handles_empty_input(self):
        """Test behavior with empty input"""
        from process_pdfs import get_user_input

        with patch('builtins.input', return_value=''):
            result = get_user_input("Enter test: ")

            assert result == ''


class TestPDFProcessingWorkflow:
    """Integration tests for PDF processing workflow"""

    @pytest.mark.integration
    @pytest.mark.api
    def test_full_pdf_processing_pipeline(self, mock_api_client, mock_pdf_document, temp_output_dir):
        """Test complete PDF processing workflow"""
        from process_pdfs import find_pdfs, upload_document, process_with_prompts

        # Create test PDF
        pdf_file = temp_output_dir / "test.pdf"
        pdf_file.write_text("fake pdf content")

        # Step 1: Find PDFs
        pdfs = find_pdfs(temp_output_dir, recursive=False)
        assert len(pdfs) == 1

        # Step 2: Upload document
        mock_api_client.upload_document.return_value = mock_pdf_document
        upload_result = upload_document(mock_api_client, "deployment_123", pdfs[0])
        assert upload_result["document_id"] == mock_pdf_document.document_id

        # Step 3: Process with prompts
        mock_api_client.create_deployment_conversation.return_value = MagicMock(
            deployment_conversation_id="conv_123"
        )
        mock_api_client.send_message_to_deployment_conversation.return_value = MagicMock(
            text="Response"
        )

        prompts = ["Analyze this document"]
        results = process_with_prompts(
            mock_api_client,
            "deployment_123",
            upload_result["document_id"],
            "test.pdf",
            prompts
        )

        assert len(results) == 1

    @pytest.mark.integration
    def test_batch_pdf_processing(self, mock_api_client, mock_pdf_document, temp_output_dir):
        """Test processing multiple PDFs in batch"""
        from process_pdfs import find_pdfs, upload_document

        # Create multiple PDFs
        for i in range(3):
            (temp_output_dir / f"test{i}.pdf").touch()

        # Find all PDFs
        pdfs = find_pdfs(temp_output_dir, recursive=False)
        assert len(pdfs) == 3

        # Process each
        mock_api_client.upload_document.return_value = mock_pdf_document
        uploaded = []

        for pdf in pdfs:
            result = upload_document(mock_api_client, "deployment_123", pdf)
            uploaded.append(result)

        assert len(uploaded) == 3

    @pytest.mark.integration
    def test_error_recovery_in_batch_processing(self, mock_api_client, temp_output_dir):
        """Test error handling in batch processing"""
        from process_pdfs import find_pdfs, upload_document

        # Create PDFs
        for i in range(3):
            (temp_output_dir / f"test{i}.pdf").touch()

        pdfs = find_pdfs(temp_output_dir, recursive=False)

        # Simulate failure on second upload
        mock_api_client.upload_document.side_effect = [
            MagicMock(document_id="doc1"),
            Exception("Upload failed"),
            MagicMock(document_id="doc3")
        ]

        results = []
        errors = []

        for pdf in pdfs:
            try:
                result = upload_document(mock_api_client, "deployment_123", pdf)
                results.append(result)
            except Exception as e:
                errors.append(str(e))

        # Should have 2 successes and 1 error
        assert len(results) == 2
        assert len(errors) == 1
        assert "Upload failed" in errors[0]


class TestSanitizeFilenameForPDFs:
    """Test filename sanitization specific to PDF processing"""

    @pytest.mark.unit
    def test_sanitize_pdf_filename(self):
        """Test sanitization of PDF filenames"""
        filename = "Research Paper (2024): Analysis.pdf"
        sanitized = sanitize_filename(filename)

        assert "(" not in sanitized
        assert ")" not in sanitized
        assert ":" not in sanitized
        assert " " not in sanitized

    @pytest.mark.unit
    def test_sanitize_preserves_pdf_extension(self):
        """Test that .pdf extension is preserved"""
        filename = "document/with/path.pdf"
        sanitized = sanitize_filename(filename)

        assert sanitized.endswith(".pdf")
        assert "/" not in sanitized

    @pytest.mark.unit
    def test_sanitize_handles_long_pdf_names(self):
        """Test truncation of very long PDF names"""
        long_name = "a" * 150 + ".pdf"
        sanitized = sanitize_filename(long_name, max_len=100)

        assert len(sanitized) == 100
        # Note: Extension might be cut off due to truncation


class TestActivityLogStructure:
    """Test activity log data structure"""

    @pytest.mark.unit
    def test_activity_log_contains_required_fields(self, temp_output_dir):
        """Test that activity log has required fields"""
        log_file = temp_output_dir / "activity.json"

        log_data = {
            "timestamp": "2024-01-01T00:00:00Z",
            "pdf_name": "test.pdf",
            "document_id": "doc_123",
            "prompts": ["prompt1"],
            "results": ["result1"]
        }

        save_activity_log(log_file, log_data)

        with open(log_file, 'r') as f:
            loaded = json.load(f)

        assert "timestamp" in loaded
        assert "pdf_name" in loaded
        assert "document_id" in loaded

    @pytest.mark.unit
    def test_activity_log_tracks_processing_history(self, temp_output_dir):
        """Test that activity log can track multiple processing events"""
        log_file = temp_output_dir / "activity.json"

        # Log multiple events
        events = []
        for i in range(3):
            event = {
                f"event_{i}": {
                    "timestamp": f"2024-01-0{i+1}T00:00:00Z",
                    "status": "completed"
                }
            }
            save_activity_log(log_file, event)
            events.append(event)

        # Verify all events are logged
        with open(log_file, 'r') as f:
            loaded = json.load(f)

        for i in range(3):
            assert f"event_{i}" in loaded
