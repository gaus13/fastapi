from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd

# import the ml model
with open('model.pkl', 'rb') as f:

    model = pickle.load(f)


app = FastAPI()

# Tier 1 Cities
tier_1_cities = [ "Mumbai",
    "Delhi",
    "Bengaluru",
    "Chennai",
    "Kolkata",
    "Hyderabad",
    "Pune",
    "Ahmedabad"
    
]

# Tier 2 Cities
tier_2_cities = [
    "Jaipur",
    "Lucknow",
    "Nagpur",
    "Indore",
    "Chandigarh",
    "Coimbatore",
    "Visakhapatnam",
    "Bhopal",
    "Vadodara",
    "Ludhiana"
]


# pydantic model to validate data
class userInput(BaseModel):
    age: Annotated[int , Field(..., gt= 0, lt= 100, description='Age of the user')]
    height: Annotated[float, Field(..., gt = 0, description='Height of the user in meters')]
    weight:  Annotated[float, Field(..., gt = 0, description='weight of the user in Kgs')]
    income_lpa: Annotated[float, Field(..., gt=0, description= 'Income of the user in LPA')]
    smoker:Annotated[Literal['yes', 'no'], Field(...,description='If the person is smoker')]
    city: Annotated[str, Field(..., description="The city you belong to ")]
    occupation:Annotated[Literal['retired','freelancer', 'student', 'government Job'], Field(..., description= "Occupation of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
      return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
       if self.smoker and self.bmi > 30:
          return "High risk"
       elif self.smoker and self.bmi > 27:
          return "Medium risk"
       else:
          return "Low risk"
       
    @computed_field   
    @property
    def age_group(self) -> str:
       if self.age < 25:
          return "Young"
       elif self.age < 45:
          return "Adult"
       elif self.age < 60:
          return "mid_aged"
       return "senior citizen"
    
    @computed_field   
    @property
    def city_tier(self) -> int:
       if self.city in tier_1_cities:
          return 1
       elif self.city in tier_2_cities:
          return 2
       else:
          return 3
       

@app.post('/predict')
def predict_premium(data: userInput):
    input_df = pd.DataFrame([{
       'bmi': data.bmi,
       'age_group': data.age_group,
       'lifestyle_risk': data.lifeStyle_risk,
       'city_tier': data.city_tier,
       'income_lpa': data.income_lpa,
       'occupation': data.occupation
    }])
   
    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'Predicted_category': prediction})