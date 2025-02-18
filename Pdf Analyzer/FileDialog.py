import tkinter as tk
from tkinter import filedialog

class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Selector")

        # Cr�er un cadre pour contenir le bouton et le label
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10, padx=10, fill=tk.X)

        # Cr�er un bouton pour ouvrir la bo�te de dialogue de s�lection de fichier
        self.select_button = tk.Button(self.frame, text="Select File", command=self.open_file_dialog)
        self.select_button.grid(row=0, column=0, padx=5)

        # Cr�er un label pour afficher le chemin du fichier s�lectionn�
        self.path_label = tk.Label(self.frame, text="No file selected", anchor='w')
        self.path_label.grid(row=0, column=1, padx=5, sticky='w')

    def open_file_dialog(self):
        # Ouvrir la bo�te de dialogue pour s�lectionner un fichier
        file_path = filedialog.askopenfilename(title="Select a file")

        # Mettre � jour le texte du label avec le chemin du fichier s�lectionn�
        if file_path:
            self.path_label.config(text=f"Selected file: {file_path}")
        else:
            self.path_label.config(text="No file selected or dialog was cancelled")

# Cr�er une instance de la fen�tre principale
root = tk.Tk()
app = FileSelectorApp(root)
root.mainloop()
