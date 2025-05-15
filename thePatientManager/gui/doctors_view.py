from tkinter import *
from tkinter import messagebox
from database import doctors

class DoctorsView:
    def __init__(self, master):
        self.master = master
        self.master.title("Doctors Management")
        
        self.frame = Frame(self.master)
        self.frame.pack(pady=10)

        self.doctor_listbox = Listbox(self.frame, width=50)
        self.doctor_listbox.pack(padx=20)

        self.name_label = Label(self.frame, text="Name:")
        self.name_label.pack(pady=5)
        self.name_entry = Entry(self.frame)
        self.name_entry.pack(pady=5)

        self.age_label = Label(self.frame, text="Age:")
        self.age_label.pack(pady=5)
        self.age_entry = Entry(self.frame)
        self.age_entry.pack(pady=5)

        self.add_button = Button(self.frame, text="Add Doctor", command=self.add_doctor)
        self.add_button.pack(pady=5)

        self.update_button = Button(self.frame, text="Update Doctor", command=self.update_doctor)
        self.update_button.pack(pady=5)

        self.delete_button = Button(self.frame, text="Delete Doctor", command=self.delete_doctor)
        self.delete_button.pack(pady=5)

        self.fetch_doctors()

    def fetch_doctors(self):
        self.doctor_listbox.delete(0, END)
        doctor_instance = doctors("", 0, 0)
        all_doctors = doctor_instance.fetchAllDoctors()
        for doctor in all_doctors:
            self.doctor_listbox.insert(END, f"NID: {doctor[1]}, Name: {doctor[0]}, Age: {doctor[2]}")

    def add_doctor(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        if name and age:
            new_doctor = doctors(name, int(age), 0)
            new_doctor.addDoctor()
            self.fetch_doctors()
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Please provide both name and age.")

    def update_doctor(self):
        selected_doctor = self.doctor_listbox.curselection()
        if selected_doctor:
            doctor_info = self.doctor_listbox.get(selected_doctor).split(", ")
            nid = int(doctor_info[0].split(": ")[1])
            name = self.name_entry.get()
            age = self.age_entry.get()
            if name and age:
                updated_doctor = doctors(name, int(age), nid)
                updated_doctor.updateDoctor()
                self.fetch_doctors()
                self.clear_entries()
            else:
                messagebox.showwarning("Input Error", "Please provide both name and age.")
        else:
            messagebox.showwarning("Selection Error", "Please select a doctor to update.")

    def delete_doctor(self):
        selected_doctor = self.doctor_listbox.curselection()
        if selected_doctor:
            doctor_info = self.doctor_listbox.get(selected_doctor).split(", ")
            nid = int(doctor_info[0].split(": ")[1])
            doctor_to_delete = doctors("", 0, nid)
            doctor_to_delete.deleteDoctor()
            self.fetch_doctors()
            self.clear_entries()
        else:
            messagebox.showwarning("Selection Error", "Please select a doctor to delete.")

    def clear_entries(self):
        self.name_entry.delete(0, END)
        self.age_entry.delete(0, END)