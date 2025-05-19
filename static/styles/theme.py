import ttkbootstrap as ttk
from ttkbootstrap.style import Style


def apply_custom_styles():
    style = Style()

    # Main frame (light background)
    style.configure("Main.TFrame", background="#f8f9fa")

    # Navbar
    style.configure(
        "Navbar.TFrame", background="#e9ecef", borderwidth=1, relief="raised"
    )

    # Sidebar
    style.configure("Sidebar.TFrame", background="#e9ecef")

    # Card-like frames
    style.configure("Card.TLabelframe", background="#ffffff", relief="flat")
    style.configure(
        "Card.TLabelframe.Label", background="#ffffff", foreground="#212529"
    )

    # Panedwindow
    style.configure("Main.Panedwindow", background="#f8f9fa")

    # Labels
    style.configure(
        "Main.Label", background="#f8f9fa", foreground="#212529", font=("Helvetica", 12)
    )

    # Treeview
    style.configure("Treeview", rowheight=30, font=("Helvetica", 11))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
