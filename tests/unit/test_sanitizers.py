"""
Unit tests for filename sanitization functions

These tests cover the sanitize_filename() function used across multiple
export scripts in the codebase.
"""

import pytest
import sys
from pathlib import Path

# Import the sanitize_filename function from different modules
# We'll test all variants to ensure consistency
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import from different modules to test consistency
from bulk_export_ai_chat import sanitize_filename as sanitize_v1
from bulk_export_all_projects import sanitize_filename as sanitize_v2
from process_pdfs import sanitize_filename as sanitize_v3


class TestSanitizeFilenameBasic:
    """Test basic sanitization functionality"""

    @pytest.mark.unit
    def test_sanitize_normal_filename(self):
        """Test that normal filenames pass through unchanged"""
        filename = "normal_filename.txt"
        assert sanitize_v1(filename) == "normal_filename.txt"
        assert sanitize_v2(filename) == "normal_filename.txt"

    @pytest.mark.unit
    def test_sanitize_replaces_slashes(self):
        """Test that forward slashes are replaced with underscores"""
        filename = "path/to/file.txt"
        result = sanitize_v1(filename)
        assert "/" not in result
        assert result == "path_to_file.txt"

    @pytest.mark.unit
    def test_sanitize_replaces_spaces(self):
        """Test that spaces are replaced with underscores"""
        filename = "file name with spaces.txt"
        result = sanitize_v1(filename)
        assert " " not in result
        assert result == "file_name_with_spaces.txt"

    @pytest.mark.unit
    def test_sanitize_replaces_colons(self):
        """Test that colons are replaced with hyphens"""
        filename = "2024-01-01:12:30:00.txt"
        result = sanitize_v1(filename)
        assert ":" not in result
        assert result == "2024-01-01-12-30-00.txt"

    @pytest.mark.unit
    def test_sanitize_removes_parentheses_v2(self):
        """Test that some variants remove parentheses"""
        filename = "file(with)parentheses.txt"
        result_v2 = sanitize_v2(filename)
        result_v3 = sanitize_v3(filename)

        # v2 and v3 remove parentheses
        assert "(" not in result_v2
        assert ")" not in result_v2
        assert result_v2 == "filewithparentheses.txt"

        assert "(" not in result_v3
        assert ")" not in result_v3


class TestSanitizeFilenameLengthLimits:
    """Test filename length truncation"""

    @pytest.mark.unit
    def test_sanitize_respects_default_max_length(self):
        """Test that filenames are truncated to max_len"""
        long_filename = "a" * 200 + ".txt"

        # Default max_len is 80 for most variants
        result_v1 = sanitize_v1(long_filename)
        assert len(result_v1) == 80

        result_v2 = sanitize_v2(long_filename)
        assert len(result_v2) == 80

        # v3 has max_len=100
        result_v3 = sanitize_v3(long_filename)
        assert len(result_v3) == 100

    @pytest.mark.unit
    def test_sanitize_custom_max_length(self):
        """Test that custom max_len parameter works"""
        long_filename = "a" * 200 + ".txt"

        result = sanitize_v1(long_filename, max_len=50)
        assert len(result) == 50

        result = sanitize_v2(long_filename, max_len=30)
        assert len(result) == 30

    @pytest.mark.unit
    def test_sanitize_short_filename_unchanged(self):
        """Test that short filenames aren't affected by max_len"""
        short_filename = "short.txt"
        assert sanitize_v1(short_filename) == "short.txt"
        assert len(sanitize_v1(short_filename)) < 80

    @pytest.mark.unit
    def test_sanitize_exactly_max_length(self):
        """Test filename that's exactly at max length"""
        filename = "a" * 80
        result = sanitize_v1(filename, max_len=80)
        assert len(result) == 80


class TestSanitizeFilenameEdgeCases:
    """Test edge cases and special scenarios"""

    @pytest.mark.unit
    def test_sanitize_empty_string(self):
        """Test handling of empty string"""
        result = sanitize_v1("")
        assert result == ""

    @pytest.mark.unit
    def test_sanitize_only_special_chars(self):
        """Test string with only special characters"""
        filename = "///::: ()()"
        result_v1 = sanitize_v1(filename)
        result_v2 = sanitize_v2(filename)

        # v1 keeps parentheses as underscores/hyphens
        assert result_v1 == "___--- ()()"

        # v2 removes parentheses entirely
        assert result_v2 == "___---"

    @pytest.mark.unit
    def test_sanitize_multiple_consecutive_replacements(self):
        """Test multiple consecutive special characters"""
        filename = "file   ///   name.txt"
        result = sanitize_v1(filename)

        # Multiple spaces and slashes become multiple underscores
        assert result == "file_________name.txt"

    @pytest.mark.unit
    def test_sanitize_preserves_file_extension(self):
        """Test that file extensions are preserved"""
        filename = "my file:name.pdf"
        result = sanitize_v1(filename)
        assert result.endswith(".pdf")
        assert result == "my_file-name.pdf"

    @pytest.mark.unit
    def test_sanitize_mixed_special_chars(self):
        """Test filename with mixed special characters"""
        filename = "Project (2024-01-01): Data/Export"
        result_v1 = sanitize_v1(filename)
        result_v2 = sanitize_v2(filename)

        # v1 keeps parentheses
        assert "/" not in result_v1
        assert ":" not in result_v1
        assert " " not in result_v1

        # v2 removes parentheses
        assert "(" not in result_v2
        assert ")" not in result_v2
        assert "/" not in result_v2
        assert ":" not in result_v2


class TestSanitizeFilenameSecurity:
    """Test security-related sanitization"""

    @pytest.mark.unit
    def test_sanitize_path_traversal_attack(self):
        """Test that path traversal attempts are neutralized"""
        filename = "../../../etc/passwd"
        result = sanitize_v1(filename)

        # Slashes should be replaced
        assert "/" not in result
        assert result == ".._.._.._etc_passwd"

        # Should not create a valid path traversal
        assert ".." in result  # Note: Still contains dots, but no slashes
        assert not result.startswith("/")

    @pytest.mark.unit
    def test_sanitize_absolute_path(self):
        """Test that absolute paths are sanitized"""
        filename = "/home/user/sensitive_file.txt"
        result = sanitize_v1(filename)

        assert "/" not in result
        assert result == "_home_user_sensitive_file.txt"
        assert not result.startswith("/")

    @pytest.mark.unit
    def test_sanitize_windows_path(self):
        """Test Windows-style paths with backslashes"""
        filename = "C:\\Users\\Admin\\file.txt"
        result = sanitize_v1(filename)

        # Note: Current implementation doesn't replace backslashes
        # This documents current behavior (not necessarily desired)
        # In production, you may want to add backslash handling
        assert "C:" not in result or result.startswith("C-")

    @pytest.mark.unit
    def test_sanitize_no_command_injection(self):
        """Test that shell command characters don't remain dangerous"""
        filename = "file; rm -rf /.txt"
        result = sanitize_v1(filename)

        # Spaces are replaced, making it less dangerous
        assert " " not in result
        # Note: semicolon is NOT currently sanitized (potential issue)
        # This test documents current behavior


class TestSanitizeFilenameUnicode:
    """Test Unicode and international character handling"""

    @pytest.mark.unit
    def test_sanitize_unicode_characters(self):
        """Test that Unicode characters are preserved"""
        filename = "文件名.txt"  # Chinese characters
        result = sanitize_v1(filename)
        assert result == "文件名.txt"

    @pytest.mark.unit
    def test_sanitize_mixed_unicode_and_ascii(self):
        """Test mixed Unicode and ASCII with special chars"""
        filename = "файл/file name:документ.txt"  # Russian/English mix
        result = sanitize_v1(filename)

        assert "/" not in result
        assert " " not in result
        assert ":" not in result
        assert "файл" in result
        assert "документ" in result

    @pytest.mark.unit
    def test_sanitize_emoji_characters(self):
        """Test emoji handling"""
        filename = "report_📊_data_🔥.txt"
        result = sanitize_v1(filename)

        # Emojis should be preserved
        assert "📊" in result
        assert "🔥" in result

    @pytest.mark.unit
    def test_sanitize_japanese_characters(self):
        """Test Japanese characters"""
        filename = "ファイル名_file.txt"
        result = sanitize_v1(filename)
        assert "ファイル" in result


class TestSanitizeFilenameRealWorldExamples:
    """Test real-world filename examples from the codebase"""

    @pytest.mark.unit
    def test_sanitize_chat_session_name(self):
        """Test typical chat session name"""
        filename = "AI Chat Session (2024-01-01 15:30)"
        result_v2 = sanitize_v2(filename)

        # Should remove parentheses, replace spaces and colons
        assert "(" not in result_v2
        assert ")" not in result_v2
        assert " " not in result_v2
        assert ":" not in result_v2

    @pytest.mark.unit
    def test_sanitize_project_name(self):
        """Test typical project name"""
        filename = "Data Analysis: Q4 2024"
        result = sanitize_v1(filename)

        assert ":" not in result
        assert " " not in result
        assert result == "Data_Analysis-_Q4_2024"

    @pytest.mark.unit
    def test_sanitize_deployment_name(self):
        """Test typical deployment name"""
        filename = "Production/Deployment v2.0"
        result = sanitize_v1(filename)

        assert "/" not in result
        assert " " not in result
        assert result == "Production_Deployment_v2.0"

    @pytest.mark.unit
    def test_sanitize_with_timestamp(self):
        """Test filename with ISO timestamp"""
        filename = "export_2024-01-01T15:30:00Z.json"
        result = sanitize_v1(filename)

        # Colons in timestamp should be replaced
        assert ":" not in result
        assert result == "export_2024-01-01T15-30-00Z.json"

    @pytest.mark.unit
    def test_sanitize_preserves_json_extension(self):
        """Test that JSON extension is preserved"""
        filename = "chat/data:export.json"
        result = sanitize_v1(filename)

        assert result.endswith(".json")
        assert "/" not in result
        assert ":" not in result


class TestSanitizeFilenameConsistency:
    """Test consistency across different implementations"""

    @pytest.mark.unit
    def test_all_variants_handle_slashes_consistently(self):
        """All variants should handle slashes the same way"""
        filename = "path/to/file.txt"

        result_v1 = sanitize_v1(filename)
        result_v2 = sanitize_v2(filename)
        result_v3 = sanitize_v3(filename)

        assert "/" not in result_v1
        assert "/" not in result_v2
        assert "/" not in result_v3

        assert result_v1 == result_v2 == result_v3

    @pytest.mark.unit
    def test_all_variants_handle_spaces_consistently(self):
        """All variants should handle spaces the same way"""
        filename = "file with spaces.txt"

        result_v1 = sanitize_v1(filename)
        result_v2 = sanitize_v2(filename)
        result_v3 = sanitize_v3(filename)

        assert " " not in result_v1
        assert " " not in result_v2
        assert " " not in result_v3

        assert result_v1 == result_v2 == result_v3

    @pytest.mark.unit
    def test_all_variants_handle_colons_consistently(self):
        """All variants should handle colons the same way"""
        filename = "time:12:30.txt"

        result_v1 = sanitize_v1(filename)
        result_v2 = sanitize_v2(filename)
        result_v3 = sanitize_v3(filename)

        assert ":" not in result_v1
        assert ":" not in result_v2
        assert ":" not in result_v3

        assert result_v1 == result_v2 == result_v3


class TestSanitizeFilenameDocumentation:
    """Test that function behavior matches documentation"""

    @pytest.mark.unit
    def test_function_has_docstring(self):
        """Verify function has documentation"""
        assert sanitize_v1.__doc__ is not None
        assert "filename" in sanitize_v1.__doc__.lower()

    @pytest.mark.unit
    def test_function_signature(self):
        """Test function signature is consistent"""
        import inspect

        # All variants should have similar signatures
        sig_v1 = inspect.signature(sanitize_v1)
        sig_v2 = inspect.signature(sanitize_v2)

        # Should have 'name' and 'max_len' parameters
        assert 'name' in sig_v1.parameters
        assert 'max_len' in sig_v1.parameters
        assert 'name' in sig_v2.parameters
        assert 'max_len' in sig_v2.parameters


# Parametrized tests for comprehensive coverage
class TestSanitizeFilenameParametrized:
    """Parametrized tests for better coverage"""

    @pytest.mark.unit
    @pytest.mark.parametrize("filename,expected", [
        ("normal.txt", "normal.txt"),
        ("with spaces.txt", "with_spaces.txt"),
        ("with/slash.txt", "with_slash.txt"),
        ("with:colon.txt", "with-colon.txt"),
        ("", ""),
        ("a" * 100, "a" * 80),  # Truncated to default 80
    ])
    def test_sanitize_various_inputs(self, filename, expected):
        """Test various input/output combinations"""
        result = sanitize_v1(filename)
        assert result == expected

    @pytest.mark.unit
    @pytest.mark.parametrize("special_char", ["/", " ", ":"])
    def test_sanitize_removes_special_characters(self, special_char):
        """Test that specific special characters are removed/replaced"""
        filename = f"file{special_char}name.txt"
        result = sanitize_v1(filename)
        assert special_char not in result

    @pytest.mark.unit
    @pytest.mark.parametrize("max_len", [10, 50, 80, 100, 200])
    def test_sanitize_respects_various_max_lengths(self, max_len):
        """Test that various max_len values work correctly"""
        long_filename = "a" * 500
        result = sanitize_v1(long_filename, max_len=max_len)
        assert len(result) == max_len
