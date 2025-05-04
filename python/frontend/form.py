import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import search

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DICOMForm(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DICOM Patient and Study Information")
        self.geometry("1400x800")
        self.minsize(1400, 800)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.original_image = None
        self.preview_image = None

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.form_frame = ctk.CTkFrame(self.main_frame, width=1600)
        self.form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.form_frame.grid_rowconfigure(0, weight=1)

        self.nav_button = ctk.CTkButton(self.form_frame, text="Go to Search", command=self.open_search)
        self.nav_button.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 10))

        self.patient_frame = ctk.CTkFrame(self.form_frame, corner_radius=10)
        self.patient_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.patient_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.patient_frame, text="Patient Information", font=("Verdana", 16)).grid(column=0, row=0, columnspan=2, pady=(10, 10))

        self.add_label_entry(self.patient_frame, "Name:", 1)
        self.add_label_entry(self.patient_frame, "Patient ID:", 2)
        self.birthdate = self.add_label_date(self.patient_frame, "Birthdate:", 3)
        self.sex = self.add_label_option(self.patient_frame, "Sex:", ["Male", "Female", "Other"], 4)
        self.add_label_entry(self.patient_frame, "Size (cm):", 5)
        self.add_label_entry(self.patient_frame, "Weight (kg):", 6)
        self.add_label_entry(self.patient_frame, "Address:", 7)
        self.add_label_entry(self.patient_frame, "Phone:", 8)

        self.study_frame = ctk.CTkFrame(self.form_frame, corner_radius=10)
        self.study_frame.grid(row=2, column=0, sticky="nsew", pady=(20, 10), padx=10, ipadx=10, ipady=10)
        self.study_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.study_frame, text="Study Information", font=("Verdana", 16)).grid(column=0, row=0, columnspan=2, pady=(10, 10))

        self.study_date = self.add_label_date(self.study_frame, "Study Date:", 1)
        self.study_time = self.add_label_entry(self.study_frame, "Study Time:", 2)
        self.add_label_entry(self.study_frame, "Study ID:", 3)
        self.add_label_entry(self.study_frame, "Series Number:", 4)
        self.add_label_entry(self.study_frame, "Accession Number:", 5)

        self.submit_button = ctk.CTkButton(self.form_frame, text="Submit", corner_radius=10, command=self.submit)
        self.submit_button.grid(row=3, column=0, pady=10)

        self.image_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, width=500)
        self.image_frame.grid(row=0, column=1, sticky="nsew")
        self.image_frame.grid_rowconfigure(1, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.image_frame, text="No image uploaded", width=200, height=200)
        self.image_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.upload_button = ctk.CTkButton(self.image_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(row=2, column=0, pady=10)

    def add_label_entry(self, frame, label_text, row):
        ctk.CTkLabel(frame, text=label_text, font=("Verdana", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = ctk.CTkEntry(frame, corner_radius=10)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        return entry

    def add_label_option(self, frame, label_text, options, row):
        ctk.CTkLabel(frame, text=label_text, font=("Verdana", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        option_menu = ctk.CTkOptionMenu(frame, values=options, corner_radius=10)
        option_menu.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        option_menu.set("Select")
        return option_menu

    def add_label_date(self, frame, label_text, row):
        ctk.CTkLabel(frame, text=label_text, font=("Verdana", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        date_entry = ctk.CTkEntry(frame, placeholder_text="dd/mm/yyyy", corner_radius=10)
        date_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        return date_entry

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.original_image = Image.open(file_path)
            max_width, max_height = 800, 800

            original_width, original_height = self.original_image.size
            scale = min(max_width / original_width, max_height / original_height)

            new_size = (int(original_width * scale), int(original_height * scale))
            resized_image = self.original_image.resize(new_size)

            self.preview_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=new_size)
            self.image_label.configure(image=self.preview_image, text="")

    def open_search(self):
        self.withdraw()
        self.search_window = search.SearchWindow(master=self)
        self.search_window.mainloop()

    def submit(self):
        print("Form submitted! It’s alive... IT’S ALIIIIIVE!")

if __name__ == "__main__":
    app = DICOMForm()
    app.mainloop()
