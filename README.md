# DocSuite - Professional PDF Management Suite

DocSuite is a comprehensive, production-ready Streamlit application for professional PDF management. Built with Python 3.11+ and modern UI/UX practices.

## Features

### PDF Manager
- **Advanced PDF Merge**: Insert PDFs at specific page positions with visual queue management
- **Page Remove**: Remove specific pages with range support (e.g., 2,4,10-12)
- **PDF Splitter**: Split by page ranges, every N pages, or individual pages with ZIP export

### Extensible Architecture
- Plugin system for easy tool addition
- Modular component structure
- Auto-discovery of new tools

## Quick Start

### Local Development
```bash
# Clone the repository
git clone <your-repo-url>
cd docsuite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Deploy to Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Deploy to Hostinger
Note: Hostinger shared hosting doesn't support Python apps directly. Use these alternatives:

**Option 1: Docker Container (VPS)**
```bash
# Build Docker image
docker build -t docsuite .

# Run container
docker run -p 8501:8501 docsuite
```

**Option 2: Embed via iframe**
Deploy to Streamlit Cloud first, then embed in your Hostinger site:
```html
<iframe src="https://your-app.streamlit.app" width="100%" height="800px"></iframe>
```

## File Structure
```
docsuite/
├── app.py                  # Main application entry point
├── pages/
│   └── pdf_manager.py      # PDF management tools
├── components/
│   ├── ui.py              # Reusable UI components
│   └── sidebar.py         # Navigation sidebar
├── utils/
│   └── pdf_utils.py       # PDF manipulation functions
├── tools/
│   ├── registry.py        # Auto-discovery system
│   └── plot_digitizer_template.py  # Template for new tools
├── static/
│   └── styles.css         # Custom CSS styling
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker containerization
└── tests/                # Unit tests
    └── test_pdf_utils.py
```

## Adding New Tools

1. Create a new file in `tools/` folder (e.g., `tools/my_tool.py`)
2. Implement the required interface:
```python
def get_tool_info():
    return {
        "name": "My Tool",
        "description": "Tool description",
        "icon": "🔧"
    }

def render_tool():
    st.write("Your tool interface here")
```
3. The tool will be auto-discovered and added to the sidebar

## Configuration

### Environment Variables
- `DOCSUITE_MAX_FILE_SIZE`: Maximum file size in MB (default: 50)
- `DOCSUITE_THEME`: Color theme ('teal', 'orange', 'lime')

### Streamlit Config
Edit `.streamlit/config.toml` to customize:
- Server settings
- Theme colors
- Upload limits

## Testing
```bash
# Run unit tests
pytest tests/

# Run specific test
pytest tests/test_pdf_utils.py
```

## License
MIT License - see LICENSE file for details

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support
- Documentation: See inline code comments
- Issues: Submit via GitHub Issues
- Email: developer@docsuite.app

## Roadmap
- [ ] OCR text extraction
- [ ] PDF annotation tools
- [ ] Batch processing
- [ ] Cloud storage integration
- [ ] API endpoints
