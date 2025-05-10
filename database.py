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
        c.execute("INSERT INTO doctors (name, age) VALUES (?, ?)", (self.name, self.NID,self.age))
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
        return result[0] > 0