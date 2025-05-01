import sqlite3
import datetime

conn = sqlite3.connect('clinic.db')
c = conn.cursor()

class patients:
    def __init__(self, name, age, NID, phone, address):
        self.name = name
        self.age = age
        self.NID = NID
        self.phone = phone
        self.address = address

class doctors:
    def __init__(self, name, age, NID, pay, specialization):
        self.name = name
        self.age = age
        self.NID = NID
        self.pay = pay
        self.specialization = specialization

class appointments:
    def __init__(self, patient, doctor, date, room):
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.room = room