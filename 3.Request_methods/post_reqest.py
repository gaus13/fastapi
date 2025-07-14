from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json
import os

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


# ---------- Utility Functions ----------

DATA_FILE = 'patient.json'

# Ensure file exists
def ensure_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)  # Start with empty list

# Load patient list from file
def load_data():
    ensure_file()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save patient list to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ---------- API Endpoint ----------

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    # Check if patient already exists
    for p in data:
        if p['id'] == patient.id:
            raise HTTPException(status_code=400, detail='Patient already exists')

    # Add new patient
    data.append(patient.model_dump())

    # Save updated data
    save_data(data)

    return {
        "message": "Patient created successfully",
        "bmi": patient.bmi,
        "verdict": patient.verdict
    }
