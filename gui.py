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
        self.create_patient_tab()

    def flashy_button(self, parent, text, bg, fg, command):
        btn = tk.Button(parent, text=text, bg=bg, fg=fg, font=("Segoe UI", 12, "bold"), activebackground=fg, activeforeground=bg, command=command, relief=tk.FLAT, bd=2, highlightthickness=2, highlightbackground=bg)
        btn.pack(fill=tk.X, pady=4)
        btn.bind("<Enter>", lambda e: btn.config(bg=fg, fg=bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg))
        return btn

    def create_patient_tab(self):
        # Left form
        form = tk.Frame(self, bg=DARK_BG)
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
        right_frame = tk.Frame(self, bg=DARK_BG)
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

    def refresh_patients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for pat in database.patients("", 0, 0).fetchAllPatients():
            self.tree.insert("", tk.END, values=(pat[1], pat[0], pat[2]))

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
        self.on_select(None)  # Clear info labels after deletion

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