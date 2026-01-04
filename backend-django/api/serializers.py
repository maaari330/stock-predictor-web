from rest_framework import serializers

class TickerSerializers(serializers.Serializer):
    ticker=serializers.CharField(required=True)
    days=serializers.IntegerField(required=True,min_value=1)