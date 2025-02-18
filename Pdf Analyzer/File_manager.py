from tkinter import filedialog, ttk, messagebox
import fitz
from Tools import var_init, buttons_config
from Page_manager import show_page
import pickle
import tkinter as tk


def Save_file(self):
	print('Saving...')
	data = {
	'pdf_path':self.pdf_path,
	'already_analysed':self.already_analysed,
    'current_page': self.current_page,
    'historic': self.historic,
   	'Block_list': self.Block_list,
	'saving_path': self.saving_path 
}
	
	with open(self.saving_path, 'wb') as file:
		pickle.dump(data, file)
		print(f"Project saved in '{self.saving_path}'.")

	self.Modification_saved = True
	self.file_menu.entryconfig("Save", state="disabled")



def Save_file_as(self):
	#self.saving_file = filedialog.askdirectory(title="Select a directory", initialdir=self.pdf_path)

	self.saving_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
	print(f'Saving in {self.saving_path}')
	
	Save_file(self)


def Open_file(self):
	load_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
	if load_path:
			try:
				with open(load_path, 'rb') as file:
					data_loaded = pickle.load(file)
					print(f"Data extracted from '{load_path}'.")
					var_init(self)
					self.pdf_path = data_loaded['pdf_path']
					self.historic = data_loaded['historic']
					self.already_analysed = data_loaded['already_analysed']
					self.Block_list = data_loaded['Block_list']
					self.saving_path = data_loaded['saving_path']
					#var_init(self)
					buttons_config(self, 'normal')
					if self.already_analysed:
						self.btn_analyse.config(state = 'disabled')
					else:
						self.btn_analyse.config(state = 'normal')

					self.file_menu.entryconfig("Save", state="disabled")
					self.file_menu.entryconfig("Save As", state="normal")

					#self.btn_analyse.config(state='normal')
					#self.file_menu.entryconfig("Save As", state="normal")
			
					Open_pdf(self)
					show_page(self, self.current_page)
			except IOError as e:
				print(f"Error while loading file : {e}")
	else:
		print("No file selected for loading.")
	return None

def New_file(self):

	if not self.Modification_saved:
            
		custom_quit_dialog = tk.Toplevel(self.master)
		custom_quit_dialog.title("Quit")
		custom_quit_dialog.geometry("250x80")
		custom_quit_dialog.grab_set()  # Prevent interaction with the main window

		style = ttk.Style()
		style.configure("TLabel", font=("Calibri", 10))
		style.configure("TButton", font=("Calibri", 8), padding=1)

		label = ttk.Label(custom_quit_dialog, text="ARE YOU SURE YOU WANT TO QUIT?\nAll unsaved changes will be lost.", wraplength=380)
		label.pack(pady=5)

		def on_quit():
			custom_quit_dialog.destroy()
			if hasattr(self, 'doc') and self.doc:
				self.doc.close()
			#self.master.destroy()

		def on_cancel():
			custom_quit_dialog.destroy()

		button_frame = ttk.Frame(custom_quit_dialog)
		button_frame.pack(pady=2)

		quit_button = ttk.Button(button_frame, text="Quit", command=on_quit)
		quit_button.pack(side=tk.LEFT, padx=10, pady=1)

		cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
		cancel_button.pack(side=tk.LEFT, padx=10, pady=1)

		self.master.wait_window(custom_quit_dialog)  # Attend la fermeture avant de continuer


	pdf_path = filedialog.askopenfilename(title="Select a file",filetypes=[("PDF files", "*.pdf")])
	if not pdf_path: 
		#pdf_path = "C:\\Users\\maxim\\source\\repos\\Paper Mapping\\Paper Mapping\\Var\\Virgin_PDF.pdf"
		return()
	
	if pdf_path.lower().endswith('.pdf'):
		self.pdf_path = pdf_path
		var_init(self)
		buttons_config(self,'normal')
		self.btn_extract_text.config(state="disabled")
		self.btn_analyse.config(state='normal')
		self.outline_listbox.delete(0, tk.END)

		self.file_menu.entryconfig("Save As", state="normal")
		self.file_menu.entryconfig("Save", state="disabled")
		self.Modification_saved = False
		self.saving_path = []
		self.pdf_loaded = True

		Open_pdf(self)
		show_page(self, self.current_page)
	else:
		messagebox.showinfo("Warning", "The file selected is not a .pdf")

def Open_pdf(self):
    self.doc = fitz.open(self.pdf_path)
    

def check_last_save_time(self):
	print('File Open')


def sure_to_quit_dial(self):
    custom_quit_dialog = tk.Toplevel(self.master)
    custom_quit_dialog.title("Quit")
    custom_quit_dialog.geometry("250x80")
    custom_quit_dialog.grab_set()  # Prevent interaction with the main window

    style = ttk.Style()
    style.configure("TLabel", font=("Calibri", 10))
    style.configure("TButton", font=("Calibri", 8), padding=1)

    label = ttk.Label(custom_quit_dialog, text="ARE YOU SURE YOU WANT TO QUIT?\nAll unsaved changes will be lost.", wraplength=380)
    label.pack(pady=5)

    def on_quit():
        custom_quit_dialog.destroy()
        if hasattr(self, 'doc') and self.doc:
            self.doc.close()
        self.master.destroy()

    def on_cancel():
        custom_quit_dialog.destroy()

    button_frame = ttk.Frame(custom_quit_dialog)
    button_frame.pack(pady=2)

    quit_button = ttk.Button(button_frame, text="Quit", command=on_quit)
    quit_button.pack(side=tk.LEFT, padx=10, pady=1)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.pack(side=tk.LEFT, padx=10, pady=1)

    self.master.wait_window(custom_quit_dialog)  # Wait until the custom dialog is closed

