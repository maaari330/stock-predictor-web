from pydantic import BaseModel,Field
from fastapi import FastAPI
import pickle
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import model_predict

app = FastAPI()

origin=['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionData(BaseModel):
    Ticker: str

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
    print(data)
    model_predict.calc(data.Ticker)
    return PredictionResponse(
        Prediction=model2.predict(ary)[0],
        PredictionLabel= 'UP' if model2.predict(ary)[0]==1 else 'Down',
        Probability=model2.predict_proba(ary)[0],
        Confidence=max(model2.predict_proba(ary)[0])
    )
