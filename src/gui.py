import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os
import subprocess
import threading

class AugmentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Augmentation Tool")

        # Load and resize images
        self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'icon.png')
        self.logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'logo.png')

        self.icon = ImageTk.PhotoImage(Image.open(self.icon_path))
        self.logo = Image.open(self.logo_path)
        self.logo = self.logo.resize((200, 50), Image.LANCZOS)  # Resize the logo
        self.logo = ImageTk.PhotoImage(self.logo)

        # Set application icon
        self.root.iconphoto(False, self.icon)

        self.create_widgets()

    def create_widgets(self):
        # Configure grid to be responsive
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.rowconfigure(8, weight=1)

        # Title label
        self.title_label = ttk.Label(self.root, text="Image Augmentation Tool", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="N")

        # Logo display
        self.logo_label = ttk.Label(self.root, image=self.logo)
        self.logo_label.grid(row=0, column=3, padx=10, pady=10, sticky="NE")

        # Input directory selection
        self.input_label = ttk.Label(self.root, text="Select Project Directory:")
        self.input_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        self.input_entry = ttk.Entry(self.root, width=50)
        self.input_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="EW")

        self.browse_button = ttk.Button(self.root, text="Browse", command=self.browse_input)
        self.browse_button.grid(row=1, column=3, padx=10, pady=10, sticky="W")

        # Augmentation mode selection
        self.mode_label = ttk.Label(self.root, text="Select Augmentation Mode:")
        self.mode_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        self.mode_var = tk.StringVar(value="automatic")
        self.manual_radio = ttk.Radiobutton(self.root, text="Manual", variable=self.mode_var, value="manual", command=self.update_entries)
        self.manual_radio.grid(row=2, column=1, padx=10, pady=5, sticky="W")
        self.automatic_radio = ttk.Radiobutton(self.root, text="Automatic", variable=self.mode_var, value="automatic", command=self.update_entries)
        self.automatic_radio.grid(row=2, column=2, padx=10, pady=5, sticky="W")

        # Augmentation options
        self.augmentations_label = ttk.Label(self.root, text="Select Augmentations:")
        self.augmentations_label.grid(row=3, column=0, padx=10, pady=10, sticky="W")

        self.brightness_var = tk.BooleanVar()
        self.contrast_var = tk.BooleanVar()
        self.flip_var = tk.BooleanVar()
        self.rotate_var = tk.BooleanVar()
        self.distortion_var = tk.BooleanVar()

        self.brightness_check = ttk.Checkbutton(self.root, text="Brightness (0.7-1.1)", variable=self.brightness_var, command=self.update_entries)
        self.brightness_check.grid(row=4, column=0, padx=10, pady=5, sticky="W")
        self.brightness_entry = ttk.Entry(self.root, width=10)

        self.flip_check = ttk.Checkbutton(self.root, text="Flip (0 or 1)", variable=self.flip_var, command=self.update_entries)
        self.flip_check.grid(row=5, column=0, padx=10, pady=5, sticky="W")
        self.flip_entry = ttk.Entry(self.root, width=10)

        self.distortion_check = ttk.Checkbutton(self.root, text="Distortion (Minimal)", variable=self.distortion_var, command=self.update_entries)
        self.distortion_check.grid(row=6, column=0, padx=10, pady=5, sticky="W")
        self.distortion_entry = ttk.Entry(self.root, width=10)

        self.contrast_check = ttk.Checkbutton(self.root, text="Contrast (0.8-1.1)", variable=self.contrast_var, command=self.update_entries)
        self.contrast_check.grid(row=4, column=2, padx=10, pady=5, sticky="W")
        self.contrast_entry = ttk.Entry(self.root, width=10)

        self.rotate_check = ttk.Checkbutton(self.root, text="Rotate (-30 to 30)", variable=self.rotate_var, command=self.update_entries)
        self.rotate_check.grid(row=5, column=2, padx=10, pady=5, sticky="W")
        self.rotate_entry = ttk.Entry(self.root, width=10)

        # Start button
        self.start_button = ttk.Button(self.root, text="Start Augmentation", command=self.start_augmentation)
        self.start_button.grid(row=7, column=0, columnspan=4, pady=20)

        # Log text area
        self.log_text = ScrolledText(self.root, width=80, height=20, state=tk.DISABLED)
        self.log_text.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="NSEW")

    def browse_input(self):
        input_directory = filedialog.askdirectory()
        if input_directory:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_directory)

    def update_entries(self):
        mode = self.mode_var.get()

        if mode == 'manual':
            self.brightness_entry.grid(row=4, column=1, padx=10, pady=5, sticky="W")
            self.flip_entry.grid(row=5, column=1, padx=10, pady=5, sticky="W")
            self.distortion_entry.grid(row=6, column=1, padx=10, pady=5, sticky="W")
            self.contrast_entry.grid(row=4, column=3, padx=10, pady=5, sticky="W")
            self.rotate_entry.grid(row=5, column=3, padx=10, pady=5, sticky="W")
        else:
            self.brightness_entry.grid_forget()
            self.flip_entry.grid_forget()
            self.distortion_entry.grid_forget()
            self.contrast_entry.grid_forget()
            self.rotate_entry.grid_forget()

    def start_augmentation(self):
        input_directory = self.input_entry.get()
        if not input_directory:
            messagebox.showerror("Error", "Please select an input directory.")
            return

        mode = self.mode_var.get()
        augmentations = []
        if self.brightness_var.get():
            if mode == 'manual':
                threshold = self.brightness_entry.get()
                augmentations.append(f"brightness:{threshold}")
            else:
                augmentations.append("brightness")
        if self.flip_var.get():
            if mode == 'manual':
                threshold = self.flip_entry.get()
                augmentations.append(f"flip:{threshold}")
            else:
                augmentations.append("flip")
        if self.distortion_var.get():
            if mode == 'manual':
                threshold = self.distortion_entry.get()
                augmentations.append(f"distortion:{threshold}")
            else:
                augmentations.append("distortion")
        if self.contrast_var.get():
            if mode == 'manual':
                threshold = self.contrast_entry.get()
                augmentations.append(f"contrast:{threshold}")
            else:
                augmentations.append("contrast")
        if self.rotate_var.get():
            if mode == 'manual':
                threshold = self.rotate_entry.get()
                augmentations.append(f"rotate:{threshold}")
            else:
                augmentations.append("rotate")

        if not augmentations:
            messagebox.showerror("Error", "Please select at least one augmentation.")
            return

        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'scripts', 'augment.py')
        
        command = ['python', script_path, mode, *augmentations]
        
        # Start the augmentation in a separate thread to avoid blocking the GUI
        threading.Thread(target=self.run_augmentation, args=(command,)).start()

    def run_augmentation(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        while True:
            output = process.stdout.readline()
            if output:
                self.log_message(output)
            if process.poll() is not None:
                break
        
        # Capture any remaining output
        for output in process.stdout.readlines():
            self.log_message(output)
        for error in process.stderr.readlines():
            self.log_message(error)
        
        messagebox.showinfo("Success", "Augmentation completed successfully.")
        
    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message)
        self.log_text.yview(tk.END)
        self.log_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AugmentationApp(root)
    root.mainloop()
