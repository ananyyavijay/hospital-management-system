from exceptions.hms_exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
    SlotNotAvailableError,
    AppointmentNotFoundError
)
from utils.decorators import log_action
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment


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

    def __str__(self):

        return f"""
        Hospital Summary
        Total Patients     : {len(self.patients)}
        Total Appointments : {len(self.appointments)}
        """

    def admin_report(self):

        print(f"Hospital has {len(self.patients)} patients")

        print(f"Hospital has {len(self.doctors)} doctors")

        print(f"Hospital has {len(self.appointments)} appointments")