from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data  # <- This was missing

@app.get("/")
def hello():
    return {'message': 'Patient management system API'}

@app.get("/about")
def about():
    return {'message': 'Fully functional API to manage your patient record'}

@app.get("/view")
def view():
    data = load_data()
    return data  # <- Now returns actual JSON content

# note - But data is a list of patient dictionaries, 
# not a dictionary keyed by patient_id. So data[patient_id] gives a KeyError.(thus we using loop)



@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001' )):
    data = load_data()

    # Search for the patient in the list
    for patient in data:
        if patient["id"] == patient_id:
            return patient

    # return {"error": "Patient not found"}
    raise HTTPException(status_code=404, detail='patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort on the basis of height, age or bmi'), order: str = Query('asc', description='sort in ascending or descending order')):

    valid_fields = ['height','age', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail= f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order == 'desc' else False
    # error I faced below is data is a list, not a dictionary, you should remove .values() [data.values() is incorrect]
    sort_data = sorted(data, key=lambda x:x.get(sort_by, 0), reverse= sort_order)

    return sort_data