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