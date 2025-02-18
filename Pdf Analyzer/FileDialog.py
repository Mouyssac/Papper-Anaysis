import tkinter as tk
from tkinter import filedialog

class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Selector")

        # Créer un cadre pour contenir le bouton et le label
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10, padx=10, fill=tk.X)

        # Créer un bouton pour ouvrir la boîte de dialogue de sélection de fichier
        self.select_button = tk.Button(self.frame, text="Select File", command=self.open_file_dialog)
        self.select_button.grid(row=0, column=0, padx=5)

        # Créer un label pour afficher le chemin du fichier sélectionné
        self.path_label = tk.Label(self.frame, text="No file selected", anchor='w')
        self.path_label.grid(row=0, column=1, padx=5, sticky='w')

    def open_file_dialog(self):
        # Ouvrir la boîte de dialogue pour sélectionner un fichier
        file_path = filedialog.askopenfilename(title="Select a file")

        # Mettre à jour le texte du label avec le chemin du fichier sélectionné
        if file_path:
            self.path_label.config(text=f"Selected file: {file_path}")
        else:
            self.path_label.config(text="No file selected or dialog was cancelled")

# Créer une instance de la fenêtre principale
root = tk.Tk()
app = FileSelectorApp(root)
root.mainloop()
