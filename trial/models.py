from django.db import models

class Video(models.Model):
    fileId = models.CharField(max_length=500)
    fileName = models.CharField(max_length=600)
    fileSize = models.BigIntegerField()
    totalChunks = models.IntegerField(default=0)
    chunkIndex = models.IntegerField(default=0)
    path = models.FileField(upload_to="videos")
    is_finished = models.BooleanField(default=False)
    
    #Create your models here.
