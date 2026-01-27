from rest_framework import serializers

class TickerSerializers(serializers.Serializer):
    ticker=serializers.CharField(required=True)
    symbol=serializers.CharField(required=True)
    model_id = serializers.IntegerField(required=False)

class TrainSerializers(serializers.Serializer):
    ticker=serializers.CharField(required=True)
    fx=serializers.CharField(required=True)