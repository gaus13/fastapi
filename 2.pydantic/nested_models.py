from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Dict, Optional, Annotated

# we create pydantic model for address
class Address(BaseModel):
    city: str
    state: str
    pin: str


# You need to make sure patient_dict contains all required fields expected by your Patient model.
class Patient(BaseModel):
    name: str
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'Haryana', 'pin': '322211'}
address1 = Address(**address_dict)  

patient_dict = {'name':'Danish', 'gender':'male', 'age':42, 'address': address1}
patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.address.city)