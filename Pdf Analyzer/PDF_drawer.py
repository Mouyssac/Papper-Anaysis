from Text_manager import *
import tkinter as tk
from tkinter import ttk
from Tools import is_contained
import threading





def analyse_pdf(self):
    from Page_manager import redraw_page

    self.analysis_canceled = False  # Variable de controle pour l'annulation

    def run_analysis():
        print('Analysing document:')
        scan_outlines(self)
        print(self.outline_list)

        for page_num in range(0, self.doc.page_count):
            if self.analysis_canceled:
                print("Analysis canceled.")
                break

            #try:
            page = self.doc.load_page(page_num)
            scan_text_boxes(self, page)
            scan_hypertext(self,page)         

            print(f'page {page_num + 1} / {self.doc.page_count}')
            progress_value = round((page_num + 1) / self.doc.page_count * 100)
            progress_bar['value'] = progress_value
            label_progress_bar.config(text=f"Analysing page : {page_num + 1} / {self.doc.page_count}")
            progress_bar_window.update_idletasks()

            #except Exception as e:
            #    print(f"Error loading page {page_num + 1}: {str(e)}")

        merge_consecutive_overlapping_identical_type_blocks(self)

        # Identify legend under figures
        for block in self.Block_list:
            if identify_figure_block(block.text): # Si le bloc text commence par fig., le bloc est assimilé à une légende de figure
                block.type = 'legend'

        # Identify all block in the reference part
        in_ref_part = False
        for block in self.Block_list:
            if block.outline_idx is not None:
                # Si le block est dans les outlinesj, prendre tout jusqu'a la prochaine outline
                if identify_ref_block(block.text): # Si le bloc text commence par ref. c'est le début de la partie référence
                    in_ref_part = True
                else:
                    in_ref_part = False
                
            if in_ref_part:
                if block.type == 'text':
                    block.type = 'sources'


        if not self.analysis_canceled:
            for idx, block in enumerate(self.Block_list):
                self.Block_list[idx].idx = idx
                self.Block_list[idx].original_idx = idx

            self.original_Block_list = self.Block_list.copy()
            self.already_analysed = True
            self.btn_analyse.config(state='disabled')

            Update_historic(self)


            redraw_page(self)

            progress_bar_window.destroy()

            # Désactivation du bouton après un certain événement
            self.btn_extract_text.config(state="enabled")

    def on_close():
        self.analysis_canceled = True
        progress_bar_window.destroy()

    # Create a window
    progress_bar_window = tk.Tk()
    progress_bar_window.title("Analysing document")
    progress_bar_window.geometry("300x100")
    progress_bar_window.protocol("WM_DELETE_WINDOW", on_close)

    # Create a label
    label_progress_bar = ttk.Label(progress_bar_window, text="Progress:")
    label_progress_bar.pack(pady=10)

    # Create a progress bar
    progress_bar = ttk.Progressbar(progress_bar_window, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=10)

    # Start the analysis in a separate thread
    analysis_thread = threading.Thread(target=run_analysis)
    analysis_thread.start()

    # Run the Tkinter event loop
    progress_bar_window.mainloop()


def draw_hypertext_boxes(self, hypertext_list):
    self.canvas.delete("hypertext")

    for hypertext in hypertext_list:

            x0 = hypertext.bbox[0]*self.scale
            x1 = hypertext.bbox[1]*self.scale
            x2 = hypertext.bbox[2]*self.scale
            x3 = hypertext.bbox[3]*self.scale
            self.canvas.create_rectangle(x0, x1, x2, x3, outline='#9370DB', width=1, tags="hypertext")




def draw_text_boxes(self, Block_list):
    self.canvas.delete("rect")
    self.text_boxes = []

    for block in Block_list:
        x0, y0, x1, y1 = block.position
        x0 *= self.scale
        y0 *= self.scale
        x1 *= self.scale
        y1 *= self.scale

        if self.show_red_boxes_var.get() and block.type == 'text':
            rect_color = 'red'
               
        elif self.show_red_boxes_var.get() and block.type == 'title':
            rect_color = '#8B0000'


        elif self.show_red_boxes_var.get() and block.type == 'authors':
            rect_color = '#FFCCCC'


        elif self.show_red_boxes_var.get() and block.type == 'sources':
            rect_color = '#FF8C00'

        elif self.show_purple_boxes_var.get() and block.type == 'legend':
            rect_color = '#FF1493'

        elif self.show_purple_boxes_var.get() and block.type == 'margin':
            rect_color = 'purple'

        elif self.show_blue_boxes_var.get() and block.type == 'equation':
            rect_color = '#87CEEB'

        elif self.show_blue_boxes_var.get() and block.type == 'figure':
            rect_color = '#28a745'

        elif self.show_blue_boxes_var.get() and block.type == 'off':
            rect_color = 'black'

        else:
            continue

        rect = self.canvas.create_rectangle(x0, y0, x1, y1, outline=rect_color, width=1, tags="rect")
        self.rect_colors[rect] = rect_color
        self.text_boxes.append(rect)
    

def draw_green_frames(self):

        # Function to check if two rectangles intersect
    def rectangles_intersect(bloc1, block2):
        return not (bloc1.position[2] < block2.position[0] or bloc1.position[0] > block2.position[2] or bloc1.position[3] < block2.position[1] or bloc1.position[1] > block2.position[3])

    self.canvas.delete("green_frame")
    if not self.show_green_boxes_var.get():
        return

    tolerance = 30  # Tolerance for matching sides
    margin = 4  # Margin for the green frame around the grouped blocks
    containment_tolerance = 100  # Tolerance for containment check
    vertical_gap_tolerance = 100
    horizontal_gap_tolerance = 10

    page_blocks = [block for block in self.Block_list if block.page == self.current_page]

    grouped_blocks = []
    used_blocks = set()

    for i, block1 in enumerate(page_blocks):
        x0_1, y0_1, x1_1, y1_1 = block1.position
        if not is_outside_margin(y0_1, y1_1, self.header_margin, self.footer_margin):
            if i in used_blocks:
                continue
            group = [block1]
            for j, block2 in enumerate(page_blocks[i + 1:], start=i + 1):
                x0_2, y0_2, x1_2, y1_2 = block2.position
                if not is_outside_margin(y0_2, y1_2, self.header_margin, self.footer_margin):
                    if j in used_blocks:
                        continue
                    if (((abs(x0_1 - x0_2) <= tolerance or abs(x1_1 - x1_2) <= tolerance)  # check if two blocks are alined
                            and abs(y0_1-y0_2) < vertical_gap_tolerance)):                      # check the vertical gap between two blocks       
                        
                        group.append(block2)
                        used_blocks.add(j)
            if len(group) > 0:
                grouped_blocks.append(group)
                used_blocks.add(i)

    frames = []

    for group in grouped_blocks:
        x0 = min(block.position[0] for block in group) - margin
        y0 = min(block.position[1] for block in group) - margin
        x1 = max(block.position[2] for block in group) + margin
        y1 = max(block.position[3] for block in group) + margin
        frames.append((x0, y0, x1, y1))

    filtered_frames = []
    for i, frame1 in enumerate(frames):
        contained = False
        for j, frame2 in enumerate(frames):
            if i != j and is_contained(frame1, frame2, containment_tolerance):
                contained = True
                break
        if not contained:
            filtered_frames.append(frame1)

    for frame in filtered_frames:
        x0, y0, x1, y1 = frame
        self.canvas.create_rectangle(x0 * self.scale, y0 * self.scale, x1 * self.scale, y1 * self.scale,
                                        outline="green", width=2, tags="green_frame")   
            
        




   