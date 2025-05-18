import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.markdown_viewer import MarkdownViewer
from utils.markdown_utils import markdown_to_html


class NoteEditor(ttk.Frame):
    def __init__(self, parent, db, on_save):
        super().__init__(parent, style="dark.TFrame")
        self.db = db
        self.on_save = on_save
        self.current_note_id = None

        # Title
        self.title_var = ttk.StringVar()
        self.title_entry = ttk.Entry(
            self, textvariable=self.title_var, style="primary.Entry"
        )
        self.title_entry.pack(fill=X, padx=5, pady=5)

        # Tags
        self.tags_var = ttk.StringVar()
        self.tags_entry = ttk.Entry(
            self, textvariable=self.tags_var, style="primary.Entry"
        )
        self.tags_entry.pack(fill=X, padx=5, pady=5)
        self.tags_entry.insert(0, "comma,separated,tags")

        # Category
        self.category_var = ttk.StringVar()
        self.category_combo = ttk.Combobox(
            self,
            textvariable=self.category_var,
            values=["General", "Work", "Personal", "Study"],
            style="primary.TCombobox",
        )
        self.category_combo.pack(fill=X, padx=5, pady=5)
        self.category_combo.set("General")

        # Content and preview
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.content_text = ttk.Text(
            self.content_frame, height=15, style="primary.Text"
        )
        self.content_text.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        self.content_text.bind("<KeyRelease>", self.update_preview)

        self.preview = MarkdownViewer(self.content_frame)
        self.preview.pack(side=RIGHT, fill=BOTH, expand=True)

        # Buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=X, padx=5, pady=5)
        self.save_button = ttk.Button(
            self.button_frame,
            text="Save",
            style="primary.TButton",
            command=self.save_note,
        )
        self.save_button.pack(side=LEFT, padx=5)
        self.delete_button = ttk.Button(
            self.button_frame,
            text="Delete",
            style="danger.TButton",
            command=self.delete_note,
        )
        self.delete_button.pack(side=LEFT, padx=5)
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Clear",
            style="secondary.TButton",
            command=self.clear_form,
        )
        self.clear_button.pack(side=LEFT, padx=5)

    def load_note(self, note_id):
        note = self.db.get_note_by_id(note_id)
        if note:
            self.current_note_id = note_id
            self.title_var.set(note["title"])
            self.tags_var.set(note["tags"] or "")
            self.category_var.set(note["category"] or "General")
            self.content_text.delete("1.0", END)
            self.content_text.insert("1.0", note["content"] or "")
            self.update_preview()

    def save_note(self):
        title = self.title_var.get().strip()
        if not title:
            ttk.messagebox.showerror("Error", "Title is required")
            return
        content = self.content_text.get("1.0", END).strip()
        tags = self.tags_var.get().strip()
        category = self.category_var.get().strip()
        if self.current_note_id:
            self.db.update_note(self.current_note_id, title, content, tags, category)
        else:
            self.current_note_id = self.db.add_note(title, content, tags, category)
        self.on_save()
        self.clear_form()

    def delete_note(self):
        if self.current_note_id:
            if ttk.messagebox.askyesno("Confirm", "Delete this note?"):
                self.db.delete_note(self.current_note_id)
                self.on_save()
                self.clear_form()

    def clear_form(self):
        self.current_note_id = None
        self.title_var.set("")
        self.tags_var.set("")
        self.category_var.set("General")
        self.content_text.delete("1.0", END)
        self.preview.clear()

    def update_preview(self, event=None):
        content = self.content_text.get("1.0", END).strip()
        html = markdown_to_html(content)
        self.preview.update_content(html)
