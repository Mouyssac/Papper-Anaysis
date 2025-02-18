from Block_class import *
from Hypertext_class import *
from Tools import is_outside_margin, Update_historic, do_frames_overlap, merge_positions 
import re
import tkinter as tk
import os
from LLM_analysis import analyse_LLM

class Outline:
    def __init__(self,level,title,page_num):
        self.level = level
        self.title = title
        self.page_num = page_num
    def __repr__(self):
        # Cette méthode retourne une représentation lisible de l'objet
        return f"Outline(level={self.level}, title='{self.title}', page_num={self.page_num})"


def scan_outlines(self):
    try:
        toc = self.doc.get_toc()  # Récupère la table des matières (signets)
        if toc is None:
            print("No table of contents found.")
            return
        
        self.outline_list = []

        for item in toc:

            level = item[0]  # Niveau du signet (hiérarchie)
            title = item[1]  # Titre du signet
            page_num = item[2]  # Numéro de la page du signet

            # Indentation pour les niveaux hiérarchiques
            indent = "  " * level
            
            self.outline_list.append(Outline(level,title,page_num)) 

            self.outline_listbox.insert(tk.END, f"{indent}{title}")
            
            # Affiche le titre et la page du signet
            #print(f"Bookmark: {title}, Page: {page_num}, Level: {level}")
    except Exception as e:
        print(f"Error extracting outlines: {e}")


def on_outline_click(self):
    """Fonction appelée lorsqu'on clique sur un élément de la Listbox."""
    from Page_manager import show_page

    # Obtenir l'élément sélectionné
    selection = self.outline_listbox.curselection()  # Récupère l'indice de l'élément sélectionné
    if selection:  # Vérifie si un élément est sélectionné
        index = selection[0]
        target_page = self.outline_list[index].page_num  # Récupère le texte de l'élément sélectionné
        print(f"Go to page : {target_page}")
        show_page(self,target_page-1)
    else:
        print("Aucun élément sélectionné.")
    

def scan_hypertext(self,page):
    if not hasattr(self, 'Hypertext_list'): self.Hypertext_list = []

    self.links = page.get_links()
    for link in self.links:
        uri = link.get('uri')
        bbox = link.get('from')
        link_type = link.get('kind')
        destination = link.get('to')
        target_page = link.get('page')
        
        # Extraire le texte à partir de la position du lien
        text = ""
        if bbox:  # Vérifier si bbox est disponible
            text = page.get_text("text", clip=bbox)  # Extraire le texte dans la zone du lien

        # Créer une instance de HypertextClass et l'ajouter à la liste
        hypertext = Hypertext_class(uri, bbox, link_type, destination, text, target_page, page.number)
        self.Hypertext_list.append(hypertext)  # Ajouter à la liste
       #rect = self.canvas.create_rectangle(bbox[0]*self.scale, bbox[1]*self.scale, bbox[2]*self.scale, bbox[3]*self.scale, outline='violet', width=2, tags="rect")
        #print(hypertext)


def identify_figure_block(text):
    # Expression régulière pour vérifier si le texte commence par "fig" (insensible à la casse)
    pattern = r'^\s*(fig)\S*'
    
    # Vérifie si la chaîne commence par "fig" (insensible à la casse)
    if re.match(pattern, text, re.IGNORECASE):
        return True
    return False

def identify_ref_block(text):
    # Expression régulière pour vérifier si le texte commence par "fig" (insensible à la casse)
    pattern = r'^\s*ref.*'
    
    # Vérifie si la chaîne commence par "fig" (insensible à la casse)
    if re.match(pattern, text, re.IGNORECASE):
        return True
    return False

def identify_pattern_block(text, pattern):
    
    
    # Vérifie si la chaîne commence par "fig" (insensible à la casse)
    if re.match(pattern, text, re.IGNORECASE):
        return True
    return False


def clean_text(text):
    # Supprimer les numéros au début du texte (comme I.a, 1.a, 2.a, III.a, etc.)
    # Cela inclut également les numérotations mixtes avec des chiffres et des lettres
    text = re.sub(r'^\s*[\dIVXLCDM]+\.[\da-zA-Z]+[\.\)]*\s*', '', text)  # Numéros de type 1.a, I.a, 1.1, etc.
    
    # Garder seulement les lettres et les espaces, ignorer la ponctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Mettre en minuscules et supprimer les espaces superflus
    text = text.lower().strip()
    
    return text


def scan_text_boxes(self, page):
    if not hasattr(self, 'Block_list'): self.Block_list = []

    blocks = page.get_text("dict")["blocks"]
    rect = page.rect
    image_width = rect.width
    image_height = rect.height

    limit = 0.08

    self.header_margin = int(image_height * limit)
    self.footer_margin = int(image_height * (1-limit))
    self.left_margin   = int(image_width  * limit)
    self.right_margin  = int(image_width  * (1-limit))

    threshold = 0.1  # Adjust this threshold as necessary (e.g., 0.5 for 50% non-letters)

    for idx, block_data in enumerate(blocks):
        bbox = block_data["bbox"]
        block_type_original = block_data['type']
        x0, y0, x1, y1 = bbox

        # Arrondir les variables a 1 chiffre apres la virgule
        x0 = round(x0, 1)
        y0 = round(y0, 1)
        x1 = round(x1, 1)
        y1 = round(y1, 1)

        block_text = extract_text_from_block(block_data)

        if is_outside_margin(y0, y1, self.header_margin, self.footer_margin) or is_outside_margin(x0, x1, self.left_margin, self.right_margin):
            block_type = 'margin'
        else:
            total_chars = len(block_text)
            non_letter_chars = len(re.findall(r'[^a-zA-Z0-9\s.,;:?!\'"()\--]', block_text))  # Count non-letter characters
            ratio = non_letter_chars / total_chars if total_chars > 0 else 0


            if block_type_original == 1:
                block_type = 'figure'

            else:
                if ratio < threshold:
                    block_type = 'text'
                    
                else:
                    block_type = 'equation'
            
        if self.outline_list == [] : 
            outline_level = -1
            outline_idx = None
        else:

            """Vérifie si le texte donné est dans la liste d'outlines."""
            for idx_outline, outline in enumerate(self.outline_list):
                
                # Garde seulement les lettres (majuscule et minuscule)
                
                outline_title_clean = clean_text(outline.title)  # Idem pour le titre de l'outline
                block_text_clean = clean_text(block_text)

                if len(block_text_clean) > len(outline_title_clean):
                    block_text_clean = block_text_clean[:len(outline_title_clean)]

                # On ne garde uniquement les parties textes, il est possible que les outlines n'ont pas les I.1., 2.a)...
                # On garde alors que les derniers éléments de notre texte 
                # = block_text_clean[5:] #on ignore les première cases qui peuvent être le numéro de titre
                #outline_title_clean = outline_title_clean[5:]

                #if block_text_clean == outline_title_clean:
                if identify_pattern_block(block_text_clean, r'.*'+ outline_title_clean + r'.*'):
                # Comparaison insensible à la casse
                    
                    print(f"Block test :\"{block_text_clean} \" comparé à \" {outline_title_clean} \"")
                    outline_level = outline.level
                    outline_idx = idx_outline
                    break
                else:
                    outline_idx = None
                    outline_level = -1
            
        # Create a Block object and append to Block_list
        self.Block_list.append(Block_class(block_type, (x0, y0, x1, y1), block_text, page.number, -1, -1, outline_level, outline_idx))

        


def merge_consecutive_overlapping_identical_type_blocks(self):
    i_max = len(self.Block_list)
    i = 1
    if i_max > 1:
        while i < i_max:
            block = self.Block_list[i]
            previous_block = self.Block_list[i-1]
            
            # Vérifier si les deux blocs consécutifs sont du même type et se chevauchent
            if block.type == previous_block.type and do_frames_overlap(previous_block.position, block.position, margin = 2):
                # Fusionner les blocs
                merged_position = merge_positions(previous_block.position, block.position)
                previous_block.position = merged_position
                previous_block.text += " " + block.text  # Ajouter le contenu du bloc actuel à l'ancien
                self.Block_list.pop(i)  # Supprimer le bloc actuel de la liste
                i_max -= 1 # La taille de la liste diminue de 1 élément
                continue
            i += 1
            

def tag_block(self, block_type):
    from Page_manager import redraw_page


    print('entering tag block')
    print(self.selected_rect_ids)
    
    try:
        if self.selected_rect_ids:
            for ids in self.selected_rect_ids:
                self.Block_list[ids].type = block_type
                print(f"Block {ids} tagged as {block_type}.")
            self.selected_rect_ids = []

        elif self.block_idx is not None:
            self.Block_list[self.block_idx].type = block_type
            print(f"Block {self.block_idx} tagged as {block_type}.")

        redraw_page(self)
        Update_historic(self)
        
    
    except Exception as e:
        print(f"An error occurred: {e}")


def extract_text_from_block(block):
    if "lines" in block:
        block_text = ""
        for line in block["lines"]:
            for span in line["spans"]:
                block_text += span["text"]
        return block_text.strip()
    else:
        return ""
    

def extract_text(self,text="texte de test", folder_path = None):
    """
    Extrait du texte, le sauvegarde dans un fichier texte dans un dossier spécifique, puis l'ouvre.

    :param text: Le texte à écrire dans le fichier.
    :param folder_path: Le dossier où sauvegarder le fichier.
    :param file_name: Le nom du fichier texte à créer.
    """
    file_name = "extracted_text.txt"

    if folder_path  is None:
        folder_path =os.path.join(self.script_path, "Var")
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Crée le dossier s'il n'existe pas
    
    file_path = os.path.join(folder_path,file_name)
    
    # Variable pour stocker le texte extrait
    extracted_text = ""
   
   
    for block in self.Block_list:
        if block.type == 'text':
            # Calculer l'indentation en fonction de outline_level
            indentation = "    " * max(0, block.outline_level)  # 4 espaces par niveau
            if block.outline_level > 0: 
                extracted_text = extracted_text + "\n"

            # Vérifier si block.text est une liste et le convertir en chaîne de caractères si nécessaire
            if isinstance(block.text, list):
                block_text = " ".join([str(item) for item in block.text])  # Joindre les éléments de la liste en une chaîne
            else:
                block_text = str(block.text)  # S'assurer que c'est une chaîne de caractères

            # Écrire le texte dans le fichier
            extracted_text = extracted_text + f"{indentation}{block_text.strip()}\n"
            
            if block.outline_level > 0: 
                extracted_text = extracted_text + "\n"

    # Créer et écrire dans le fichier texte
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(extracted_text)

    """
    try:
        os.startfile(file_path)  # Windows uniquement
    except AttributeError:
        print(f"Veuillez ouvrir le fichier manuellement : {file_path}")"""

    
    analyse_LLM(extracted_text)

    # Exemple d'utilisation
    #extracted_text = "Voici le texte extrait d'un PDF."
    #extract_text(extracted_text)



