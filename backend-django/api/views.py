from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TickerSerializers
from .model_predict import model_predict

def home(request):
    json_data= {"message": "Hello"}
    return Response(data=json_data,status=status.HTTP_200_OK)

@api_view(['POST'])
def predict(request):
    serializer=TickerSerializers(data=request.data)
    if serializer.is_valid():
        res=model_predict(serializer.validated_data.get("ticker"),f"{serializer.validated_data.get("days")}d")
        return Response(res,status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)