import tkinter as tk
from tkinter import ttk, messagebox
import database

database.init_db()

DARK_BG = "#181c25"
ENTRY_BG = "#232837"
FG = "#fff"
BTN_GREEN = "#1de982"
BTN_RED = "#e53935"
BTN_ORANGE = "#ff9800"
TABLE_HL = "#2ecc40"

class PatientManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Patient Manager")
        self.geometry("900x450")
        self.configure(bg=DARK_BG)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", 
                        background=ENTRY_BG, 
                        foreground=FG, 
                        fieldbackground=ENTRY_BG, 
                        rowheight=32,
                        font=("Segoe UI", 12))
        style.configure("Treeview.Heading", 
                        background="#222", 
                        foreground="#00ffc8", 
                        font=("Segoe UI", 13, "bold"))
        style.map("Treeview", background=[("selected", "#00ffc8")], foreground=[("selected", "#222")])
        style.configure("TLabel", background=DARK_BG, foreground=FG, font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=6)

        # Add notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Patients tab
        self.patient_tab = tk.Frame(self.notebook, bg=DARK_BG)
        self.notebook.add(self.patient_tab, text="Patients")
        self.create_patient_tab(self.patient_tab)

        # Doctors tab
        self.doctor_tab = tk.Frame(self.notebook, bg=DARK_BG)
        self.notebook.add(self.doctor_tab, text="Doctors")
        self.create_doctor_tab(self.doctor_tab)

        # Appointments tab
        self.appointment_tab = tk.Frame(self.notebook, bg=DARK_BG)
        self.notebook.add(self.appointment_tab, text="Appointments")
        self.create_appointment_tab(self.appointment_tab)

    def flashy_button(self, parent, text, bg, fg, command):
        btn = tk.Button(parent, text=text, bg=bg, fg=fg, font=("Segoe UI", 12, "bold"), activebackground=fg, activeforeground=bg, command=command, relief=tk.FLAT, bd=2, highlightthickness=2, highlightbackground=bg)
        btn.pack(fill=tk.X, pady=4)
        btn.bind("<Enter>", lambda e: btn.config(bg=fg, fg=bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg))
        return btn

    def create_patient_tab(self, parent):
        # Left form
        form = tk.Frame(parent, bg=DARK_BG)
        form.pack(side=tk.LEFT, fill=tk.Y, padx=24, pady=24)
        labels = ["Name:", "Age:"]
        self.entries = {}
        for lbl in labels:
            tk.Label(form, text=lbl, bg=DARK_BG, fg="#00ffc8", anchor="w", font=("Segoe UI", 12, "bold")).pack(fill=tk.X, pady=2)
            ent = tk.Entry(form, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief=tk.FLAT, font=("Segoe UI", 12))
            ent.pack(fill=tk.X, pady=2)
            self.entries[lbl[:-1].lower()] = ent

        self.flashy_button(form, "Add Patient", BTN_GREEN, DARK_BG, self.add_patient)
        self.flashy_button(form, "New Patient", BTN_ORANGE, FG, self.clear_form)
        self.flashy_button(form, "Delete Patient", BTN_RED, FG, self.delete_patient)

        # Right table
        right_frame = tk.Frame(parent, bg=DARK_BG)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=24)

        columns = ("NID", "Name", "Age")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col != "Name" else 180, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh_patients()

        # Info display below table
        info_frame = tk.Frame(right_frame, bg="#00ffc8", bd=3, relief=tk.RIDGE)
        info_frame.pack(fill=tk.X, pady=(16,0), padx=10)
        self.info_labels = {}
        for field in columns:
            lbl = tk.Label(info_frame, text=f"{field}: ", bg="#00ffc8", fg="#222", font=("Segoe UI", 12, "bold"), anchor="w")
            lbl.pack(fill=tk.X)
            self.info_labels[field] = lbl

    def create_doctor_tab(self, parent):
        # Left form
        form = tk.Frame(parent, bg=DARK_BG)
        form.pack(side=tk.LEFT, fill=tk.Y, padx=24, pady=24)
        labels = ["Name:", "Age:"]
        self.doc_entries = {}
        for lbl in labels:
            tk.Label(form, text=lbl, bg=DARK_BG, fg="#00ffc8", anchor="w", font=("Segoe UI", 12, "bold")).pack(fill=tk.X, pady=2)
            ent = tk.Entry(form, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief=tk.FLAT, font=("Segoe UI", 12))
            ent.pack(fill=tk.X, pady=2)
            self.doc_entries[lbl[:-1].lower()] = ent

        self.flashy_button(form, "Add Doctor", BTN_GREEN, DARK_BG, self.add_doctor)
        self.flashy_button(form, "New Doctor", BTN_ORANGE, FG, self.clear_doc_form)
        self.flashy_button(form, "Delete Doctor", BTN_RED, FG, self.delete_doctor)

        # Right table
        right_frame = tk.Frame(parent, bg=DARK_BG)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=24)

        columns = ("NID", "Name", "Age")
        self.doc_tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.doc_tree.heading(col, text=col)
            self.doc_tree.column(col, width=120 if col != "Name" else 180, anchor="center")
        self.doc_tree.pack(fill=tk.BOTH, expand=True)
        self.doc_tree.bind("<<TreeviewSelect>>", self.on_doc_select)
        self.refresh_doctors()

        # Info display below table
        info_frame = tk.Frame(right_frame, bg="#00ffc8", bd=3, relief=tk.RIDGE)
        info_frame.pack(fill=tk.X, pady=(16,0), padx=10)
        self.doc_info_labels = {}
        for field in columns:
            lbl = tk.Label(info_frame, text=f"{field}: ", bg="#00ffc8", fg="#222", font=("Segoe UI", 12, "bold"), anchor="w")
            lbl.pack(fill=tk.X)
            self.doc_info_labels[field] = lbl

    def create_appointment_tab(self, parent):
        # Left form
        form = tk.Frame(parent, bg=DARK_BG)
        form.pack(side=tk.LEFT, fill=tk.Y, padx=24, pady=24)
        tk.Label(form, text="Doctor:", bg=DARK_BG, fg="#00ffc8", anchor="w", font=("Segoe UI", 12, "bold")).pack(fill=tk.X, pady=2)
        self.app_doc_combo = ttk.Combobox(form, state="readonly", font=("Segoe UI", 12))
        self.app_doc_combo.pack(fill=tk.X, pady=2)
        tk.Label(form, text="Patient:", bg=DARK_BG, fg="#00ffc8", anchor="w", font=("Segoe UI", 12, "bold")).pack(fill=tk.X, pady=2)
        self.app_pat_combo = ttk.Combobox(form, state="readonly", font=("Segoe UI", 12))
        self.app_pat_combo.pack(fill=tk.X, pady=2)
        tk.Label(form, text="Date (YYYY-MM-DD):", bg=DARK_BG, fg="#00ffc8", anchor="w", font=("Segoe UI", 12, "bold")).pack(fill=tk.X, pady=2)
        self.app_date_entry = tk.Entry(form, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief=tk.FLAT, font=("Segoe UI", 12))
        self.app_date_entry.pack(fill=tk.X, pady=2)

        self.flashy_button(form, "Add Appointment", BTN_GREEN, DARK_BG, self.add_appointment)
        self.flashy_button(form, "Delete Appointment", BTN_RED, FG, self.delete_appointment)
        self.flashy_button(form, "Refresh", BTN_ORANGE, FG, self.refresh_appointments)

        # Right table
        right_frame = tk.Frame(parent, bg=DARK_BG)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=24)

        columns = ("ID", "Doctor", "Patient", "Date")
        self.app_tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.app_tree.heading(col, text=col)
            self.app_tree.column(col, width=120 if col != "Date" else 180, anchor="center")
        self.app_tree.pack(fill=tk.BOTH, expand=True)
        self.app_tree.bind("<<TreeviewSelect>>", self.on_app_select)
        self.refresh_appointments()

        # Info display below table
        info_frame = tk.Frame(right_frame, bg="#00ffc8", bd=3, relief=tk.RIDGE)
        info_frame.pack(fill=tk.X, pady=(16,0), padx=10)
        self.app_info_labels = {}
        for field in columns:
            lbl = tk.Label(info_frame, text=f"{field}: ", bg="#00ffc8", fg="#222", font=("Segoe UI", 12, "bold"), anchor="w")
            lbl.pack(fill=tk.X)
            self.app_info_labels[field] = lbl

    def refresh_patients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for pat in database.patients("", 0, 0).fetchAllPatients():
            self.tree.insert("", tk.END, values=(pat[1], pat[0], pat[2]))

    def refresh_doctors(self):
        for row in self.doc_tree.get_children():
            self.doc_tree.delete(row)
        for doc in database.doctors("", 0, 0).fetchAllDoctors():
            self.doc_tree.insert("", tk.END, values=(doc[1], doc[0], doc[2]))

    def refresh_appointments(self):
        # Update doctor/patient comboboxes
        docs = database.doctors("", 0, 0).fetchAllDoctors()
        self.app_doc_combo["values"] = [f"{doc[1]} - {doc[0]}" for doc in docs]
        pats = database.patients("", 0, 0).fetchAllPatients()
        self.app_pat_combo["values"] = [f"{pat[1]} - {pat[0]}" for pat in pats]

        # Update appointment table
        for row in self.app_tree.get_children():
            self.app_tree.delete(row)
        for app in database.appointments(0, 0, "", 0).fetchAllAppointments():
            # app = (ID, doctorNID, patientNID, date)
            doc = next((d for d in docs if d[1] == app[1]), None)
            pat = next((p for p in pats if p[1] == app[2]), None)
            doc_name = doc[0] if doc else f"ID:{app[1]}"
            pat_name = pat[0] if pat else f"ID:{app[2]}"
            self.app_tree.insert("", tk.END, values=(app[0], doc_name, pat_name, app[3]))

    def add_patient(self):
        name = self.entries["name"].get().strip()
        age_str = self.entries["age"].get().strip()
        if not name or not age_str:
            messagebox.showerror("Error", "Both Name and Age are required.")
            return
        try:
            age = int(age_str)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return
        database.patients(name, age, None).addPatient()
        self.refresh_patients()
        self.refresh_appointments()  # Update appointments tab dropdowns
        # Select the last added patient and update entry fields
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[-1])
            self.tree.see(children[-1])
            self.on_select(None)

    def add_doctor(self):
        name = self.doc_entries["name"].get().strip()
        age_str = self.doc_entries["age"].get().strip()
        if not name or not age_str:
            messagebox.showerror("Error", "Both Name and Age are required.")
            return
        try:
            age = int(age_str)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return
        database.doctors(name, age, None).addDoctor()
        self.refresh_doctors()
        self.refresh_appointments()  # Update appointments tab dropdowns
        # Select the last added doctor and update entry fields
        children = self.doc_tree.get_children()
        if children:
            self.doc_tree.selection_set(children[-1])
            self.doc_tree.see(children[-1])
            self.on_doc_select(None)

    def add_appointment(self):
        doc_val = self.app_doc_combo.get()
        pat_val = self.app_pat_combo.get()
        date = self.app_date_entry.get().strip()
        if not doc_val or not pat_val or not date:
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            doc_nid = int(doc_val.split(" - ")[0])
            pat_nid = int(pat_val.split(" - ")[0])
        except Exception:
            messagebox.showerror("Error", "Invalid doctor or patient selection.")
            return
        database.appointments(doc_nid, pat_nid, date, None).addAppointment()
        self.refresh_appointments()

    def clear_form(self):
        for ent in self.entries.values():
            ent.delete(0, tk.END)

    def clear_doc_form(self):
        for ent in self.doc_entries.values():
            ent.delete(0, tk.END)

    def delete_patient(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No patient selected.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient?")
        if not confirm:
            return
        nid = self.tree.item(selected[0])["values"][0]
        database.patients("", 0, nid).deletePatient()
        self.refresh_patients()
        self.clear_form()
        self.on_select(None)  # Clear info labels after deletion

    def delete_doctor(self):
        selected = self.doc_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No doctor selected.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?")
        if not confirm:
            return
        nid = self.doc_tree.item(selected[0])["values"][0]
        database.doctors("", 0, nid).deleteDoctor()
        self.refresh_doctors()
        self.clear_doc_form()
        self.on_doc_select(None)  # Clear info labels after deletion

    def delete_appointment(self):
        selected = self.app_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No appointment selected.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?")
        if not confirm:
            return
        app_id = self.app_tree.item(selected[0])["values"][0]
        database.appointments(0, 0, "", app_id).deleteAppointment()
        self.refresh_appointments()
        self.on_app_select(None)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            for lbl in self.info_labels.values():
                lbl.config(text="")
            return
        values = self.tree.item(selected[0])["values"]
        self.entries["name"].delete(0, tk.END)
        self.entries["name"].insert(0, values[1])
        self.entries["age"].delete(0, tk.END)
        self.entries["age"].insert(0, values[2])
        # Show info below table
        for i, field in enumerate(("NID", "Name", "Age")):
            self.info_labels[field].config(text=f"{field}: {values[i]}")

    def on_doc_select(self, event):
        selected = self.doc_tree.selection()
        if not selected:
            for lbl in self.doc_info_labels.values():
                lbl.config(text="")
            return
        values = self.doc_tree.item(selected[0])["values"]
        self.doc_entries["name"].delete(0, tk.END)
        self.doc_entries["name"].insert(0, values[1])
        self.doc_entries["age"].delete(0, tk.END)
        self.doc_entries["age"].insert(0, values[2])
        # Show info below table
        for i, field in enumerate(("NID", "Name", "Age")):
            self.doc_info_labels[field].config(text=f"{field}: {values[i]}")

    def on_app_select(self, event):
        selected = self.app_tree.selection()
        if not selected:
            for lbl in self.app_info_labels.values():
                lbl.config(text="")
            return
        values = self.app_tree.item(selected[0])["values"]
        for i, field in enumerate(("ID", "Doctor", "Patient", "Date")):
            self.app_info_labels[field].config(text=f"{field}: {values[i]}")

if __name__ == "__main__":
    app = PatientManagerApp()
    app.mainloop()