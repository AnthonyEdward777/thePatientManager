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
        self.geometry("800x400")
        self.configure(bg=DARK_BG)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=ENTRY_BG, foreground=FG, fieldbackground=ENTRY_BG, rowheight=28)
        style.configure("Treeview.Heading", background=DARK_BG, foreground=BTN_GREEN, font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", TABLE_HL)])
        style.configure("TLabel", background=DARK_BG, foreground=FG, font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"))
        self.create_patient_tab()

    def create_patient_tab(self):
        # Left form
        form = tk.Frame(self, bg=DARK_BG)
        form.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        labels = ["Name:", "Age:"]
        self.entries = {}
        for lbl in labels:
            tk.Label(form, text=lbl, bg=DARK_BG, fg=FG, anchor="w").pack(fill=tk.X, pady=2)
            ent = tk.Entry(form, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief=tk.FLAT)
            ent.pack(fill=tk.X, pady=2)
            self.entries[lbl[:-1].lower()] = ent

        tk.Button(form, text="Add Patient", bg=BTN_GREEN, fg=DARK_BG, command=self.add_patient).pack(fill=tk.X, pady=(10,2))
        tk.Button(form, text="New Patient", bg=BTN_ORANGE, fg=FG, command=self.clear_form).pack(fill=tk.X, pady=2)
        tk.Button(form, text="Delete Patient", bg=BTN_RED, fg=FG, command=self.delete_patient).pack(fill=tk.X, pady=2)

        # Right table
        right_frame = tk.Frame(self, bg=DARK_BG)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=20)

        columns = ("NID", "Name", "Age")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "Name" else 150, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh_patients()

        # Info display below table
        info_frame = tk.Frame(right_frame, bg=DARK_BG)
        info_frame.pack(fill=tk.X, pady=(10,0))
        self.info_labels = {}
        for field in columns:
            lbl = tk.Label(info_frame, text=f"{field}: ", bg=DARK_BG, fg=FG, font=("Arial", 10, "bold"), anchor="w")
            lbl.pack(fill=tk.X)
            self.info_labels[field] = lbl

    def refresh_patients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for pat in database.patients("", 0, 0).fetchAllPatients():
            self.tree.insert("", tk.END, values=(pat[0], pat[1], pat[2]))

    def add_patient(self):
        name = self.entries["name"].get()
        try:
            age = int(self.entries["age"].get())
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return
        database.patients(name, age, None).addPatient()
        self.refresh_patients()
        # Select the last added patient and update entry fields
        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[-1])
            self.tree.see(children[-1])
            self.on_select(None)

    def clear_form(self):
        for ent in self.entries.values():
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

if __name__ == "__main__":
    app = PatientManagerApp()
    app.mainloop()