"""PDF manipulation utilities using pypdf."""
import io
import zipfile
from typing import List, Tuple, Dict, Union
from pypdf import PdfReader, PdfWriter
import streamlit as st

class PDFProcessor:
    @staticmethod
    def validate_pdf(file_bytes: bytes) -> bool:
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            _ = len(reader.pages)
            return True
        except Exception:
            return False

    @staticmethod
    def get_pdf_info(file_bytes: bytes) -> Dict:
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            return {
                'page_count': len(reader.pages),
                'metadata': {}
            }
        except Exception:
            return {'page_count': 0, 'metadata': {}}

    @staticmethod
    def merge_with_inserts(main_bytes: bytes, inserts: List[Tuple[bytes, int]]) -> bytes:
        try:
            main_reader = PdfReader(io.BytesIO(main_bytes))
            writer = PdfWriter()

            # Sort inserts by insertion position
            inserts_sorted = sorted(inserts, key=lambda x: x[1])
            insert_index = 0

            # Add pages from main PDF and insert files at appropriate positions
            for page_num in range(len(main_reader.pages)):
                writer.add_page(main_reader.pages[page_num])

                # Check if we need to insert PDFs after this page
                while (insert_index < len(inserts_sorted) and 
                       inserts_sorted[insert_index][1] == page_num + 1):

                    insert_bytes, _ = inserts_sorted[insert_index]
                    insert_reader = PdfReader(io.BytesIO(insert_bytes))

                    for insert_page in insert_reader.pages:
                        writer.add_page(insert_page)

                    insert_index += 1

            output_bytes = io.BytesIO()
            writer.write(output_bytes)
            return output_bytes.getvalue()

        except Exception as e:
            st.error(f"Error merging PDFs: {str(e)}")
            raise

    @staticmethod 
    def remove_pages(pdf_bytes: bytes, remove_list: List[int]) -> bytes:
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            writer = PdfWriter()

            total_pages = len(reader.pages)
            remove_indices = {page_num - 1 for page_num in remove_list if 1 <= page_num <= total_pages}

            for i, page in enumerate(reader.pages):
                if i not in remove_indices:
                    writer.add_page(page)

            output_bytes = io.BytesIO()
            writer.write(output_bytes)
            return output_bytes.getvalue()

        except Exception as e:
            st.error(f"Error removing pages: {str(e)}")
            raise

    @staticmethod
    def split_pdf(pdf_bytes: bytes, mode: str, param: Union[int, str]) -> Dict[str, bytes]:
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            total_pages = len(reader.pages)
            result = {}

            if mode == 'individual':
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)

                    output_bytes = io.BytesIO()
                    writer.write(output_bytes)
                    result[f'page_{i+1}.pdf'] = output_bytes.getvalue()

            return result

        except Exception as e:
            st.error(f"Error splitting PDF: {str(e)}")
            raise

    @staticmethod
    def create_zip_archive(file_dict: Dict[str, bytes], archive_name: str = "split_pdfs.zip") -> bytes:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, file_bytes in file_dict.items():
                zip_file.writestr(filename, file_bytes)
        return zip_buffer.getvalue()
