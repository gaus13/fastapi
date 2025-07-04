from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float  # in kg
    height: float  # in meters
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('BMI:', patient.bmi)
    print(patient.email)

patient_info = {
    'name': 'Danish',
    'email': 'danish@hdfc.com',
    'age': '12',
    'weight': 90.0,
    'height': 1.80,
    'allergies': ['pollen', 'dust'],  # This will be ignored (not in model)
    'contact_details': {'phone': '33432636'}
}

patient1 = Patient(**patient_info)
insert_patient(patient1)
