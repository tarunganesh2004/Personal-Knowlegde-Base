import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ui.note_list import NoteList
from ui.note_editor import NoteEditor
from db.database import Database
from utils.export_utils import export_notes_to_json
from static.styles.theme import apply_custom_styles


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")
        self.title("Personal Knowledge Base")
        self.geometry("1200x700")
        self.minsize(800, 500)
        self.db = Database()
        apply_custom_styles()

        # Load background image (fallback to solid color if image fails)
        try:
            bg_image = Image.open("static/backgrounds/bg_image.jpg")
            bg_image = bg_image.resize((1200, 700), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
        except:
            self.bg_photo = None

        # Main container
        self.main_frame = ttk.Frame(self, style="Main.TFrame")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Navbar
        self.navbar = ttk.Frame(self.main_frame, style="Navbar.TFrame")
        self.navbar.pack(fill=X, padx=10, pady=(10, 5))

        self.new_note_btn = ttk.Button(
            self.navbar, text="New Note", style="primary.TButton", command=self.new_note
        )
        self.new_note_btn.pack(side=LEFT, padx=5)

        self.search_var = ttk.StringVar()
        self.search_entry = ttk.Entry(
            self.navbar, textvariable=self.search_var, style="primary.Entry"
        )
        self.search_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.search_entry.bind("<Return>", self.on_search)

        self.export_btn = ttk.Button(
            self.navbar,
            text="Export to JSON",
            style="secondary.TButton",
            command=self.export_notes,
        )
        self.export_btn.pack(side=RIGHT, padx=5)

        # Content area with sidebar and main content
        self.content_frame = ttk.Frame(self.main_frame, style="Main.TFrame")
        self.content_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Sidebar toggle
        self.sidebar_visible = True
        self.sidebar_frame = ttk.Frame(
            self.content_frame, width=200, style="Sidebar.TFrame"
        )
        self.sidebar_frame.pack(side=LEFT, fill=Y, padx=(0, 5))

        self.toggle_btn = ttk.Button(
            self.sidebar_frame,
            text="Hide Tags",
            style="info.TButton",
            command=self.toggle_sidebar,
        )
        self.toggle_btn.pack(fill=X, padx=5, pady=5)

        self.tag_list = ttk.Treeview(self.sidebar_frame, style="Treeview", show="tree")
        self.tag_list.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.tag_list.bind("<<TreeviewSelect>>", self.on_tag_select)
        self.update_tags()

        # Separator
        self.sep = ttk.Separator(self.content_frame, orient=VERTICAL)
        self.sep.pack(side=LEFT, fill=Y, padx=2)

        # Main content (note list + editor)
        self.main_content = ttk.PanedWindow(
            self.content_frame, orient=HORIZONTAL, style="Main.Panedwindow"
        )
        self.main_content.pack(fill=BOTH, expand=True)

        # Note list
        self.note_list_frame = ttk.Frame(self.main_content, style="Main.TFrame")
        self.main_content.add(self.note_list_frame, weight=1)
        self.note_list = NoteList(self.note_list_frame, self.db, self.on_note_select)
        self.note_list.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Note editor
        self.editor_frame = ttk.Frame(self.main_content, style="Main.TFrame")
        self.main_content.add(self.editor_frame, weight=2)
        self.note_editor = NoteEditor(self.editor_frame, self.db, self.on_note_save)
        self.note_editor.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Bind resize for background
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        if self.bg_photo:
            width, height = self.winfo_width(), self.winfo_height()
            try:
                bg_image = Image.open("static/backgrounds/bg_image.jpg")
                bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
            except:
                self.bg_photo = None

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.toggle_btn.configure(text="Show Tags")
            self.sidebar_visible = False
        else:
            self.sidebar_frame.pack(side=LEFT, fill=Y, padx=(0, 5))
            self.toggle_btn.configure(text="Hide Tags")
            self.sidebar_visible = True

    def update_tags(self):
        self.tag_list.delete(*self.tag_list.get_children())
        tags = self.db.get_all_tags()
        for tag in tags:
            self.tag_list.insert("", END, text=tag, values=(tag,))

    def on_tag_select(self, event):
        selected = self.tag_list.selection()
        if selected:
            tag = self.tag_list.item(selected[0])["values"][0]
            self.note_list.filter_by_tag(tag)
        else:
            self.note_list.load_notes()

    def on_search(self, event):
        query = self.search_var.get().strip()
        if query:
            self.note_list.search_notes(query)
        else:
            self.note_list.load_notes()

    def on_note_select(self, note_id):
        self.note_editor.load_note(note_id)

    def on_note_save(self):
        self.note_list.load_notes()
        self.update_tags()

    def new_note(self):
        self.note_editor.clear_form()

    def export_notes(self):
        filename = ttk.filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if filename:
            export_notes_to_json(self.db, filename)
