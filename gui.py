import customtkinter as ctk

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