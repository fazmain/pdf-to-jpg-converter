import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf2image import convert_from_path
from PIL import Image
from threading import Thread

def convert_pdf_to_jpg(pdf_path, save_path, pages, progress, update_status):
    """ Convert the given PDF to JPG and save to the specified path """
    try:
        if pages:
            pages_to_convert = [int(p) - 1 for p in pages.split(',') if p.isdigit()]  # Convert to 0-based index
        else:
            pages_to_convert = None  # Convert all pages

        images = convert_from_path(pdf_path, first_page=min(pages_to_convert)+1, last_page=max(pages_to_convert)+1) if pages_to_convert else convert_from_path(pdf_path)
        total = len(images)
        for i, image in enumerate(images):
            if pages_to_convert and i not in pages_to_convert:
                continue  # Skip pages not in the specified range
            image_path = os.path.join(save_path, f"output_{i+1}.jpg")  # Page numbers are 1-based in file names
            image.save(image_path, 'JPEG')
            progress['value'] = (i + 1) / total * 100
            root.update_idletasks()
        update_status("Conversion Completed Successfully!")
    except Exception as e:
        update_status(f"Error: {e}")

def start_conversion(pdf_path_var, save_path_var, pages_var, progress, status_label):
    """ Start the conversion process """
    if pdf_path_var.get() and save_path_var.get():
        status_label.config(text="Converting...")
        Thread(target=convert_pdf_to_jpg, args=(pdf_path_var.get(), save_path_var.get(), pages_var.get(), progress, lambda status: status_label.config(text=status))).start()
    else:
        messagebox.showwarning("Warning", "Please select a file and a save path.")

def select_pdf(pdf_path_var):
    """ Select a PDF file """
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_path_var.set(file_path)

def select_save_path(save_path_var):
    """ Select a path to save the converted files """
    path = filedialog.askdirectory()
    if path:
        save_path_var.set(path)

def main():
    global root
    root = tk.Tk()
    root.title("PDF to JPG Converter")
    root.geometry('400x300')  # Set window size

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    pdf_path_var = tk.StringVar()
    save_path_var = tk.StringVar()
    pages_var = tk.StringVar()

    upload_button = tk.Button(frame, text="Upload PDF", command=lambda: select_pdf(pdf_path_var))
    upload_button.pack(side=tk.TOP, fill=tk.X)

    save_path_button = tk.Button(frame, text="Select Save Path", command=lambda: select_save_path(save_path_var))
    save_path_button.pack(side=tk.TOP, fill=tk.X, pady=5)

    pages_label = tk.Label(frame, text="Enter Pages (e.g., 1,3-5,7):")
    pages_label.pack(side=tk.TOP, fill=tk.X)

    pages_entry = tk.Entry(frame, textvariable=pages_var)
    pages_entry.pack(side=tk.TOP, fill=tk.X, pady=5)

    convert_button = tk.Button(frame, text="Start Conversion", command=lambda: start_conversion(pdf_path_var, save_path_var, pages_var, progress_bar, status_label))
    convert_button.pack(side=tk.TOP, fill=tk.X, pady=5)

    progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
    progress_bar.pack(side=tk.TOP, fill=tk.X, pady=5)

    status_label = tk.Label(frame, text="Ready", fg="white")
    status_label.pack(side=tk.TOP, fill=tk.X, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
