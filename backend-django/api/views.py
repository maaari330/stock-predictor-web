from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TickerSerializers,TrainSerializers
from .model_predict import model_predict
from .train_model import train_model

def home(request):
    json_data= {"message": "Hello"}
    return Response(data=json_data,status=status.HTTP_200_OK)

@api_view(["POST"])
def predict(request):
    ticker_serializer=TickerSerializers(data=request.data)
    if ticker_serializer.is_valid():
        validate_test_data=ticker_serializer.validated_data
        test_response=model_predict(validate_test_data.get("ticker"),validate_test_data.get("symbol"),f"{validate_test_data.get("days")}d")
        return Response(test_response,status=status.HTTP_200_OK)
    return Response(ticker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def train(request):
    train_serializer=TrainSerializers(data=request.data)
    if train_serializer.is_valid():
        validate_train_data=train_serializer.validated_data
        train_model(validate_train_data.get("ticker"),validate_train_data.get("fx"))
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)