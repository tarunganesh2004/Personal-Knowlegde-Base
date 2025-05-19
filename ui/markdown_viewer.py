import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class MarkdownViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = ttk.Text(
            self,
            height=15,
            wrap=WORD,
            state="disabled",
            font=("Helvetica", 12),
            bg="#ffffff",
            fg="#212529",
        )
        self.text.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Configure basic styles
        self.text.tag_configure("bold", font=("Helvetica", 12, "bold"))
        self.text.tag_configure("italic", font=("Helvetica", 12, "italic"))
        self.text.tag_configure("heading", font=("Helvetica", 16, "bold"))

    def update_content(self, html):
        self.text.configure(state="normal")
        self.text.delete("1.0", END)
        current_tag = None
        buffer = ""
        i = 0
        while i < len(html):
            if html[i] == "<":
                if buffer:
                    self.text.insert(END, buffer)
                    buffer = ""
                i += 1
                if html[i : i + 2] == "b>":
                    current_tag = "bold"
                    i += 2
                elif html[i : i + 2] == "i>":
                    current_tag = "italic"
                    i += 2
                elif html[i : i + 3] == "h1>":
                    current_tag = "heading"
                    i += 3
                elif html[i : i + 3] in ["</b>", "</i>", "</h1>"]:
                    current_tag = None
                    i += 3
            else:
                buffer += html[i]
                i += 1
            if buffer and current_tag:
                self.text.insert(END, buffer, current_tag)
                buffer = ""
        if buffer:
            self.text.insert(END, buffer)
        self.text.configure(state="disabled")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", END)
        self.text.configure(state="disabled")
