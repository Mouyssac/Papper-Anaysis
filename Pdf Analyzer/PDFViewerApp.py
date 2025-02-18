import tkinter as tk
from tkinter import Menu, ttk, messagebox
from Page_manager import *
from Mouse_manager import *
from Text_manager import *
from Block_actions import Merge_block, Create_block, Resize
from PIL import Image, ImageTk
from Tools import var_init
import copy
from File_manager import Save_file, Save_file_as, New_file, Open_file, sure_to_quit_dial



class PDFViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Viewer")
        
        var_init(self)

        # Nouveau Frame pour les signets
        self.outline_frame = tk.Frame(self.master, width=200)
        self.outline_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Listbox pour afficher les signets
        self.outline_listbox = tk.Listbox(self.outline_frame, width=30)
        self.outline_listbox.pack(fill=tk.BOTH, expand=True)
        # Configurer le scroll horizontal
        scroll_x = tk.Scrollbar(self.outline_frame, orient=tk.HORIZONTAL, command=self.outline_listbox.xview)
        self.outline_listbox.config(xscrollcommand=scroll_x.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

                
        # Variables to track drag-and-select
        self.drag_start_x = None
        self.drag_start_y = None
        self.selection_rectangle = None

        self.blocks_data = []
        self.rect_colors = {}

        # Transparent image
        self.transparent_image_tk = None
        self.transparent_image_id = None
        self.border_rectangle = None


        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)


        self.btn_prev = ttk.Button(self.master, text="Previous", command=lambda: show_prev_page(self))
        self.btn_prev.pack(side=tk.TOP, padx=10)

        self.btn_next = ttk.Button(self.master, text="Next", command=lambda: show_next_page(self))
        self.btn_next.pack(side=tk.TOP, padx=10)

        self.btn_extract_text = ttk.Button(self.master, text="AI Analysis", command=lambda: extract_text(self))
        self.btn_extract_text.pack(side=tk.TOP, padx=20)
        # Désactivation du bouton après un certain événement
        self.btn_extract_text.config(state="disabled")

        self.btn_analyse = ttk.Button(self.master, text="Structure Analysis", command=lambda: analyse_pdf(self))
        self.btn_analyse.pack(side=tk.TOP, padx=20)

        self.show_red_boxes_var = tk.BooleanVar(value=True)
        self.checkbox_show_red_boxes = ttk.Checkbutton(self.master, text="Show Red Boxes", variable=self.show_red_boxes_var, command=lambda: toggle_boxes(self))
        self.checkbox_show_red_boxes.pack(side=tk.TOP, anchor=tk.W, padx=10)

        self.show_green_boxes_var = tk.BooleanVar(value=False)
        self.checkbox_show_green_boxes = ttk.Checkbutton(self.master, text="Show Green Boxes", variable=self.show_green_boxes_var, command=lambda: toggle_boxes(self))
        self.checkbox_show_green_boxes.pack(side=tk.TOP, anchor=tk.W, padx=10)

        self.show_purple_boxes_var = tk.BooleanVar(value=True)
        self.checkbox_show_purple_boxes = ttk.Checkbutton(self.master, text="Show Purple Boxes", variable=self.show_purple_boxes_var, command=lambda: toggle_boxes(self))
        self.checkbox_show_purple_boxes.pack(side=tk.TOP, anchor=tk.W, padx=10)

        self.show_blue_boxes_var = tk.BooleanVar(value=True)
        self.checkbox_show_blue_boxes = ttk.Checkbutton(self.master, text="Show Blue Boxes", variable=self.show_blue_boxes_var, command=lambda: toggle_boxes(self))
        self.checkbox_show_blue_boxes.pack(side=tk.TOP, anchor=tk.W, padx=10)

        self.show_dark_blue_frames_var = tk.BooleanVar(value=False)
        self.checkbox_show_dark_blue_frames = ttk.Checkbutton(self.master, text="Show Dark Blue Frames", variable=self.show_dark_blue_frames_var, command=lambda: toggle_boxes(self))
        self.checkbox_show_dark_blue_frames.pack(side=tk.TOP, anchor=tk.W, padx=10)

      # Charger les images des icônes de flèches
        print(self.script_path)
        undo_arrow_img = Image.open( os.path.join(self.script_path, "Icons\\undo.png") )  # Remplacez par le chemin de votre fichier
        undo_arrow_img = undo_arrow_img.resize((30, 30), Image.Resampling.LANCZOS)
        self.undo_arrow_photo = ImageTk.PhotoImage(undo_arrow_img)

        # Créer un cadre pour les boutons
        frame_buttons = tk.Frame(self.master)
        frame_buttons.pack(side=tk.TOP, anchor=tk.E, pady=(20, 100))  # Ajustez la valeur '30' selon vos besoins

        # Créer les boutons avec les images
        self.btn_undo = ttk.Button(frame_buttons, image=self.undo_arrow_photo, command=self.undo_button)
        self.btn_undo.pack(side=tk.LEFT, padx=0, pady=0)

        #self.page_label = ttk.Label(self.master, text=f"Page", font=("Helvetica", 12))
        #self.page_label.pack()

        ## Remplacer le Label par un Entry
        #self.page_entry = ttk.Entry(self.master, width=10, font=("Helvetica", 12))
        #self.page_entry.pack()

        # Création du label fixe pour "Page"
        self.page_label_fixed = ttk.Label(self.master, text="Page", font=("Helvetica", 12))
        self.page_label_fixed.pack(side=tk.LEFT)

        # Création de l'Entry pour le numéro de la page
        self.page_entry = ttk.Entry(self.master, width=5, font=("Helvetica", 12))
        self.page_entry.pack(side=tk.LEFT)

        # Création du label fixe pour "de {len(self.doc)}"
        self.page_label_total = ttk.Label(self.master, text=f"  ", font=("Helvetica", 12))
        self.page_label_total.pack(side=tk.LEFT)
        

        # Create the main context menu
        self.context_menu = Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Merge Blocks", command=lambda: Merge_block(self))
        self.context_menu.add_command(label="New Block", command=lambda: Create_block(self))
        self.context_menu.add_command(label="Resize", command=lambda: Resize(self))
        self.context_menu.entryconfig("Merge Blocks", state=tk.DISABLED)
        self.context_menu.entryconfig("New Block", state=tk.DISABLED)
        self.context_menu.entryconfig("Resize", state=tk.DISABLED)

        # Create the "Tag as..." submenu
        self.tag_menu = Menu(self.context_menu, tearoff=0)
        self.tag_menu.add_command(label="Tag as Text",     command=lambda: tag_block(self, 'text'))
        self.tag_menu.add_command(label="Tag as Title",    command=lambda: tag_block(self, 'title'))
        self.tag_menu.add_command(label="Tag as authors",  command=lambda: tag_block(self, 'authors'))
        self.tag_menu.add_command(label="Tag as Sources",  command=lambda: tag_block(self, 'sources'))
        self.tag_menu.add_command(label="Tag as Legend",   command=lambda: tag_block(self, 'legend'))
        self.tag_menu.add_command(label="Tag as Equation", command=lambda: tag_block(self, 'equation'))
        self.tag_menu.add_command(label="Tag as Margin",   command=lambda: tag_block(self, 'margin'))
        self.tag_menu.add_command(label="Tag as Figure",   command=lambda: tag_block(self, 'figure'))
        self.tag_menu.add_command(label="Disable Block",   command=lambda: tag_block(self, 'off'))
        # Add the "Tag as..." submenu to the main context menu
        self.context_menu.add_cascade(label="Tag as...", menu=self.tag_menu)
        self.context_menu.entryconfig("Tag as...", state=tk.DISABLED)

        buttons_config(self, 'disabled')
        self.btn_analyse.config(state='disabled')


        # Créer une barre de menu
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Ajouter le menu "File"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Ajouter les options "Save" et "Save As"
        self.file_menu.add_command(label="Open existing project", command=lambda:Open_file(self))
        self.file_menu.add_command(label="New pdf", command=lambda:New_file(self))
        self.file_menu.add_command(label="Save", command=lambda:Save_file(self))
        self.file_menu.add_command(label="Save As", command=lambda:Save_file_as(self))

        self.file_menu.entryconfig("Save", state="disabled")
        self.file_menu.entryconfig("Save As", state="disabled")


        # Bind keyboard events
        self.master.bind('<Right>', lambda event: self.btn_next.invoke())
        self.master.bind('<Left>' , lambda event: self.btn_prev.invoke())

        # Bind the function to the canvas event
        self.canvas.bind("<Button-3>", lambda event: on_right_click(self, event))
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Motion>", lambda event: on_mouse_motion(self, event))
        self.canvas.bind("<Button-1>", lambda event: on_left_click(self, event))
        self.canvas.bind("<MouseWheel>", lambda event: on_mouse_wheel(self, event))

        # Bind mouse events for drag-and-select
        self.canvas.bind("<B1-Motion>", lambda event: on_drag_motion(self, event))
        self.canvas.bind("<ButtonRelease-1>", lambda event: on_drag_release(self, event))

        # Ajouter un gestionnaire d'événements pour la touche Entrée
        self.page_entry.bind('<Return>', lambda event: choose_page(self))

        # Lier le clic de la souris à la fonction `on_item_click`
        self.outline_listbox.bind("<ButtonRelease-1>", lambda event: on_outline_click(self))

  



    def on_canvas_resize(self, event):
        show_page(self, self.current_page)

    #def close_pdf(self):
        
    #    if self.Modification_saved == False:
    #        if not messagebox.askokcancel("Quit", "Are you sure you want to quit? All unsaved changes will be lost."):
    #            return()
                    
    #    if hasattr(self, 'doc') and self.doc:
    #        self.doc.close()
    #    self.master.destroy()  

    def close_pdf(self):
        if not self.Modification_saved:
            sure_to_quit_dial(self)
            
        else:
            if hasattr(self, 'doc') and self.doc:
                self.doc.close()
            self.master.destroy()
                    


        


    def undo_button(self):
        print('undo')
        print(f'historic length: {len(self.historic)}')

        # Si l'historique a plus d'un élément, on peut annuler la dernière opération
        if len(self.historic) > 1:
            self.Block_list = copy.deepcopy(self.historic[-2])
            del(self.historic[-1])
            redraw_page(self)
            self.Modification_saved = False
            self.file_menu.entryconfig("Save", state="normal")

        else:
            print("No more actions to undo.")


def load_outline(self):
        """Charge les signets du PDF et les affiche dans la Listbox."""
        if hasattr(self, 'doc') and self.doc:
            try:
                # Obtenir les signets depuis le document
                outlines = self.doc.get_toc()  # Utilise get_toc() pour récupérer la table des matières
                for outline in outlines:
                    # Affiche le titre et la page dans la Listbox
                    self.outline_listbox.insert(tk.END, f"{outline[1]} (Page {outline[2]})")
            except Exception as e:
                print("Erreur lors du chargement des signets:", e)

def on_outline_select(self, event):
    """Handler pour changer de page lors d'un clic sur un signet."""
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        outline = self.doc.get_toc()[index]
        page_num = outline[2] - 1  # `outline[2]` donne le numéro de page (indexée à partir de 1)
        show_page(self, page_num)
