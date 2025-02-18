import copy
from Block_class import *

def is_outside_margin ( y0, y1, header_margin, footer_margin):
    return y1 <= header_margin or y0 >= footer_margin

def is_contained( frame1, frame2, tolerance):
        return (frame1[0] >= frame2[0] - tolerance and 
                frame1[1] >= frame2[1] - tolerance and 
                frame1[2] <= frame2[2] + tolerance and 
                frame1[3] <= frame2[3] + tolerance)

def do_frames_overlap(frame1, frame2, margin=0):
    # Décomposer les coordonnées des deux frames
    x0_1, y0_1, x1_1, y1_1 = frame1
    x0_2, y0_2, x1_2, y1_2 = frame2
    
    # Appliquer la marge aux coordonnées des cadres
    x0_1 -= margin
    y0_1 -= margin
    x1_1 += margin
    y1_1 += margin
    
    x0_2 -= margin
    y0_2 -= margin
    x1_2 += margin
    y1_2 += margin
    
    # Vérifier les conditions de chevauchement
    if x1_1 > x0_2 and x0_1 < x1_2 and  y1_1 > y0_2 and y0_1 < y1_2:     
        return True
    return False

def merge_positions(position1, position2):
    # Fusionner les deux positions (en supposant que ce sont des coordonnées sous la forme (x0, y0, x1, y1))
    x0_merged = min(position1[0], position2[0])  # Prendre le minimum des x0
    y0_merged = min(position1[1], position2[1])  # Prendre le minimum des y0
    x1_merged = max(position1[2], position2[2])  # Prendre le maximum des x1
    y1_merged = max(position1[3], position2[3])  # Prendre le maximum des y1
    
    return (x0_merged, y0_merged, x1_merged, y1_merged)


def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

def Show_historic(self):
    historic_current_page = [[block for block in blocks if block.page == self.current_page] for blocks in self.historic]
    print(f'Hitoric: \n {historic_current_page}')

def Update_historic(self):
    Block_list_copy = copy.deepcopy(self.Block_list)
    self.historic.append(Block_list_copy)
    self.Modification_saved = False
    if hasattr(self,'saving_path'):
        if self.saving_path != []:
            self.file_menu.entryconfig("Save", state="normal")



def buttons_config(self, state_value):
    if state_value not in ('disabled','normal'): 
        raise ValueError("buttons_config parameter must be normal or disabled")
        
    self.checkbox_show_dark_blue_frames.config(state=state_value)
    self.checkbox_show_red_boxes.config(state=state_value)
    self.checkbox_show_green_boxes.config(state=state_value)
    self.checkbox_show_purple_boxes.config(state=state_value)
    self.checkbox_show_blue_boxes.config(state=state_value)

    self.btn_prev.config(state=state_value)
    self.btn_next.config(state=state_value)
    self.btn_extract_text.config(state=state_value)
    self.btn_undo.config(state=state_value)


def var_init(self):
    self.current_page = 0
    self.historic = []
    self.Block_list = []
    self.resize_mode = False
    self.new_block_mode = False
    self.scale = 1.0
    self.already_analysed = False
    self.saving_path = None
    self.selected_rect_ids = []
    self.Blocks_page = []
    self.Hypertext_page = []
    self.Modification_saved = True
    self.is_dragging = False
    self.mouse_on_hypertext = False
    self.current_hypertext_block = None
    self.pdf_loaded = False
    self.Hypertext_list = []
    self.outline_list = []


