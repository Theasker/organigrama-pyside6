import ttkbootstrap as tb
from ttkbootstrap.constants import *

try:
    # Intentamos iniciar con ttkbootstrap
    app = tb.Window(themename="darkly", title="Organigrama DGA")
except ImportError:
    # Si falla usamos tkinter
    import tkinter as tk
    app = tk.Tk()
    app
    
app.geometry("800x600")
app.resizable(False, False)                                

# Marco Superior (Encabezado)
header_frame = tb.Frame(app, padding=5)
header_frame.pack()

header_label = tb.Label(
    header_frame,
    text="Estructura organizativa DGA",
    font=("Helvetica", 16, "bold"),
    bootstyle="success"
)
header_label.pack()

# Marco central (Área de contenido)
content_frame = tb.Frame(app)
content_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

dir_general = tb.Button(
    content_frame, 
    text="Dirección General", 
    bootstyle="info",
    width=25
)
dir_general.pack(pady=10)

# Línea visual (un separador)
separador = tb.Separator(content_frame, orient="horizontal")
separador.pack(fill=X, pady=15)

app.mainloop()
