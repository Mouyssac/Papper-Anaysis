import fitz
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class PDFViewerApp:
    def __init__(self, master, pdf_path):
        self.master = master
        self.master.title("PDF Viewer")
        self.pdf_path = pdf_path
        self.doc = fitz.open(self.pdf_path)
        self.current_page = 0

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        self.scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.page_label = ttk.Label(self.master, text=f"Page {self.current_page + 1}/{len(self.doc)}", font=("Helvetica", 12))
        self.page_label.pack()

        self.btn_prev = ttk.Button(self.master, text="Previous", command=self.show_prev_page)
        self.btn_prev.pack(side=tk.TOP, padx=10)

        self.btn_next = ttk.Button(self.master, text="Next", command=self.show_next_page)
        self.btn_next.pack(side=tk.TOP, padx=10)

        self.show_page(self.current_page)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Motion>", self.on_mouse_motion)

        self.current_hovered_rect = None
        self.blocks_data = []
        self.rect_colors = {}  # Store the initial color of each rectangle

    def on_canvas_resize(self, event):
        self.show_page(self.current_page)

    def on_mouse_motion(self, event):
        if self.current_hovered_rect:
            # Restore the original color of the rectangle
            original_color = self.rect_colors[self.current_hovered_rect]
            self.canvas.itemconfigure(self.current_hovered_rect, outline=original_color)

        x, y = event.x, event.y
        items = self.canvas.find_withtag("rect")

        for item in items:
            bbox = self.canvas.bbox(item)
            if bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]:
                self.canvas.itemconfigure(item, outline="yellow")
                self.current_hovered_rect = item
                return

        self.current_hovered_rect = None

    def show_page(self, page_num):
        #try:
        page = self.doc.load_page(page_num)
        pix = page.get_pixmap()

        # Check image dimensions
        if pix.width <= 0 or pix.height <= 0:
            print(f"Invalid image dimensions for page {page_num + 1}: width={pix.width}, height={pix.height}")
            return

        # Determine canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate image size to fit canvas, preserving aspect ratio
        image_width = pix.width
        image_height = pix.height

        # Scale image to fit within canvas dimensions
        scale_x = canvas_width / image_width
        scale_y = canvas_height / image_height
        scale = min(scale_x, scale_y)

        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        self.img_tk = ImageTk.PhotoImage(img)

        # Clear canvas and display new image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        # Draw text boxes
        self.draw_text_boxes(page, scale)

        # Update page label
        self.page_label.config(text=f"Page {page_num + 1}/{len(self.doc)}")
        self.current_page = page_num

        #except Exception as e:
        #    print(f"Error loading page {page_num + 1}: {str(e)}")

     def draw_text_boxes(self, page, scale, page_height):
        blocks = page.get_text("dict")["blocks"]
        self.blocks_data = blocks
        self.text_boxes = []

        header_margin = int(page_height * 0.08)  # Define header margin (10% of page height)
        footer_margin = int(page_height * 0.92)  # Define footer margin (90% of page height)

        for idx, block in enumerate(blocks):
            bbox = block["bbox"]
            x0, y0, x1, y1 = bbox
            x0, y0, x1, y1 = int(x0 * scale), int(y0 * scale), int(x1 * scale), int(y1 * scale)

            # Determine the color based on position
            if y1 <= header_margin:
                outline_color = "purple"  # Header
            elif y0 >= footer_margin:
                outline_color = "purple"  # Footer
            else:
                outline_color = "red"  # Regular text block

            rect = self.canvas.create_rectangle(x0, y0, x1, y1, outline=outline_color, width=2, tags="rect")
            self.rect_colors[rect] = outline_color  # Store the original color
            self.text_boxes.append(rect)

            # Create a transparent rectangle to capture clicks
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="", fill="", tags=("rect_click", f"block{idx}"))
            self.canvas.tag_bind(f"block{idx}", "<Button-1>", lambda event, idx=idx: self.show_block_info(idx))


    def show_block_info(self, block_index):
        block = self.blocks_data[block_index]
        block_text = ""
        for line in block["lines"]:
            for span in line["spans"]:
                block_text += span["text"] + " "
            block_text += "\n"
        bbox = block["bbox"]
        print(f"Clicked on block number {block_index + 1}")
        print(f"Text: {block_text}")
        print(f"Position: {bbox}")

    def show_prev_page(self):
        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def show_next_page(self):
        if self.current_page < len(self.doc) - 1:
            self.show_page(self.current_page + 1)

    def close_pdf(self):
        self.doc.close()
        self.master.destroy()

def main():
    pdf_path = "C:\\Users\\maxim\\Desktop\\Biblio doctorat\\Article.pdf"

    root = tk.Tk()
    app = PDFViewerApp(root, pdf_path)

    # Set initial size of the window to match the PDF dimensions
    page = app.doc.load_page(0)
    pix = page.get_pixmap()
    
    # Calculate the width of the scrollbar
    scrollbar_width = 20  # Adjust this value as needed
    
    # Set the geometry of the window
    root.geometry(f"{pix.width + scrollbar_width}x{pix.height + 100}")

    root.mainloop()

if __name__ == "__main__":
    main()
