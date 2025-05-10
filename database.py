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