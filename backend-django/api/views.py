from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TickerSerializers,TrainSerializers
from .model_predict import model_predict
from .train_model import train_model
from .get_stock_chart import get_stock_chart
from .models import TrainedModel

def home(request):
    json_data= {"message": "Hello"}
    return Response(data=json_data,status=status.HTTP_200_OK)

@api_view(["POST"])
def predict(request):
    ticker_serializer=TickerSerializers(data=request.data)
    if ticker_serializer.is_valid():
        validate_test_data=ticker_serializer.validated_data
        test_response=model_predict(validate_test_data.get("ticker"),validate_test_data.get("symbol"),validate_test_data.get("model_id"))
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

@api_view(["GET"])
def show_stock_chart(request):
    ticker=request.query_params.get("ticker")
    metric=request.query_params.get("metric")
    start=request.query_params.get("start")
    end=request.query_params.get("end")
    competitor=request.query_params.get("competitor")
    if competitor:
        show_competitor_response= get_stock_chart(competitor,metric,start,end)
    else:
        show_competitor_response=None
    show_stock_response= get_stock_chart(ticker,metric,start,end)
    response={"main":show_stock_response,"competitor":show_competitor_response}
    return Response(response,status=status.HTTP_200_OK)

@api_view(["GET"])
def show_models(request):
    latest_models_list=TrainedModel.objects.all().order_by("-id")
    list_except_model=[{"id": m.id,"ticker": m.ticker,"fx": m.fx,"trained_at": m.trained_at,"threshold": m.threshold,} for m in latest_models_list]
    return Response(list_except_model,status=status.HTTP_200_OK)