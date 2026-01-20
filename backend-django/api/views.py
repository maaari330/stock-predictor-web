from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .serializers import TickerSerializers,TrainSerializers
from .model_predict import model_predict
from .train_model import train_model

def home(request):
    json_data= {"message": "Hello"}
    return Response(data=json_data,status=status.HTTP_200_OK)

@api_view(["POST"])
def predict(request):
    ticker_serializer=TickerSerializers(data=request.data)
    validate_test_data=ticker_serializer.validated_data
    if ticker_serializer.is_valid():
        test_response=model_predict(validate_test_data.get("ticker"),f"{validate_test_data.get("days")}d")
        return Response(test_response,status=status.HTTP_200_OK)
    return Response(ticker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def train(request):
    train_serializer=TrainSerializers(data=request.data)
    validate_train_data=train_serializer.validated_data
    if train_serializer.is_valid():
        train_model(validate_train_data.get("ticker"),validate_train_data.get("fx"))
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)