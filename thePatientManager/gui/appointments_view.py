from tkinter import *
from tkinter import messagebox
from database import appointments

class AppointmentsView:
    def __init__(self, master):
        self.master = master
        self.master.title("Appointments Management")

        self.label = Label(master, text="Manage Appointments")
        self.label.pack()

        self.appointment_listbox = Listbox(master)
        self.appointment_listbox.pack()

        self.load_appointments()

        self.add_button = Button(master, text="Add Appointment", command=self.add_appointment)
        self.add_button.pack()

        self.update_button = Button(master, text="Update Appointment", command=self.update_appointment)
        self.update_button.pack()

        self.delete_button = Button(master, text="Delete Appointment", command=self.delete_appointment)
        self.delete_button.pack()

    def load_appointments(self):
        self.appointment_listbox.delete(0, END)
        app = appointments("", "", "", 0)
        for appointment in app.fetchAllAppointments():
            self.appointment_listbox.insert(END, appointment)

    def add_appointment(self):
        # Logic to add an appointment (e.g., open a new window to input details)
        pass

    def update_appointment(self):
        # Logic to update the selected appointment
        pass

    def delete_appointment(self):
        selected = self.appointment_listbox.curselection()
        if selected:
            appointment_id = self.appointment_listbox.get(selected)[0]  # Assuming ID is the first element
            app = appointments("", "", "", appointment_id)
            app.deleteAppointment()
            self.load_appointments()
        else:
            messagebox.showwarning("Selection Error", "Please select an appointment to delete.")

if __name__ == "__main__":
    root = Tk()
    app_view = AppointmentsView(root)
    root.mainloop()