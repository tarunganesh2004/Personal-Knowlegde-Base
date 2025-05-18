import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from ui.note_list import NoteList
from ui.note_editor import NoteEditor
from db.database import Database
from utils.export_utils import export_notes_to_json


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Personal Knowledge Base")
        self.geometry("1000x600")
        self.minsize(800, 500)
        self.db = Database()

        # Load background image
        bg_image = Image.open("static/backgrounds/bg_image.jpg")
        bg_image = bg_image.resize((1000, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create canvas for background
        self.canvas = ttk.Canvas(self)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=NW)

        # Create main frame
        self.main_frame = ttk.Frame(self.canvas, style="dark.TFrame")
        self.canvas.create_window((0, 0), window=self.main_frame, anchor=NW)

        # Sidebar (tags)
        self.sidebar = ttk.Frame(self.main_frame, width=200, style="secondary.TFrame")
        self.sidebar.grid(row=0, column=0, sticky=NS, padx=5, pady=5)
        self.tag_list = ttk.Treeview(
            self.sidebar, style="primary.Treeview", show="tree"
        )
        self.tag_list.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.tag_list.bind("<<TreeviewSelect>>", self.on_tag_select)
        self.update_tags()

        # Note list
        self.note_list_frame = ttk.Frame(self.main_frame, style="dark.TFrame")
        self.note_list_frame.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)
        self.note_list = NoteList(self.note_list_frame, self.db, self.on_note_select)
        self.note_list.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Note editor
        self.editor_frame = ttk.Frame(self.main_frame, style="dark.TFrame")
        self.editor_frame.grid(row=0, column=2, sticky=NSEW, padx=5, pady=5)
        self.note_editor = NoteEditor(self.editor_frame, self.db, self.on_note_save)
        self.note_editor.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Export button
        self.export_button = ttk.Button(
            self.main_frame,
            text="Export to JSON",
            style="primary.TButton",
            command=self.export_notes,
        )
        self.export_button.grid(row=1, column=2, sticky=E, padx=5, pady=5)

        # Configure grid weights for responsiveness
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=2)
        self.main_frame.rowconfigure(0, weight=1)

        # Bind window resize to update background
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Resize background image to fit window
        width, height = self.winfo_width(), self.winfo_height()
        bg_image = Image.open("static/backgrounds/bg_image.jpg")
        bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=NW)

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

    def on_note_select(self, note_id):
        self.note_editor.load_note(note_id)

    def on_note_save(self):
        self.note_list.load_notes()
        self.update_tags()

    def export_notes(self):
        filename = ttk.filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if filename:
            export_notes_to_json(self.db, filename)
