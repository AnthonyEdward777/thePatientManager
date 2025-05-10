import customtkinter as ctk
from entities.patients import patients
from entities.doctors import doctors
from entities.appointments import appointments

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("The Patient Manager")
        self.geometry("500x400")
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=20, expand=True, fill="both")

        self.doctorTab = self.tabview.add("Doctors")
        self.addDoctorTab_content()

        self.patientsTab = self.tabview.add("Patients")
        self.addPatientTab_content()
        
        self.appointmentsTab = self.tabview.add("Appointments")
        self.addAppointmentTab_content()
        
    def addDoc(self):
        self.name_label = ctk.CTkLabel(self, text="Name:")
        self.name_label.pack(pady=10)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=10)

        self.age_label = ctk.CTkLabel(self, text="Age:")
        self.age_label.pack(pady=10)
        self.age_entry = ctk.CTkEntry(self)
        self.age_entry.pack(pady=10)

        self.nid_label = ctk.CTkLabel(self, text="NID:")
        self.nid_label.pack(pady=10)
        self.nid_entry = ctk.CTkEntry(self)
        self.nid_entry.pack(pady=10)

        # Create submit button
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submit_button.pack(pady=20)