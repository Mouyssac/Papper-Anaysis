from PIL import Image, ImageTk, ImageDraw
from Page_manager import *
from PDF_drawer import draw_text_boxes
from tkinter import messagebox
from Tools import Update_historic, buttons_config
import webbrowser
from Page_manager import show_page



def on_mouse_motion(self, event):
    self.x_mouse, self.y_mouse = event.x, event.y
    self.x_scaled = self.x_mouse / self.scale
    self.y_scaled = self.y_mouse / self.scale

    mouse_block_id = mouse_in_block_id(self.Blocks_page,self.x_scaled,self.y_scaled)

    last_mouse_block_id = -1

    Hypertext_found = False
    for hypertext_block in self.Hypertext_page :
        if hypertext_block.bbox[0] <= self.x_scaled <= hypertext_block.bbox[2] and hypertext_block.bbox[1] <= self.y_scaled <= hypertext_block.bbox[3]:
            Hypertext_found = True
            self.current_hypertext_block = hypertext_block
            break

    
    if mouse_block_id is not None :
            if last_mouse_block_id != mouse_block_id:
                self.canvas.delete("selection_rect")
                x0,y0,x1,y1 = self.Block_list[mouse_block_id[0]].position
                x0 *= self.scale
                y0 *= self.scale
                x1 *= self.scale
                y1 *= self.scale
                self.canvas.create_rectangle(x0, y0, x1, y1, outline='#778899', width=1, tags="selection_rect")
                last_mouse_block_id = mouse_block_id
    else:
        self.canvas.delete("selection_rect")
        

    if Hypertext_found :
        if self.canvas.find_withtag("tooltip"): self.canvas.delete("tooltip")
        if self.canvas.find_withtag("transparent_image_tooltip"):   self.canvas.delete("transparent_image_tooltip")


        self.canvas.config(cursor="hand2")
        self.mouse_on_hypertext = True
        self.canvas.create_rectangle(hypertext_block.bbox[0]*self.scale, hypertext_block.bbox[1]*self.scale, hypertext_block.bbox[2]*self.scale, hypertext_block.bbox[3]*self.scale, outline='#5B2E91', width=1, tags="temp")
        
        

        self.transparent_image_tooltip = Image.new('RGBA', (140, 12), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(self.transparent_image_tooltip)
        draw.rectangle((0, 0, 140, 12), fill=(200, 200, 200, 200))

        self.transparent_image_tooltip_tk = ImageTk.PhotoImage(self.transparent_image_tooltip)
        self.canvas.create_image(self.x_mouse-50, self.y_mouse-21,  image=self.transparent_image_tooltip_tk, anchor='nw',tags = "transparent_image_tooltip")

        self.canvas.create_rectangle(self.x_mouse-50, self.y_mouse-21, self.x_mouse+90, self.y_mouse-9, outline='#101010', width=1, tags="tooltip")
        self.canvas.create_text(self.x_mouse + 20, self.y_mouse - 14 ,text="Press CTRL + Click to open",font=("Helvetica", 8),fill="black", anchor="center", tags="tooltip")
       
    else:
        if self.canvas.find_withtag("tooltip"): self.canvas.delete("tooltip")
        if self.canvas.find_withtag("temp"): self.canvas.delete("temp")
        if self.canvas.find_withtag("transparent_image_tooltip"):   self.canvas.delete("transparent_image_tooltip")
        self.canvas.config(cursor="")
        self.mouse_on_hypertext = False
        self.current_hypertext_block = None



def on_left_click(self, event):
    self.drag_start_x = self.x_mouse
    self.drag_start_y = self.y_mouse
    self.drag_end_x = None
    self.drag_end_y = None
    self.is_dragging  = False 
    print(f'Left Click: x:{self.x_scaled}   y: {self.y_scaled}\n')

    if self.mouse_on_hypertext:
        print(self.current_hypertext_block)

        if event.state & 0x4:  # 0x4 correspond à la touche Ctrl sur de nombreux systèmes
            print("Ctrl Click Gauche")
            if self.current_hypertext_block.link_type == 1:  # URL
                print("Not implemented yet")

            if self.current_hypertext_block.link_type == 2:  # URL
                webbrowser.open(self.current_hypertext_block.uri)

            if self.current_hypertext_block.link_type == 3:  # File Link
                print("Not implemented yet")

            if self.current_hypertext_block.link_type == 4 :  # Internal link to a specific position
                target_position = self.current_hypertext_block.destination
                if target_position is not None:
                    self.current_page = self.current_hypertext_block.target_page
                    print(target_position)
                    target_position = target_position*self.scale
                    print(target_position)
                    print(f"new heigh: {self.new_height}")
                    show_page(self,self.current_page)
                    self.transparent_image = create_semi_transparent_image(10, 10, color = (10,77,51,128))
                    self.transparent_image_tk = ImageTk.PhotoImage(self.transparent_image)
                    self.transparent_image_id = self.canvas.create_image(target_position[0],self.new_height-target_position[1]+5,  image=self.transparent_image_tk, anchor='nw')
                    self.border_rectangle = self.canvas.create_rectangle(target_position[0], self.new_height-target_position[1]+5, target_position[0]+10, self.new_height-target_position[1]+15, outline='#0A4D33', width=1)
                else:
                    print("target position undefined")

    if self.selected_rect_ids:
        for idx in self.selected_rect_ids:  self.canvas.delete(f"selection_rect_{idx}")

        self.selected_rect_ids = []
    else:
        mouse_block_id = mouse_in_block_id(self.Blocks_page,self.x_scaled,self.y_scaled)

        if mouse_block_id:
            #print(f'Block idx: {self.Block_list[mouse_block_id[0]].idx}')
            #print(f'Block text: {self.Block_list[mouse_block_id[0]].text}')
            #print(f'Block type: {self.Block_list[mouse_block_id[0]].type}')
            #print("click")
            print(self.Block_list[mouse_block_id[0]])



def on_right_click(self, event):

    if not self.already_analysed:
        self.context_menu.entryconfig("New Block", state=tk.DISABLED)
    else:
    
        if self.resize_mode or self.new_block_mode:
            #Cancel the mode
            self.resize_mode = False 
            self.new_block_mode = False
            redraw_page(self)
            self.canvas.config(cursor="")
            buttons_config(self,'normal')


        else:
            # Initialiser selected_rect_ids si n�cessaire
            if self.selected_rect_ids is None:
                self.selected_rect_ids = []

            self.context_menu.entryconfig("Tag as...", state=tk.DISABLED)
            self.context_menu.entryconfig("Merge Blocks", state=tk.DISABLED)
            self.context_menu.entryconfig("New Block", state=tk.NORMAL)
            self.context_menu.entryconfig("Resize", state=tk.DISABLED)


            mouse_block_id = mouse_in_block_id(self.Blocks_page,self.x_scaled,self.y_scaled)
    
            print(mouse_block_id)

            if mouse_block_id is not None and len(self.selected_rect_ids) == 0:
                print(f'Adding mouse_block_id to selected_rect_ids: {mouse_block_id}')
                self.selected_rect_ids.append(mouse_block_id[0])

            if len(self.selected_rect_ids) == 1 and self.selected_rect_ids is not None:
                self.context_menu.entryconfig("Resize", state=tk.NORMAL)

            if len(self.selected_rect_ids) >= 1 and self.selected_rect_ids is not None:
                self.context_menu.entryconfig("Tag as...", state=tk.NORMAL)
        

            if len(self.selected_rect_ids) >= 2 and self.selected_rect_ids is not None:
                self.context_menu.entryconfig("Merge Blocks", state=tk.NORMAL)

 
            show_context_menu(self, event)

            self.is_dragging = False
            print(f'Right Click: x:{self.x_scaled}   y: {self.y_scaled}\n')


def on_mouse_wheel(self, event):
    if hasattr(self, 'doc'):
        if event.delta > 0:
            show_prev_page(self)
        else:
            show_next_page(self)


def on_drag_motion(self, event):
    if self.drag_start_x is not None and self.drag_start_y is not None:
        current_x = self.canvas.canvasx(event.x)
        current_y = self.canvas.canvasy(event.y)

        if not self.is_dragging:
            # Calculate distance from the starting point
            distance = ((current_x - self.drag_start_x)**2 + (current_y - self.drag_start_y)**2)**0.5
            if distance > 5:  # Adjust this threshold as needed
                self.is_dragging = True
                print('Drag starts\n')

        else:

            width = abs(int(current_x - self.drag_start_x))
            height = abs(int(current_y - self.drag_start_y))

            if not self.resize_mode:
                
                                
                selection_left = min(self.drag_start_x, current_x)
                selection_top = min(self.drag_start_y, current_y)
                selection_right = max(self.drag_start_x, current_x)
                selection_bottom = max(self.drag_start_y, current_y)

                # List to store the selected rectangle IDs
                if not hasattr(self, 'selected_rect_ids'):
                    self.selected_rect_ids = []

                for Block in self.Blocks_page:
                    if rectangles_intersect(
                            (selection_left, selection_top, selection_right, selection_bottom),
                            (Block.position[0]*self.scale, Block.position[1]*self.scale, Block.position[2]*self.scale, Block.position[3]*self.scale)):
                    
                        if Block.idx not in self.selected_rect_ids:
                            self.selected_rect_ids.append(Block.idx)
                
                    elif Block.idx in self.selected_rect_ids:
                        self.selected_rect_ids.remove(Block.idx)


                    if Block.idx in self.selected_rect_ids:

                        x0,y0,x1,y1 = Block.position
                        x0 *= self.scale
                        y0 *= self.scale
                        x1 *= self.scale
                        y1 *= self.scale
                        self.canvas.create_rectangle(x0, y0, x1, y1, outline='#FFD700', width=1, tags=f"selection_rect_{Block.idx}")
                        
                
                    elif self.canvas.find_withtag(f"selection_rect_{Block.idx}"):
                        self.canvas.delete(f"selection_rect_{Block.idx}")

                print(self.selected_rect_ids)

            if self.transparent_image_id:   self.canvas.delete(self.transparent_image_id)
            if self.border_rectangle:   self.canvas.delete(self.border_rectangle)

            self.transparent_image = create_semi_transparent_image(width, height)
            self.transparent_image_tk = ImageTk.PhotoImage(self.transparent_image)
            self.transparent_image_id = self.canvas.create_image(min(self.drag_start_x, current_x), min(self.drag_start_y, current_y),  image=self.transparent_image_tk, anchor='nw')
            self.border_rectangle = self.canvas.create_rectangle(self.drag_start_x, self.drag_start_y, current_x, current_y, outline='#5555AA', width=1)
            
   


   


def on_drag_release(self, event):

    if self.is_dragging:
        if self.transparent_image_id:
            self.canvas.delete(self.transparent_image_id)
        if self.border_rectangle:
            self.canvas.delete(self.border_rectangle)
        
        print('Drag release\n')
        print(f'selected ids: {self.selected_rect_ids}')
        self.drag_end_x, self.drag_end_y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        if self.resize_mode:
            print(f'resizing block: {self.id_to_resize}')
            print(f'New position: {self.drag_start_x}, {self.drag_start_y}, {self.drag_end_x}, {self.drag_end_y}')


            rect = self.canvas.create_rectangle(
            self.drag_start_x, self.drag_start_y, self.drag_end_x, self.drag_end_y, 
            outline='black', 
            width=2, 
            dash=(10, 5),  # Longues lignes pointill�es (10 pixels de trait, 5 pixels d'espace)
            tags="rect_dash"
            )

            response = messagebox.askquestion("Confirmation", f"Do you want to resize the block {self.id_to_resize}?")

            if response == 'yes':
                print("L'utilisateur a choisi Oui")
                self.Block_list[self.id_to_resize].position = self.drag_start_x/self.scale, self.drag_start_y/self.scale, self.drag_end_x/self.scale, self.drag_end_y/self.scale
                Update_historic(self)

            else:
                print("L'utilisateur a choisi Non")
                
            rect_list = self.canvas.find_withtag("rect")
            for rect in rect_list: self.canvas.delete(rect)
            self.resize_mode = False
            
            redraw_page(self)
            self.canvas.config(cursor="")
            buttons_config(self,'normal')

            return

        if self.new_block_mode:
            rect = self.canvas.create_rectangle(
            self.drag_start_x, self.drag_start_y, self.drag_end_x, self.drag_end_y, 
            outline='black', 
            width=2, 
            dash=(10, 5),  # Longues lignes pointill�es (10 pixels de trait, 5 pixels d'espace)
            tags="rect_dash"
            )

            response = messagebox.askquestion("Confirmation", f"Create anew block?")

            if response == 'yes':
                print("L'utilisateur a choisi Oui")
                new_block =   Block_class('text', 
                              (self.drag_start_x/self.scale, self.drag_start_y/self.scale, self.drag_end_x/self.scale, self.drag_end_y/self.scale), 
                              '', 
                              self.current_page, 
                              self.current_page_last_id+1, 
                              -1,
                              outline_level = 1)
                self.Block_list.insert(self.current_page_last_id, new_block)

                rect_list = self.canvas.find_withtag("rect")
                for rect in rect_list: self.canvas.delete(rect)
                
                for new_idx, block in enumerate(self.Block_list):
                    self.Block_list[new_idx].idx = new_idx

                Update_historic(self)

            else:
                print("L'utilisateur a choisi Non")
           

            self.new_block_mode = False

            redraw_page(self)
            self.canvas.config(cursor="")
            buttons_config(self,'normal')
            
            return




def create_semi_transparent_image( width, height, color=(128, 128, 256, 128) ):
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill=color)  # Semi-transparent gray rectangle
    return image



def Select_mode_context_menu(self):
    self.select_mode_var.set(not self.select_mode_var.get())
    if self.select_mode_var.get():
        # Select Mode is activated
        self.master.config(cursor="cross")
    else:
        # Select Mode is deactivated
        self.master.config(cursor="")
  


def on_toggle_select_mode(self):
    if not self.select_mode_var.get():
        # Select Mode is activated
        self.master.config(cursor="cross")
    else:
        # Select Mode is deactivated
        self.master.config(cursor="")

def mouse_in_block_id(blocks,x_mouse, y_mouse):
    block_found = False
    for block in blocks:
        if block.position[0] <= x_mouse <= block.position[2] and block.position[1] <= y_mouse <= block.position[3]:
            block_found = True
            return([block.idx])
    
    if not block_found:
        return(None)

def rectangles_intersect(r1, r2):
                return not (r1[2] < r2[0] or r1[0] > r2[2] or r1[3] < r2[1] or r1[1] > r2[3])


def draw_dashed_rectangle(canvas, x0, y0, x1, y1, dash_length=5, dash_color='yellow', dash_width=2):
    # Dessiner le haut
    for x in range(x0, x1, dash_length * 2):  # Ajouter un espacement
        canvas.create_line(x, y0, x + dash_length, y0, fill=dash_color, width=dash_width)

    # Dessiner le bas
    for x in range(x0, x1, dash_length * 2):
        canvas.create_line(x, y1, x + dash_length, y1, fill=dash_color, width=dash_width)

    # Dessiner le côté gauche
    for y in range(y0, y1, dash_length * 2):
        canvas.create_line(x0, y + dash_length, x0, y + dash_length * 2, fill=dash_color, width=dash_width)

    # Dessiner le côté droit
    for y in range(y0, y1, dash_length * 2):
        canvas.create_line(x1, y + dash_length, x1, y + dash_length * 2, fill=dash_color, width=dash_width)
