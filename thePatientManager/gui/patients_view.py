from tkinter import *
from tkinter import messagebox
from database import patients

class PatientsView:
    def __init__(self, master):
        self.master = master
        self.master.title("Patients Management")
        
        self.label_name = Label(master, text="Name:")
        self.label_name.grid(row=0, column=0)
        self.entry_name = Entry(master)
        self.entry_name.grid(row=0, column=1)

        self.label_age = Label(master, text="Age:")
        self.label_age.grid(row=1, column=0)
        self.entry_age = Entry(master)
        self.entry_age.grid(row=1, column=1)

        self.label_nid = Label(master, text="NID:")
        self.label_nid.grid(row=2, column=0)
        self.entry_nid = Entry(master)
        self.entry_nid.grid(row=2, column=1)

        self.button_add = Button(master, text="Add Patient", command=self.add_patient)
        self.button_add.grid(row=3, column=0, columnspan=2)

        self.button_fetch = Button(master, text="Fetch Patients", command=self.fetch_patients)
        self.button_fetch.grid(row=4, column=0, columnspan=2)

        self.listbox_patients = Listbox(master)
        self.listbox_patients.grid(row=5, column=0, columnspan=2)

        self.button_delete = Button(master, text="Delete Patient", command=self.delete_patient)
        self.button_delete.grid(row=6, column=0, columnspan=2)

        self.button_update = Button(master, text="Update Patient", command=self.update_patient)
        self.button_update.grid(row=7, column=0, columnspan=2)

    def add_patient(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        nid = self.entry_nid.get()
        if name and age and nid:
            new_patient = patients(name, age, nid)
            new_patient.addPatient()
            messagebox.showinfo("Success", "Patient added successfully!")
            self.fetch_patients()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def fetch_patients(self):
        self.listbox_patients.delete(0, END)
        patient_instance = patients("", "", "")
        all_patients = patient_instance.fetchAllPatients()
        for patient in all_patients:
            self.listbox_patients.insert(END, f"Name: {patient[0]}, Age: {patient[2]}, NID: {patient[1]}")

    def delete_patient(self):
        selected_patient = self.listbox_patients.curselection()
        if selected_patient:
            patient_info = self.listbox_patients.get(selected_patient).split(", ")
            nid = patient_info[2].split(": ")[1]
            patient_instance = patients("", "", nid)
            patient_instance.deletePatient()
            messagebox.showinfo("Success", "Patient deleted successfully!")
            self.fetch_patients()
        else:
            messagebox.showwarning("Selection Error", "Please select a patient to delete.")

    def update_patient(self):
        selected_patient = self.listbox_patients.curselection()
        if selected_patient:
            patient_info = self.listbox_patients.get(selected_patient).split(", ")
            nid = patient_info[2].split(": ")[1]
            name = self.entry_name.get()
            age = self.entry_age.get()
            patient_instance = patients(name, age, nid)
            patient_instance.updatePatient()
            messagebox.showinfo("Success", "Patient updated successfully!")
            self.fetch_patients()
        else:
            messagebox.showwarning("Selection Error", "Please select a patient to update.")