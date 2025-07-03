from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    contact_details: Dict[str,str]

# Below code checks if the patient above the age 60 has an emergency contact or not
    @model_validator(mode='after')
    def emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details: 
            raise ValueError('Patient older than 60 must have an emergency contact')
        
        return model
    
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('inserted to DB')
    print(patient.weight)

patient_info = {'name':'Danish', 'email': 'danish@gmail.com', 'age': '92', 'weight': 90.0, 'married': True, 'allergies':['pollen', 'dust'], 'contact_details':{'phone':'33432636', 'emergency': '3297432'}}

# dictionary is unpacked by below double star method
patient1 = Patient(**patient_info)
insert_patient(patient1)    