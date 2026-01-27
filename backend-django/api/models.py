from django.db import models

# Create your models here.
class TrainedModel(models.Model):
    ticker = models.CharField(max_length=20)
    fx     = models.CharField(max_length=20)
    trained_at = models.DateTimeField(auto_now_add=True)
    model_data = models.BinaryField()     
    threshold  = models.FloatField()    
    feature_cols = models.JSONField()