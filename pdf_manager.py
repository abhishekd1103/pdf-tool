"""
PDF Manager with fully functional PDF operations
"""

import streamlit as st
import io
import zipfile
from typing import List, Tuple, Dict
from pypdf import PdfReader, PdfWriter

class PDFProcessor:
    """PDF processing utilities"""

    @staticmethod
    def validate_pdf(file_bytes: bytes) -> bool:
        """Validate PDF file"""
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            _ = len(reader.pages)
            return True
        except Exception:
            return False

    @staticmethod
    def get_pdf_info(file_bytes: bytes) -> Dict:
        """Get PDF information"""
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            return {
                'page_count': len(reader.pages),
                'title': getattr(reader.metadata, 'title', 'Unknown') if reader.metadata else 'Unknown'
            }
        except Exception:
            return {'page_count': 0, 'title': 'Unknown'}

    @staticmethod
    def merge_pdfs(main_bytes: bytes, insert_list: List[Tuple[bytes, int]]) -> bytes:
        """Merge PDFs with insertion points"""
        try:
            main_reader = PdfReader(io.BytesIO(main_bytes))
            writer = PdfWriter()

            # Sort inserts by position
            inserts_sorted = sorted(insert_list, key=lambda x: x[1])
            insert_index = 0

            # Process main PDF pages
            for page_num in range(len(main_reader.pages)):
                # Add main page
                writer.add_page(main_reader.pages[page_num])

                # Check for inserts after this page
                while (insert_index < len(inserts_sorted) and 
                       inserts_sorted[insert_index][1] == page_num + 1):

                    insert_bytes, _ = inserts_sorted[insert_index]
                    insert_reader = PdfReader(io.BytesIO(insert_bytes))

                    # Add all pages from insert PDF
                    for insert_page in insert_reader.pages:
                        writer.add_page(insert_page)

                    insert_index += 1

            # Handle beginning inserts (position 0)
            if inserts_sorted and inserts_sorted[0][1] == 0:
                new_writer = PdfWriter()

                # Add beginning inserts first
                for insert_bytes, position in inserts_sorted:
                    if position == 0:
                        insert_reader = PdfReader(io.BytesIO(insert_bytes))
                        for page in insert_reader.pages:
                            new_writer.add_page(page)

                # Add main content
                for page in writer.pages:
                    new_writer.add_page(page)

                writer = new_writer

            # Write to bytes
            output = io.BytesIO()
            writer.write(output)
            return output.getvalue()

        except Exception as e:
            st.error(f"Merge error: {str(e)}")
            raise

    @staticmethod
    def remove_pages(pdf_bytes: bytes, pages_to_remove: List[int]) -> bytes:
        """Remove specific pages from PDF"""
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            writer = PdfWriter()

            total_pages = len(reader.pages)
            remove_set = set(p - 1 for p in pages_to_remove if 1 <= p <= total_pages)

            # Add pages not in remove set
            for i, page in enumerate(reader.pages):
                if i not in remove_set:
                    writer.add_page(page)

            output = io.BytesIO()
            writer.write(output)
            return output.getvalue()

        except Exception as e:
            st.error(f"Remove error: {str(e)}")
            raise

    @staticmethod
    def split_pdf(pdf_bytes: bytes, mode: str, pages_per_split: int = 1) -> Dict[str, bytes]:
        """Split PDF into multiple files"""
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            total_pages = len(reader.pages)
            result = {}

            if mode == 'individual':
                # One page per file
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)

                    output = io.BytesIO()
                    writer.write(output)
                    result[f'page_{i+1}.pdf'] = output.getvalue()

            elif mode == 'every_n':
                # N pages per file
                for start in range(0, total_pages, pages_per_split):
                    end = min(start + pages_per_split, total_pages)

                    writer = PdfWriter()
                    for i in range(start, end):
                        writer.add_page(reader.pages[i])

                    output = io.BytesIO()
                    writer.write(output)
                    result[f'pages_{start+1}-{end}.pdf'] = output.getvalue()

            return result

        except Exception as e:
            st.error(f"Split error: {str(e)}")
            raise

def render_pdf_manager():
    """Main PDF Manager interface"""

    st.markdown("### 🔧 Professional PDF Tools")

    # Create tabs for different tools
    tab1, tab2, tab3 = st.tabs(["🔗 PDF Merge", "❌ Page Remove", "✂️ PDF Splitter"])

    with tab1:
        render_pdf_merge()

    with tab2:
        render_page_remove()

    with tab3:
        render_pdf_splitter()

def render_pdf_merge():
    """PDF Merge tool"""
    st.markdown('<div class="tool-section">', unsafe_allow_html=True)

    st.markdown("#### 🔗 Advanced PDF Merge")
    st.info("Combine multiple PDFs with precise insertion control")

    # Step 1: Main PDF Upload
    st.markdown("**Step 1: Upload Main PDF**")
    main_pdf = st.file_uploader(
        "Choose the main PDF file",
        type=['pdf'],
        key="main_pdf_upload",
        help="This will be the base document"
    )

    if main_pdf:
        main_bytes = main_pdf.read()
        if PDFProcessor.validate_pdf(main_bytes):
            st.session_state.main_pdf = {
                'name': main_pdf.name,
                'bytes': main_bytes,
                'info': PDFProcessor.get_pdf_info(main_bytes)
            }

            col1, col2 = st.columns(2)
            with col1:
                st.success(f"✅ Main PDF: {main_pdf.name}")
            with col2:
                st.info(f"📄 Pages: {st.session_state.main_pdf['info']['page_count']}")
        else:
            st.error("❌ Invalid PDF file")
            return

    # Step 2: Insert PDFs
    if st.session_state.main_pdf:
        st.markdown("**Step 2: Add PDFs to Insert**")

        insert_pdf = st.file_uploader(
            "Choose PDF(s) to insert",
            type=['pdf'],
            accept_multiple_files=True,
            key="insert_pdfs_upload"
        )

        if insert_pdf:
            for pdf in insert_pdf:
                pdf_bytes = pdf.read()
                if PDFProcessor.validate_pdf(pdf_bytes):
                    info = PDFProcessor.get_pdf_info(pdf_bytes)

                    col1, col2, col3 = st.columns([3, 1, 1])

                    with col1:
                        st.write(f"**{pdf.name}** ({info['page_count']} pages)")

                    with col2:
                        max_pages = st.session_state.main_pdf['info']['page_count']
                        insert_pos = st.number_input(
                            "Insert after page",
                            min_value=0,
                            max_value=max_pages,
                            value=max_pages,
                            key=f"pos_{pdf.name}",
                            help="0 = beginning"
                        )

                    with col3:
                        if st.button("Add to Queue", key=f"add_{pdf.name}"):
                            queue_item = {
                                'name': pdf.name,
                                'bytes': pdf_bytes,
                                'pages': info['page_count'],
                                'position': insert_pos
                            }
                            st.session_state.merge_queue.append(queue_item)
                            st.success(f"Added {pdf.name}")
                            st.rerun()

    # Step 3: Display Queue
    if st.session_state.merge_queue:
        st.markdown("**Step 3: Merge Queue**")

        for i, item in enumerate(st.session_state.merge_queue):
            st.markdown(f"""
            <div class="queue-item">
                <strong>{item['name']}</strong> ({item['pages']} pages) 
                → Insert after page {item['position']}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Remove", key=f"remove_{i}"):
                st.session_state.merge_queue.pop(i)
                st.rerun()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔗 Start Merge", type="primary", use_container_width=True):
                try:
                    with st.spinner("Merging PDFs..."):
                        inserts = [(item['bytes'], item['position']) 
                                 for item in st.session_state.merge_queue]

                        merged = PDFProcessor.merge_pdfs(
                            st.session_state.main_pdf['bytes'],
                            inserts
                        )

                        st.session_state.merged_pdf = merged
                        st.success("✅ PDFs merged successfully!")
                        st.rerun()

                except Exception as e:
                    st.error(f"❌ Merge failed: {str(e)}")

        with col2:
            if st.button("Clear Queue", use_container_width=True):
                st.session_state.merge_queue = []
                st.rerun()

    # Step 4: Download
    if st.session_state.merged_pdf:
        st.markdown("**Step 4: Download Result**")

        main_name = st.session_state.main_pdf['name'].replace('.pdf', '')
        filename = f"{main_name}_merged.pdf"

        info = PDFProcessor.get_pdf_info(st.session_state.merged_pdf)

        col1, col2 = st.columns([3, 1])

        with col1:
            st.download_button(
                "📥 Download Merged PDF",
                data=st.session_state.merged_pdf,
                file_name=filename,
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )

        with col2:
            st.metric("Total Pages", info['page_count'])

    st.markdown('</div>', unsafe_allow_html=True)

def render_page_remove():
    """Page Remove tool"""
    st.markdown('<div class="tool-section">', unsafe_allow_html=True)

    st.markdown("#### ❌ Remove Pages")
    st.info("Remove specific pages using ranges (e.g., 2,4,10-12)")

    uploaded_file = st.file_uploader(
        "Choose PDF file",
        type=['pdf'],
        key="remove_pdf_upload"
    )

    if uploaded_file:
        pdf_bytes = uploaded_file.read()

        if PDFProcessor.validate_pdf(pdf_bytes):
            info = PDFProcessor.get_pdf_info(pdf_bytes)
            total_pages = info['page_count']

            col1, col2 = st.columns(2)

            with col1:
                st.success(f"✅ Loaded: {uploaded_file.name}")
                st.info(f"📄 Total pages: {total_pages}")

            with col2:
                st.markdown("""
                **Examples:**
                - `2,4,6` - Remove pages 2, 4, 6
                - `1-3,5` - Remove pages 1, 2, 3, 5
                - `10-12` - Remove pages 10, 11, 12
                """)

            # Page removal input
            remove_input = st.text_input(
                "Pages to remove",
                placeholder="e.g., 2,4,10-12",
                help="Use commas for individual pages, dashes for ranges"
            )

            if remove_input:
                try:
                    # Parse remove string
                    pages_to_remove = parse_page_string(remove_input, total_pages)

                    if pages_to_remove:
                        remaining = total_pages - len(pages_to_remove)

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric("Pages to Remove", len(pages_to_remove))

                        with col2:
                            st.metric("Remaining Pages", remaining)

                        if st.button("❌ Remove Pages", type="primary"):
                            if remaining <= 0:
                                st.error("Cannot remove all pages!")
                            else:
                                try:
                                    with st.spinner("Removing pages..."):
                                        result = PDFProcessor.remove_pages(pdf_bytes, pages_to_remove)

                                    filename = f"{uploaded_file.name.replace('.pdf', '')}_removed.pdf"

                                    st.download_button(
                                        "📥 Download PDF with Pages Removed",
                                        data=result,
                                        file_name=filename,
                                        mime="application/pdf",
                                        type="primary"
                                    )

                                    st.success("✅ Pages removed successfully!")

                                except Exception as e:
                                    st.error(f"❌ Remove failed: {str(e)}")
                    else:
                        st.warning("No valid pages specified")

                except Exception as e:
                    st.error(f"Invalid format: {str(e)}")
        else:
            st.error("❌ Invalid PDF file")

    st.markdown('</div>', unsafe_allow_html=True)

def render_pdf_splitter():
    """PDF Splitter tool"""
    st.markdown('<div class="tool-section">', unsafe_allow_html=True)

    st.markdown("#### ✂️ PDF Splitter")
    st.info("Split PDFs into multiple files")

    uploaded_file = st.file_uploader(
        "Choose PDF file to split",
        type=['pdf'],
        key="split_pdf_upload"
    )

    if uploaded_file:
        pdf_bytes = uploaded_file.read()

        if PDFProcessor.validate_pdf(pdf_bytes):
            info = PDFProcessor.get_pdf_info(pdf_bytes)
            total_pages = info['page_count']

            col1, col2 = st.columns(2)

            with col1:
                st.success(f"✅ Loaded: {uploaded_file.name}")
                st.info(f"📄 Total pages: {total_pages}")

            with col2:
                file_size = len(pdf_bytes) / (1024 * 1024)
                st.metric("File Size", f"{file_size:.1f} MB")

            # Split options
            split_mode = st.radio(
                "Split method:",
                ["Individual Pages", "Every N Pages"],
                horizontal=True
            )

            if split_mode == "Individual Pages":
                st.info("Split into individual PDF files (one page per file)")
                estimated_files = total_pages
                pages_per_split = 1

            else:  # Every N Pages
                pages_per_split = st.number_input(
                    "Pages per file",
                    min_value=1,
                    max_value=total_pages,
                    value=min(5, total_pages)
                )
                estimated_files = (total_pages + pages_per_split - 1) // pages_per_split

                st.info(f"Will create ~{estimated_files} files")

            if st.button("✂️ Split PDF", type="primary", use_container_width=True):
                try:
                    with st.spinner("Splitting PDF..."):
                        mode = 'individual' if split_mode == "Individual Pages" else 'every_n'
                        split_files = PDFProcessor.split_pdf(pdf_bytes, mode, pages_per_split)

                    st.success(f"✅ PDF split into {len(split_files)} files!")

                    if len(split_files) == 1:
                        # Single file
                        filename, file_bytes = next(iter(split_files.items()))
                        st.download_button(
                            f"📥 Download {filename}",
                            data=file_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            type="primary"
                        )
                    else:
                        # Create ZIP
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for filename, file_bytes in split_files.items():
                                zip_file.writestr(filename, file_bytes)

                        zip_filename = f"{uploaded_file.name.replace('.pdf', '')}_split.zip"

                        st.download_button(
                            f"📦 Download All Files (ZIP)",
                            data=zip_buffer.getvalue(),
                            file_name=zip_filename,
                            mime="application/zip",
                            type="primary"
                        )

                        st.metric("Files Created", len(split_files))

                except Exception as e:
                    st.error(f"❌ Split failed: {str(e)}")
        else:
            st.error("❌ Invalid PDF file")

    st.markdown('</div>', unsafe_allow_html=True)

def parse_page_string(page_str: str, total_pages: int) -> List[int]:
    """Parse page range string like '2,4,10-12' into list of page numbers"""
    pages = []
    parts = page_str.replace(' ', '').split(',')

    for part in parts:
        if '-' in part:
            # Range like "10-12"
            start, end = map(int, part.split('-'))
            if 1 <= start <= end <= total_pages:
                pages.extend(range(start, end + 1))
        else:
            # Single page like "4"
            page = int(part)
            if 1 <= page <= total_pages:
                pages.append(page)

    return sorted(list(set(pages)))  # Remove duplicates and sort
