from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title= 'Name of the Patient', description='Write name in Block letters')]
    age: int = Field(gt=0, lt=100)
    weight:Annotated[float , Field(gt=0, strict=True)]
    married: bool = False
    email: EmailStr

    # To make any field optional we import optional from typing module and use as shown below
    allergies: Optional[List[str]] 
    
    #two str values bcs key and value both are string
    contact_details: Dict[str, str]

# any new changes we want in we can easily add here like weight, bmi etc.   
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('inserted to DB')
    print(patient.weight)

patient_info = {'name':'Danish', 'email': 'danish@gmail.com', 'age': '12', 'weight': 90.0, 'married': True, 'allergies':['pollen', 'dust'], 'contact_details':{'phone':'33432636'}}

# dictionary is unpacked by below double star method
patient1 = Patient(**patient_info)
insert_patient(patient1)