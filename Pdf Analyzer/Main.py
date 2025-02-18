from PDFViewerApp import *
 
def main():
    root = tk.Tk()
    app = PDFViewerApp(root)
    root.geometry(f"{1050}x{800}")
    root.protocol("WM_DELETE_WINDOW", app.close_pdf)
    root.mainloop()

if __name__ == "__main__":
    main()    