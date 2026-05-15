from dataclasses import dataclass, field
from typing import List

@dataclass
class Doctor:
    name: str
    specialization: str
    doctor_id: str
    available_slots: List[str] = field(default_factory=list)
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.doctor_id.startswith('D'):
            raise ValueError("Invalid Doctor Id")

        if not self.name:
            raise ValueError("Name is required")

    def add_slot(self, slot: str) -> None:
        self.available_slots.append(slot)

    def remove_slot(self, slot: str) -> bool:
        if slot in self.available_slots:
            self.available_slots.remove(slot)
            return True
        return False
    
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