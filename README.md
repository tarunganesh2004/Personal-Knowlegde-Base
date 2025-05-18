# Personal Knowledge Base

A desktop application for managing notes with markdown support, full-text search, tag-based organization, and JSON export. Built with Python, Tkinter (ttkbootstrap), and SQLite.

## Features
- Add, edit, and delete notes with titles, markdown content, tags, and categories.
- Full-text search using SQLite FTS5.
- Organize notes by tags in a sidebar.
- Real-time markdown preview.
- Export notes as JSON.

## Requirements
- Python 3.10+
- Dependencies listed in `requirements.txt`
- A background image (`static/backgrounds/bg_image.jpg`, 1000x600 JPG)

## Setup
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd personal_knowledge_base
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add a background image to `static/backgrounds/bg_image.jpg` (e.g., a gradient or textured image).
5. Run the application:
   ```bash
   python main.py
   ```

## Usage
- **Add Note**: Enter title, content (markdown), tags (comma-separated), and category, then click "Save".
- **Edit Note**: Select a note from the list, modify fields, and click "Save".
- **Delete Note**: Select a note and click "Delete".
- **Search**: Type in the search bar and press Enter to find notes.
- **Filter by Tag**: Click a tag in the sidebar to filter notes.
- **Export**: Click "Export to JSON" and choose a file location.

## Project Structure
- `db/`: SQLite database operations.
- `ui/`: Tkinter UI components.
- `utils/`: Markdown conversion and export utilities.
- `static/`: Background images and custom styles.
- `main.py`: Application entry point.

## Notes
- The UI uses `ttkbootstrap`’s `darkly` theme for a modern, dark look with animations.
- Ensure `bg_image.jpg` exists before running the app.
- Future enhancements: PDF export, note sync across devices.