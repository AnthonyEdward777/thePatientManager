import sqlite3 as sql

def init_db():
    conn = sql.connect('clinic.db')
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

    c.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        doctorName INTEGER,
        patientName INTEGER,
        date TEXT NOT NULL,
        FOREIGN KEY(doctorName) REFERENCES doctors(name),
        FOREIGN KEY(patientName) REFERENCES patients(name)
    )""")

    conn.commit()
    conn.close()
    
class doctors:
    def __init__(self, name, age, NID):
        self.name = name
        self.age = age
        self.NID = NID
    
    def fetchAllDoctors(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("SELECT * FROM doctors")
        doctors = c.fetchall()
        conn.close()
        return doctors
    
    def addDoctor(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("INSERT INTO doctors (name, age) VALUES (?, ?)", (self.name, self.age))
        conn.commit()
        conn.close()   
    
    def deleteDoctor(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("DELETE FROM doctors WHERE NID=?", (self.NID,))
        conn.commit()
        conn.close()
    
    def updateDoctor(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("UPDATE doctors SET name=?, age=? WHERE NID=?", (self.name, self.age, self.NID))
        conn.commit()
        conn.close()
        
    def docExists(self):
        conn = sql.connect('clinic.db')
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
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("SELECT * FROM patients")
        patients = c.fetchall()
        conn.close()
        return patients
    
    def addPatient(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age) VALUES (?, ?)", (self.name, self.age))
        conn.commit()
        conn.close()   
    
    def deletePatient(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("DELETE FROM patients WHERE NID=?", (self.NID,))
        conn.commit()
        conn.close()
    
    def updatePatient(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("UPDATE patients SET name=?, age=? WHERE NID=?", (self.name, self.age, self.NID))
        conn.commit()
        conn.close()
        
    def patExists(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM patients WHERE NID=?", (self.NID,))
        patient = c.fetchone()
        conn.close()
        return patient[0] > 0
    
class appointments:
    def __init__(self, doctorName, patientName, date, ID):
        self.doctorName = doctorName
        self.patientName = patientName
        self.date = date
        self.ID = ID
    
    def fetchAllAppointments(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("SELECT * FROM appointments")
        appointments = c.fetchall()
        conn.close()
        return appointments
    
    def addAppointment(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("INSERT INTO appointments (doctorName, patientName, date) VALUES (?, ?, ?)", (self.doctorName, self.patientName, self.date))
        conn.commit()
        conn.close()   
    
    def deleteAppointment(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("DELETE FROM appointments WHERE ID=?", (self.ID,))
        conn.commit()
        conn.close()
    
    def updateAppointment(self):
        conn = sql.connect('clinic.db')
        c = conn.cursor()
        c.execute("UPDATE appointments SET doctorName=?, patientName=?, date=? WHERE ID=?", (self.doctorName, self.patientName, self.date, self.ID))
        conn.commit()
        conn.close()