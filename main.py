from  abc import ABC, abstractmethod
import time
from datetime import datetime
from functools import wraps
from zoneinfo import ZoneInfo

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):   
        ist_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%b-%Y %H:%M:%S IST")
        print(f"[LOG] {ist_time} | Action: '{func.__name__}' started")
        start = time.time()

        try:
            result = func(*args, **kwargs)
            end = time.time()
            print(f"[LOG] {ist_time} | Action: '{func.__name__}' completed in {end-start}")
        except Exception as err:
            print(f"[LOG] {ist_time} | Action: '{func.__name__}'" f"raise {type(err).__name__}: {err}")
            raise
        return result
    return wrapper

class PatientNotFoundError(Exception):
    def __init__(self, message="Patient not found"):
        super().__init__(message)

class DoctorNotFoundError(Exception):
    def __init__(self, message="Doctor not found"):
        super().__init__(message)

class SlotNotAvailableError(Exception):
    def __init__(self, message="Slot not available"):
        super().__init__(message)

class AppointmentNotFoundError(Exception):
    def __init__(self, message="Appointment not found"):
        super().__init__(message)

class Person(ABC):
    def __init__(self, name, age, contact):
        self.name = name
        self.age = age
        self.contact = contact

    def __str__(self):
        return f"Role: {self.get_role()}\nName: {self.name}\nAge: {self.age}\nContact: {self.contact}"

    @abstractmethod
    def get_role(self):
        pass

class Patient(Person):
    def __init__(self, name, age, contact, patient_id, blood_group):
        super().__init__(name, age, contact)
        self.__patient_id = patient_id
        self.blood_group = blood_group
        self.medical_history = []

    def get_role(self):
        return "Patient"

    @property
    def patient_id(self):
        return self.__patient_id
        
    def add_medical_record(self, record):
        self.medical_history.append(record)

    def get_history(self):
        history = ""

        for i, record in enumerate(self.medical_history, 1):
            history += f"{i}. {record}\n"
        return history

obj = Patient("Ananya", 21, 123, 1, "B+")
# while True:
#     data = input("Enter your medical record: ")
#     obj.add_medical_record(data)
#     choice = input("Do you want to add more records? (yes/no): ")
#     if choice.lower() == "no":
#         break

# print(obj)
# print("your history: ")
# print(obj.get_history())
    
class Doctor(Person):
    def __init__(self, name, age, contact, doctor_id, specialization):
        super().__init__(name, age, contact)
        self.__doctor_id = doctor_id
        self.specialization = specialization
        self.available_slots = []

    def get_role(self):
        return "Doctor"

    @property
    def doctor_id(self):
        return self.__doctor_id
    
    def add_slot(self, time):
        if time not in self.available_slots:
            self.available_slots.append(time)
            print("slot added successfully")

    def remove_slot(self, time):
        if time in self.available_slots:
            self.available_slots.remove(time)
            print("slot removes successfully")
        else:
            print("slot already removed")

    @staticmethod
    def validate_slot_format(slot):
        parts = slot.split(":")

        if len(parts) != 2:
            return False
        
        hours, minutes = parts
        if not (hours.isdigit() and minutes.isdigit()):
            return False
        
        hours = int(hours)
        minutes = int(minutes)

        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return True
        
        return False

doc_obj = Doctor("mr. bhatt", 35, 923, 21, "ortho")
# while True:
#     add_time = input("enter the available slot time(HH:MM): ")
#     if Doctor.validate_slot_format(add_time):     
#         doc_obj.add_slot(add_time)
#         print(doc_obj.available_slots)
#         choice = input("Add more slots? (yes/no): ")
#         if choice.lower() == "no":
#             break
#         else:
#             print("slot already exists")
#     else:
#         print("invalid date format")

# choice = input("Do you want to remove any slot? (yes/no): ")
# if choice.lower() == "yes":
#     remove_time = input("enter the slot time(HH:MM) you want to remove: ")
#     doc_obj.remove_slot(remove_time)
#     print(doc_obj.available_slots)

class Appointment:
    count = 1
    def __init__(self, patient, doctor, time_slot, status="Scheduled"):

        self.appointment_id  = f"APT{str(Appointment.count).zfill(4)}"
        Appointment.count += 1
        print(self.appointment_id)

        self.patient = patient
        self.doctor = doctor
        self.time_slot = time_slot
        self.status = status

    def cancel(self):
        self.status = "Cancelled"
        self.doctor.add_slot(self.time_slot)

    def __str__(self):

        return f"""
        Appointment ID : {self.appointment_id}
        Patient        : {self.patient.name}
        Doctor         : {self.doctor.name}
        Time Slot      : {self.time_slot}
        Status         : {self.status}
        """

class Hospital:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = {}

    @log_action
    def register_patient(self, patient):
        self.patients[patient.patient_id] = patient

    @log_action
    def register_doctor(self, doctor):
        self.doctors[doctor.doctor_id] = doctor

    @log_action
    def book_appointment(self, patient_id, doctor_id, time_slot):
    
        if patient_id not in self.patients:
            raise PatientNotFoundError("Patient not found")
        
        if doctor_id not in self.doctors:
            raise DoctorNotFoundError("Doctor not found")
        
        if not Doctor.validate_slot_format(time_slot):
            raise ValueError("Invalid slot format")
        
        doctor = self.doctors[doctor_id]
        patient = self.patients[patient_id]
        
        if time_slot not in doctor.available_slots:
            raise SlotNotAvailableError("time slot not available")
        
        appointment = Appointment(patient, doctor, time_slot)
        self.appointments[appointment.appointment_id] = appointment

        doctor.remove_slot(time_slot)
        return appointment
    
    @log_action
    def cancel_appointment(self, appointment_id):
        if appointment_id not in self.appointments:
            raise AppointmentNotFoundError("Appointment not found")
        
        appointment = self.appointments[appointment_id]
        appointment.cancel()

    def get_doctor_appointments(self, doctor_id):
    
        return list(
        filter(
            lambda appointment : appointment.doctor.doctor_id == doctor_id
            and
            appointment.status == "Scheduled",
            self.appointments.values()
        )
    )

    def get_all_patients(self, sort_by_name=False):

        patients = list(self.patients.values())

        if sort_by_name:
            patients = sorted(
                patients,
                key=lambda patient : patient.name
            )
        return patients
    
    def patient_report(self, patient_id):
        if patient_id not in self.patients:
            raise PatientNotFoundError("No patient record found")
        
        patient = self.patients[patient_id]

        yield f"=== Report: {patient.name} (ID: {patient.patient_id}) ==="
        yield f"Blood Group : {patient.blood_group}"

        yield "Medical History: "

        if not patient.medical_history:
            yield "No records found"
        else:
            for index, record in enumerate(patient.medical_history, start=1):
                yield f"  {index}. {record}"
        
        yield "Appointment History:"

        patient_appointments = [
            appointment
            for appointment in self.appointments.values()
            if appointment.patient.patient_id == patient_id
    ]

        if not patient_appointments:
            yield "  No appointments found."

        else:
            for appointment in patient_appointments:

                yield (
                    f"  [{appointment.status}] "
                    f"{appointment.appointment_id} — "
                    f"Dr.{appointment.doctor.name} "
                    f"at {appointment.time_slot}"
                )

    # def __str__(self):

    #     return f"""
    #     Total Patients     : {len(self.patients)}
    #     Total Doctors      : {len(self.doctors)}
    #     Total Appointments : {len(self.appointments)}
    #     """

    def admin_report(self):

        print(f"Hospital has {len(self.patients)} patients")

        print(f"Hospital has {len(self.doctors)} doctors")

        print(f"Hospital has {len(self.appointments)} appointments")

if __name__ == "__main__":

    hospital = Hospital()

    doc1 = Doctor("dr. Rina", 35, 9876543, "D002", "Gyno")
    doc2 = Doctor("dr. Bedi", 46, 9872345, "D003", "Surgen")

    doc1.add_slot("10:15")
    doc1.add_slot("11:15")
    doc2.add_slot("11:30")

    pat1 = Patient("Richa", 22, 9876234, "P012", "A+")
    pat2 = Patient("Raja Bajaj", 32, 9822223, "P015", "AB+")
    pat3 = Patient("Ahana ", 29, 984565, "P032", "O+")

    pat1.add_medical_record("PCOD")
    pat2.add_medical_record("Bone Fracture")
    pat1.add_medical_record("Fever")
    pat3.add_medical_record("Sinus")

    hospital.register_doctor(doc1)
    hospital.register_doctor(doc2)

    hospital.register_patient(pat1)
    hospital.register_patient(pat2)
    hospital.register_patient(pat3)

    apt1 = hospital.book_appointment("P012", "D002", "10:15")
    apt2 = hospital.book_appointment("P015", "D003", "11:30")
    apt3 = hospital.book_appointment("P032", "D002", "11:15")

    try:
        hospital.book_appointment("P032", "D002", "10:15")
    except SlotNotAvailableError as s:
        print(s)

    try:
        hospital.book_appointment("P042", "D012", "10:15")
    except PatientNotFoundError as p:
        print(p)

    hospital.cancel_appointment(apt1.appointment_id)
    print(doc2.available_slots)

    patients = hospital.get_all_patients(True)
    for patient in patients:
        print(patient)

    appointments = hospital.get_doctor_appointments("D001")
    for appointment in appointments:
        print(appointment)

    for record in hospital.patient_report("P012"):
        print(record)
