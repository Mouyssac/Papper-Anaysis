from tkinter import messagebox
from Page_manager import redraw_page
from Tools import flatten_list, Update_historic, buttons_config, merge_positions
from Block_class import *
from PIL import Image, ImageTk, ImageDraw


def Merge_block(self):
    Previous_Block_list = self.Block_list
    #self.selected_rect_ids


    ids_consecutive = []

    if self.selected_rect_ids:
        self.selected_rect_ids.sort()
        sublist = [self.selected_rect_ids[0]]

        # Iterate through the elements of the initial list starting from the second element
        for i in range(1, len(self.selected_rect_ids)):
            # Check if the current element is exactly 1 more than the previous element
            if self.selected_rect_ids[i] == self.selected_rect_ids[i - 1] + 1:
                # If yes, add it to the current sub-list
                sublist.append(self.selected_rect_ids[i])
            else:
                # If no, add the current sub-list to the result list and start a new sub-list
                ids_consecutive.append(sublist)
                sublist = [self.selected_rect_ids[i]]

        # Add the last sub-list to the result list
        ids_consecutive.append(sublist)
        ids_to_remove = []

        for i in ids_consecutive:
            x0, y0, x1, y1, text = [], [], [], [], []
            first_iteration = True
            need_to_check_type = True

            for idx in i:
                Block = self.Block_list[idx]
                if first_iteration: 
                    Block_type_1 = Block.type
                    Block_idx_1 = Block.idx
                    first_iteration = False
                else:
                    ids_to_remove.append(idx)

                if Block.type != Block_type_1:
                    response = messagebox.askquestion("Error", f"All blocks must have identical type. Turn all into {Block_type_1} type?")
                    # Gestion de la r�ponse
                    if response == 'yes':
                        print("L'utilisateur a choisi Oui")
                        for ids in i:
                            self.Block_list[ids].type = Block_type_1
                    else:
                        print("L'utilisateur a choisi Non")
                        return()
            
                text.append(Block.text)
                x0.append(Block.position[0])
                y0.append(Block.position[1])
                x1.append(Block.position[2])
                y1.append(Block.position[3])
                
        
            self.Block_list[Block_idx_1].text = text
            self.Block_list[Block_idx_1].position = (min(x0), min(y0), max(x1), max(y1)) 
            self.Block_list[Block_idx_1].type =  Block_type_1
            self.Block_list[Block_idx_1].merged = True
            ids_in_merged_group = [Block_idx_1] + ids_to_remove
            original_ids = [self.Block_list[idx].original_idx for idx in ids_in_merged_group]
            self.Block_list[Block_idx_1].original_idx = original_ids

     
        print(f"Ids to remove {ids_to_remove}")
        print(f"Original ids { self.Block_list[Block_idx_1].original_idx}\n")
            
        new_block_list = [block for idx, block in enumerate(self.Block_list) if idx not in ids_to_remove]
    
        for new_idx, block in enumerate(new_block_list):
            new_block_list[new_idx].idx = new_idx
    
        self.Block_list = new_block_list

        redraw_page(self)
        self.selected_rect_ids = []
        Update_historic(self)



def Create_block(self):

    print('New block creation')
    self.new_block_mode = True

    buttons_config(self,'disabled')

    self.canvas.config(cursor="cross")


    # Obtenir la taille du canevas
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()

    # Cr�er une image semi-transparente qui couvre toute la page
    semi_transparent_image = Image.new('RGBA', (canvas_width, canvas_height), (128, 128, 128, 128))

    # Convertir l'image en PhotoImage pour l'afficher sur le canevas
    self.semi_transparent_image_tk = ImageTk.PhotoImage(semi_transparent_image)
    self.resize_transparent_image_id = self.canvas.create_image(0, 0, image=self.semi_transparent_image_tk, anchor='nw')
    

    self.current_page_last_id = [block.idx for block in self.Block_list if block.page == self.current_page][-1] if any(block.page == self.current_page for block in self.Block_list) else None
    

def Resize(self):
    print('Resize')
    self.resize_mode = True
    self.id_to_resize = self.selected_rect_ids[0]

    buttons_config(self,'disabled')


    # Obtenir la taille du canevas
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()

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


    # Mettre le curseur de la souris en croix
    self.canvas.config(cursor="cross")
    