# search.py
import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SearchWindow(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        self.title("Search")
        self.geometry("1400x800")
        self.minsize(1400, 800)
        self.master = master

        self.selected_patient_id = None

        # === MOCK BACKEND DATA ===
        self.mock_patients = {
            "erik": {
                "name": "Erik",
                "id": "111",
                "birthdate": "Monday, August 3, 2009",
                "sex": "M",
                "studies": [
                    {
                        "StudyDate": "Saturday, May 3, 2025",
                        "AccessionNumber": "",
                        "StudyInstanceUID": "1.2.826.0.1.3680043.8.498.698306395085431683210748209704311008",
                        "StudyID": "STUDY_001",
                        "Status": "Unknown",
                        "Modality": "OT",
                        "SeriesInstanceUID": "1.2.826.0.1.3680043.8.498.10055149824286693553303198047467153629",
                        "SeriesNumber": "1"
                    }
                ]
            },
            "anne": {
                "name": "Anne",
                "id": "222",
                "birthdate": "Wednesday, July 14, 2010",
                "sex": "F",
                "studies": [
                    {
                        "StudyDate": "Tuesday, April 2, 2024",
                        "AccessionNumber": "",
                        "StudyInstanceUID": "1.2.826.0.1.3680043.8.498.568306395094383321748209704311111",
                        "StudyID": "STUDY_A1",
                        "Status": "Completed",
                        "Modality": "CT",
                        "SeriesInstanceUID": "1.2.826.0.1.3680043.8.498.200000000000001",
                        "SeriesNumber": "1"
                    },
                    {
                        "StudyDate": "Friday, March 15, 2024",
                        "AccessionNumber": "",
                        "StudyInstanceUID": "1.2.826.0.1.3680043.8.498.568306395094383321748209704311112",
                        "StudyID": "STUDY_A2",
                        "Status": "In Progress",
                        "Modality": "MR",
                        "SeriesInstanceUID": "1.2.826.0.1.3680043.8.498.200000000000002",
                        "SeriesNumber": "2"
                    }
                ]
            }
        }

        # === NAVBAR ===
        nav_bar = ctk.CTkFrame(self, height=50)
        nav_bar.pack(fill="x", side="top")
        back_button = ctk.CTkButton(nav_bar, text="Back to Form", command=self.back_to_form)
        back_button.pack(side="left", padx=20, pady=10)

        # === SEARCH BAR ===
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", padx=20, pady=(10, 5))

        self.search_dropdown = ctk.CTkOptionMenu(self.search_frame, values=["Erik", "Anne"])
        self.search_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_button = ctk.CTkButton(self.search_frame, text="Search", command=self.search_patient)
        self.search_button.pack(side="left")

        # === MAIN PANEL LAYOUT ===
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=3)

        # === LEFT PANEL ===
        self.left_panel = ctk.CTkFrame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # === RIGHT PANEL ===
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self.title_label = ctk.CTkLabel(self.right_panel, text="Studies on selected patient", font=("Verdana", 20, "bold"))
        self.title_label.pack(anchor="w", padx=10, pady=(10, 20))

        self.study_container = ctk.CTkFrame(self.right_panel)
        self.study_container.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_patient_and_studies(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        for widget in self.study_container.winfo_children():
            widget.destroy()
        self.selected_patient_id = None

    def search_patient(self):
        selected = self.search_dropdown.get().strip().lower()
        if selected in self.mock_patients:
            patient = self.mock_patients[selected]
            if patient["id"] != self.selected_patient_id:
                self.clear_patient_and_studies()
                self.selected_patient_id = patient["id"]
                self.display_patient_info(patient)
                for study in patient["studies"]:
                    self.create_study_card(study)

    def display_patient_info(self, patient):
        frame = ctk.CTkFrame(self.left_panel, fg_color="#2980b9", corner_radius=10)
        frame.pack(fill="x", pady=10)

        ctk.CTkLabel(frame, text="Patient information", font=("Verdana", 14, "bold"), fg_color="#2980b9",
                     text_color="white", corner_radius=0, height=30).pack(fill="x")

        ctk.CTkLabel(frame, text=patient["name"], font=("Verdana", 16, "bold"), text_color="white").pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(frame, text=f"PatientID: {patient['id']}", font=("Verdana", 12), text_color="white").pack(anchor="w", padx=20)
        ctk.CTkLabel(frame, text=f"PatientBirthDate: {patient['birthdate']}", font=("Verdana", 12), text_color="white").pack(anchor="w", padx=20)
        ctk.CTkLabel(frame, text=f"PatientSex: {patient['sex']}", font=("Verdana", 12), text_color="white").pack(anchor="w", padx=20, pady=(0, 10))

    def create_study_card(self, study):
        card = ctk.CTkFrame(self.study_container, corner_radius=10)
        card.pack(fill="x", pady=10)

        header = ctk.CTkLabel(
            card, text=study["StudyDate"], font=("Verdana", 14, "bold"),
            fg_color="#2980b9", text_color="white", corner_radius=10, height=30
        )
        header.pack(fill="x", padx=0, pady=(0, 5))

        body = ctk.CTkLabel(card, anchor="w", justify="left", font=("Verdana", 12))
        body.pack(fill="x", padx=10, pady=(10, 0))

        plot_button = ctk.CTkButton(card, text="Show plot", width=100)
        plot_button.pack(anchor="e", padx=10, pady=(5, 10))

        def set_summary():
            body.configure(
                text=f"StudyDate: {study['StudyDate']}\n"
                     f"AccessionNumber: {study['AccessionNumber'] or 'N/A'}\n"
                     f"StudyInstanceUID: {study['StudyInstanceUID']}\n"
                     f"StudyID: {study['StudyID']}"
            )
            header.configure(text=study["StudyDate"])

        def set_details():
            body.configure(
                text=f"Status: {study['Status']}\n"
                     f"Modality: {study['Modality']}\n"
                     f"SeriesInstanceUID: {study['SeriesInstanceUID']}\n"
                     f"SeriesNumber: {study['SeriesNumber']}"
            )
            header.configure(text=study["StudyID"])

        def on_enter(e): card.configure(fg_color="#f0f0f0")
        def on_leave(e): card.configure(fg_color="transparent")

        for widget in (card, header, body):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e: set_details())
            widget.configure(cursor="hand2")

        set_summary()

    def back_to_form(self):
        self.destroy()
        if self.master:
            self.master.deiconify()
