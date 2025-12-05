from pydantic import BaseModel,Field
from fastapi import FastAPI
import pickle
import numpy as np

app = FastAPI()

class PredictionData(BaseModel):
    Return: float
    Volatility: float
    Volume_change: float
    Roll_5: float
    Roll_10: float
    MA_Ratio: float

class PredictionResponse(BaseModel):
    Prediction: int=Field(ge=0,le=1)
    PredictionLabel: str
    Probability:list[float]
    Confidence: float

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('/predict',response_model=PredictionResponse)
async def predict(data:PredictionData):
    ary=np.array([[data.Return,data.Volatility,data.Volume_change,data.Roll_5,data.Roll_10,data.MA_Ratio]])
    with open('model2.pkl',mode='rb') as f:
        model2=pickle.load(f)
    return PredictionResponse(
        Prediction=model2.predict(ary)[0],
        PredictionLabel= 'UP' if model2.predict(ary)[0]==1 else 'Down',
        Probability=model2.predict_proba(ary)[0],
        Confidence=max(model2.predict_proba(ary)[0])
    )
