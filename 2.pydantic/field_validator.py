from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_banks = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_banks:
            raise ValueError('Not a valid bank email domain')
        
        return value  # 🔁 You must return the value
    
    @field_validator('name')
    @classmethod
    def tranform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode= 'after')
    # if here we take mode as after that means we will be assigning the str value to compare '<=>' thus raising an error.
    @classmethod
    def validate_age(cls, value):
      if 0< value <100:
          return value
      else:
          raise ValueError('Age should be in btween 0 and 100')


# any new changes we want in we can easily add here like weight, bmi etc.   
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('inserted to DB')
    print(patient.email)

patient_info = {'name':'Danish', 'email': 'danish@hdfc.com', 'age': '12', 'weight': 90.0, 'married': True, 'allergies':['pollen', 'dust'], 'contact_details':{'phone':'33432636'}}

# dictionary is unpacked by below double star method
patient1 = Patient(**patient_info)
insert_patient(patient1)