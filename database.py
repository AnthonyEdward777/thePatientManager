import sqlite3 as sql

def get_connection():
    conn = sql.connect('clinic.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        name TEXT NOT NULL,
        NID INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER NOT NULL
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        name TEXT NOT NULL,
        NID INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER NOT NULL
    )""")

    # Drop and recreate appointments table with ON DELETE CASCADE if needed
    c.execute("DROP TABLE IF EXISTS appointments")
    c.execute("""
    CREATE TABLE appointments (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        doctorNID INTEGER,
        patientNID INTEGER,
        date TEXT NOT NULL,
        FOREIGN KEY(doctorNID) REFERENCES doctors(NID) ON DELETE CASCADE,
        FOREIGN KEY(patientNID) REFERENCES patients(NID) ON DELETE CASCADE
    )""")

    conn.commit()
    conn.close()

class doctors:
    def __init__(self, name, age, NID):
        self.name = name
        self.age = age
        self.NID = NID

    def fetchAllDoctors(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM doctors")
        doctors = c.fetchall()
        conn.close()
        return doctors

    def addDoctor(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO doctors (name, age) VALUES (?, ?)", (self.name, self.age))
        conn.commit()
        conn.close()

    def deleteDoctor(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM doctors WHERE NID=?", (self.NID,))
        conn.commit()
        conn.close()

    def updateDoctor(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE doctors SET name=?, age=? WHERE NID=?", (self.name, self.age, self.NID))
        conn.commit()
        conn.close()

    def docExists(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM doctors WHERE NID=?", (self.NID,))
        doctor = c.fetchone()
        conn.close()
        return doctor[0] > 0

class patients:
    def __init__(self, name, age, NID):
        self.name = name
        self.age = age
        self.NID = NID

    def fetchAllPatients(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM patients")
        patients = c.fetchall()
        conn.close()
        return patients

    def addPatient(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age) VALUES (?, ?)", (self.name, self.age))
        conn.commit()
        conn.close()

    def deletePatient(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM patients WHERE NID=?", (self.NID,))
        conn.commit()
        conn.close()

    def updatePatient(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE patients SET name=?, age=? WHERE NID=?", (self.name, self.age, self.NID))
        conn.commit()
        conn.close()

    def patExists(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM patients WHERE NID=?", (self.NID,))
        patient = c.fetchone()
        conn.close()
        return patient[0] > 0

class appointments:
    def __init__(self, doctorNID, patientNID, date, ID):
        self.doctorNID = doctorNID
        self.patientNID = patientNID
        self.date = date
        self.ID = ID

    def fetchAllAppointments(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM appointments")
        appointments = c.fetchall()
        conn.close()
        return appointments

    def addAppointment(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO appointments (doctorNID, patientNID, date) VALUES (?, ?, ?)", (self.doctorNID, self.patientNID, self.date))
        conn.commit()
        conn.close()

    def deleteAppointment(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM appointments WHERE ID=?", (self.ID,))
        conn.commit()
        conn.close()

    def updateAppointment(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE appointments SET doctorNID=?, patientNID=?, date=? WHERE ID=?", (self.doctorNID, self.patientNID, self.date, self.ID))
        conn.commit()
        conn.close()