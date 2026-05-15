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