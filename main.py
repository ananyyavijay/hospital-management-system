import random 
from  abc import ABC, abstractmethod

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Action: '{func.__name__}' started")
        result = func(*args, **kwargs)
        print(f"[LOG] Action: '{func.__name__}' completed")
        return result
    return wrapper

class PatientNotFoundError(Exception):
    pass


class DoctorNotFoundError(Exception):
    pass


class SlotNotAvailableError(Exception):
    pass


class AppointmentNotFoundError(Exception):
    pass

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
        else:
            print("slot already exists")

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
        self.patient = {}
        self.doctor = {}
        self.appointments = {}

    @log_action
    def register_patient(self, patient):
        self.patient[patient.patient_id] = patient

    @log_action
    def register_doctor(self, doctor):
        self.doctor[doctor.doctor_id] = doctor

    @log_action
    def book_appointment(self, patient_id, doctor_id, time_slot):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.time_slot = time_slot

        doctor = self.doctors[doctor_id]
        patient = self.patient[patient_id]
    
        if patient_id not in self.patient:
            raise PatientNotFoundError("Patient not found")
        
        if doctor_id not in self.doctor:
            raise DoctorNotFoundError("Doctor not found")
        
        if time_slot not in doctor.available_slots:
            raise SlotNotAvailableError("time slot not available")
        
    @log_action
    def cancel_appointment(self, appointment_id):
        if appointment_id not in self.appointments:
            raise AppointmentNotFoundError("Appointment not found")
        
        appointment = self.appointments[appointment_id]
        appointment.cancel()


    

