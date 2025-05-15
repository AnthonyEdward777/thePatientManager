from tkinter import Tk, Frame, Button, Label, StringVar, ttk
from gui.doctors_view import DoctorsView
from gui.patients_view import PatientsView
from gui.appointments_view import AppointmentsView

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("The Patient Manager")
        self.master.geometry("800x600")

        self.current_frame = None
        self.show_home()

        self.create_navigation()

    def create_navigation(self):
        nav_frame = Frame(self.master)
        nav_frame.pack(side="top", fill="x")

        Button(nav_frame, text="Doctors", command=self.show_doctors_view).pack(side="left")
        Button(nav_frame, text="Patients", command=self.show_patients_view).pack(side="left")
        Button(nav_frame, text="Appointments", command=self.show_appointments_view).pack(side="left")

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self.master)
        self.current_frame.pack(fill="both", expand=True)

    def show_home(self):
        home_frame = Frame(self.master)
        home_frame.pack(fill="both", expand=True)

        Label(home_frame, text="Welcome to The Patient Manager", font=("Helvetica", 16)).pack(pady=20)
        Label(home_frame, text="Select an option from the navigation bar.").pack(pady=10)

    def show_doctors_view(self):
        self.show_frame(DoctorsView)

    def show_patients_view(self):
        self.show_frame(PatientsView)

    def show_appointments_view(self):
        self.show_frame(AppointmentsView)

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    root.mainloop()