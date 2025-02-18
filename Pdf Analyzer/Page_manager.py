import tkinter as tk
from PDF_drawer import *
import fitz
from PIL import Image, ImageTk, ImageDraw



def toggle_boxes(self):
    redraw_page(self)

def redraw_page(self):
    show_page(self, self.current_page)

def show_page(self, page_num):
    if self.pdf_loaded:
        #try:
        print('Updating page')
        page = self.doc.load_page(page_num)
        zoom = 2.0 # 300 DPI
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if pix.width <= 0 or pix.height <= 0:
            print(f"Invalid image dimensions for page {page_num + 1}: width={pix.width}, height={pix.height}")
            return

        self.current_page = page_num

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        image_width = pix.width
        image_height = pix.height

        scale_x = canvas_width / image_width
        scale_y = canvas_height / image_height
        self.scale = min(scale_x, scale_y) 

        self.new_width = int(image_width * self.scale)
        self.new_height = int(image_height * self.scale)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = img.resize((self.new_width, self.new_height), Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        self.scale *= zoom
        #self.page_label.config(text=f"Page {page_num + 1}/{len(self.doc)}")
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(0, f"{page_num + 1}")
        self.page_label_total.config(text=f" / {len(self.doc)}")




        if self.already_analysed :

            self.Blocks_page = [block for block in self.Block_list if block.page == page_num]
            self.Hypertext_page = [hypertext for hypertext in self.Hypertext_list if hypertext.page_number == page_num]
            
            draw_text_boxes(self,self.Blocks_page)
            draw_hypertext_boxes(self,self.Hypertext_page)
            
        
        if self.new_block_mode:
            # Cr�er une image semi-transparente qui couvre toute la page
            semi_transparent_image = Image.new('RGBA', (canvas_width, canvas_height), (128, 128, 128, 128))
            self.semi_transparent_image_tk = ImageTk.PhotoImage(semi_transparent_image)
            self.resize_transparent_image_id = self.canvas.create_image(0, 0, image=self.semi_transparent_image_tk, anchor='nw')

        if self.resize_mode:
            # Cr�er une image semi-transparente qui couvre toute la page
            semi_transparent_image = Image.new('RGBA', (canvas_width, canvas_height), (128, 128, 128, 128))

            # Convertir l'image en PhotoImage pour l'afficher sur le canevas
            self.semi_transparent_image_tk = ImageTk.PhotoImage(semi_transparent_image)
            self.resize_transparent_image_id = self.canvas.create_image(0, 0, image=self.semi_transparent_image_tk, anchor='nw')

            # Supprimer tous les cadres affich�s
            rect_list = self.canvas.find_withtag("rect")
            for rect in rect_list:
                self.canvas.delete(rect)

            x0, y0, x1, y1 = self.Block_list[self.id_to_resize].position
            rect = self.canvas.create_rectangle(
            x0*self.scale, y0*self.scale, x1*self.scale, y1*self.scale, 
            outline='black', 
            width=1, 
            dash=(10, 5),  # Longues lignes pointill�es (10 pixels de trait, 5 pixels d'espace)
            tags="rect_dash"
            )



        #except Exception as e:
        #    print(f"Error loading page {page_num + 1}: {str(e)}")

        return(self)

def show_prev_page(self):
    if self.current_page > 0:
        show_page(self,self.current_page - 1)

def show_next_page(self):
    if self.current_page < len(self.doc) - 1:
        show_page(self,self.current_page + 1)


def show_context_menu(self, event):

    print(self.selected_rect_ids)

    self.context_menu_x = self.canvas.canvasx(event.x)
    self.context_menu_y = self.canvas.canvasy(event.y)

    x, y = self.context_menu_x, self.context_menu_y
    page_block = []
    page_idx = -1

    # Find the blocks corresponding to the current page
    for idx, block in enumerate(self.Block_list):
        if block.page == self.current_page:
            page_block.append(block)
            if page_idx == -1:
                page_idx = idx

    Block_list = [block for block in self.Block_list if block.page == self.current_page]
    self.block_idx = None
    for block in Block_list:
        if block.position[0] <= x/self.scale <= block.position[2] and block.position[1] <= y/self.scale <= block.position[3]:
       
            self.block_idx = block.idx + page_idx
            break  # Exit loop once the correct block is found

    try:
        self.context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        self.context_menu.grab_release()


def choose_page(self):
    try:
        new_page_num = int(self.page_entry.get()) - 1
        if 0 <= new_page_num < len(self.doc):
            show_page(self, new_page_num)
        else:
            show_invalid_page_error(self)
    except ValueError:
        show_invalid_page_error(self)

def show_invalid_page_error(self):
    self.page_entry.delete(0, tk.END)
    self.page_entry.insert(0, f"{self.current_page + 1}")
    print("Invalid page number")
