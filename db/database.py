import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path="knowledge_base.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Create notes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    tags TEXT,
                    category TEXT,
                    created_at TIMESTAMP
                )
            """)
            # Create FTS5 virtual table for full-text search
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                    title, content, tokenize=porter
                )
            """)
            conn.commit()

    def add_note(self, title, content, tags, category):
        created_at = datetime.now()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO notes (title, content, tags, category, created_at) VALUES (?, ?, ?, ?, ?)",
                (title, content, tags, category, created_at),
            )
            note_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO notes_fts (rowid, title, content) VALUES (?, ?, ?)",
                (note_id, title, content),
            )
            conn.commit()
        return note_id

    def update_note(self, note_id, title, content, tags, category):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET title = ?, content = ?, tags = ?, category = ? WHERE id = ?",
                (title, content, tags, category, note_id),
            )
            cursor.execute(
                "INSERT OR REPLACE INTO notes_fts (rowid, title, content) VALUES (?, ?, ?)",
                (note_id, title, content),
            )
            conn.commit()

    def delete_note(self, note_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            cursor.execute("DELETE FROM notes_fts WHERE rowid = ?", (note_id,))
            conn.commit()

    def get_all_notes(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
            return cursor.fetchall()

    def get_note_by_id(self, note_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
            return cursor.fetchone()

    def search_notes(self, query):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT rowid FROM notes_fts WHERE notes_fts MATCH ? ORDER BY rank",
                (query,),
            )
            note_ids = [row["rowid"] for row in cursor.fetchall()]
            if not note_ids:
                return []
            placeholders = ",".join("?" for _ in note_ids)
            cursor.execute(
                f"SELECT * FROM notes WHERE id IN ({placeholders}) ORDER BY created_at DESC",
                note_ids,
            )
            return cursor.fetchall()

    def get_all_tags(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tags FROM notes")
            tags = set()
            for row in cursor.fetchall():
                if row[0]:
                    tags.update(tag.strip() for tag in row[0].split(","))
            return sorted(tags)
