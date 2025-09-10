"""Unit tests for PDF utilities."""
import pytest
from unittest.mock import Mock, patch
from utils.pdf_utils import PDFProcessor

class TestPDFProcessor:
    def test_validate_pdf_valid(self):
        with patch('utils.pdf_utils.PdfReader') as mock_reader:
            mock_instance = Mock()
            mock_instance.pages = [Mock(), Mock()]
            mock_reader.return_value = mock_instance

            result = PDFProcessor.validate_pdf(b"fake_pdf_bytes")
            assert result is True

    def test_validate_pdf_invalid(self):
        with patch('utils.pdf_utils.PdfReader') as mock_reader:
            mock_reader.side_effect = Exception("Invalid PDF")

            result = PDFProcessor.validate_pdf(b"invalid_bytes")
            assert result is False

if __name__ == "__main__":
    pytest.main([__file__])
