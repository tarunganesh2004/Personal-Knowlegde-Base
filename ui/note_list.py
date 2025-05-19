import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class NoteList(ttk.Frame):
    def __init__(self, parent, db, on_select):
        super().__init__(parent, style="Main.TFrame")
        self.db = db
        self.on_select = on_select

        # Note list
        self.note_tree = ttk.Treeview(
            self, columns=("id", "title"), show="headings", style="Treeview"
        )
        self.note_tree.heading("title", text="Notes")
        self.note_tree.column("id", width=0, stretch=False)
        self.note_tree.column("title", width=200)
        self.note_tree.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.note_tree.bind("<<TreeviewSelect>>", self.on_note_select)

        self.load_notes()

    def load_notes(self):
        self.note_tree.delete(*self.note_tree.get_children())
        notes = self.db.get_all_notes()
        for note in notes:
            self.note_tree.insert("", END, values=(note["id"], note["title"]))

    def filter_by_tag(self, tag):
        self.note_tree.delete(*self.note_tree.get_children())
        notes = self.db.get_all_notes()
        for note in notes:
            if note["tags"] and tag in [t.strip() for t in note["tags"].split(",")]:
                self.note_tree.insert("", END, values=(note["id"], note["title"]))

    def search_notes(self, query):
        self.note_tree.delete(*self.note_tree.get_children())
        notes = self.db.search_notes(query)
        for note in notes:
            self.note_tree.insert("", END, values=(note["id"], note["title"]))

    def on_note_select(self, event):
        selected = self.note_tree.selection()
        if selected:
            note_id = self.note_tree.item(selected[0])["values"][0]
            self.on_select(note_id)
