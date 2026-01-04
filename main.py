from pydantic import BaseModel,Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import model_predict

app = FastAPI()

origins=['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionData(BaseModel):
    Ticker: str
    Days: int

class PredictionResponse(BaseModel):
    Prediction: int=Field(ge=0,le=1)
    PredictionLabel: str
    Confidence: float= Field(ge=0.0, le=1.0)

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('predict/',response_model=PredictionResponse)
async def predict(data:PredictionData):
    res=model_predict.model_predict(data.Ticker, period=f"{data.Days}d")
    return PredictionResponse(
        Prediction=res['Prediction'],
        PredictionLabel= res['PredictionLabel'],
        Confidence=res['Confidence']
    )
