from dataclasses import dataclass, field
from typing import List

@dataclass
class Patient:
    name: str
    blood_group: str
    patient_id: str
    age: int = 0
    medical_history: List[str] = field(default_factory=list)
    is_active: bool = True
    
    def __post_init__(self) -> None:
        if not self.patient_id.startswith('P'):
            raise ValueError("Invalid Patient Id")
            
        if not self.name :
            raise ValueError("Name is required")

        if self.age < 0:
            raise ValueError("age cannot be less then 0")
        

    def add_record(self, record: str) -> None:
        self.medical_history.append(record)
        

    def get_history(self) -> str:
        if not self.medical_history:
            return "No records found"

        result = []
            
        for index, record in enumerate(self.medical_history, start=1):
            result.append(f"{index}.{record}")
        return "\n".join(result)