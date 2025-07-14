from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json



app = FastAPI()

# ---------- Patient Model ----------
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Id of the patient', examples=['P002'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description='Height of the Patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in Kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        else:
            return 'overweight'


class PatientUpdate(BaseModel):
   

   name: Annotated[Optional[str], Field(default=None)]
   age: Annotated[Optional[int], Field(default=None)]
   gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
   height: Annotated[Optional[float], Field(default=None, gt = 0)]
   weight: Annotated[Optional[float], Field(default=None, gt = 0 )]

Loading_data = 'patient.json'

def load_data():
    with open(Loading_data, 'r') as f:
     return json.load(f)

def save_data(data):
    with open(Loading_data, 'w') as f:
        json.dump(data, f, indent=2)   


@app.put('/edit/{patient_id}')
def update_patient(patient_id :str, patient_update: PatientUpdate):
   data = load_data()

   if patient_id not in data:
      raise HTTPException(status_code=404, detail= 'Patient not found')
   
   existing_patient_info = data[patient_id]

   updated_patient_info = patient_update.model_dump(exclude_unset = True)

   for key , value in updated_patient_info.items():
      existing_patient_info[key] = value

# The problem is with change in data such as weight the BMI and Verdict also changes
# to make sure it is re-calculated we'll use the below flow
# existing_patient_info -> convert to pydantic object -> this will update BMI + VERDICT ->

   existing_patient_info['id'] = patient_id
   patient_pydantic_obj = Patient(**existing_patient_info)

#  now pydantic obj back to dict and then save.
   existing_patient_info= patient_pydantic_obj.model_dump(exclude='id')

# Add this above dict to data
   data[patient_id] = existing_patient_info

   save_data(data)

   return JSONResponse(status_code = 200, content = {'message':'Patient Information Updated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load the patient data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail= "Patient not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': "Patient {patient_id} deleted"})