# Library Management System (Flask + JSON)

## Features
- Dashboard with total, available, and issued book counts
- Add books
- Search by Book ID
- Issue books to students
- Return issued books
- Delete books
- Persistent storage in `books.json`

## Run on macOS
1. Open this folder in VS Code.
2. In the terminal, install Flask:
   ```bash
   python3 -m pip install flask
   ```
3. Start the application:
   ```bash
   python3 app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

Book records are automatically saved in `books.json`. Keep this file in the same folder as `app.py`; do not reset it to `[]` if you want to keep saved records.
