import os
import uuid

from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

from .models import *

def index(request):
    video = Video.objects.all()
    
    return render(request, "trial/index.html", {"videos":video})
    

def getId(request):
    Id = uuid.uuid4()
    return JsonResponse({"status":"ok", "id":Id})
    
    
def upload(request):
    if request.method == "POST":
        
        file = request.FILES.get("file")
        fileName = request.POST.get("fileName")
        fileSize = request.POST.get("fileSize")
        totalChunks = int(request.POST.get("totalChunks"))
        fileId = request.POST.get("fileId")
        chunkIndex = int(request.POST.get("chunkIndex"))
        
        video, created = Video.objects.get_or_create(
            fileId = fileId,
            defaults = {
                "fileName":fileName,
                "fileSize":fileSize,
                "totalChunks":totalChunks,
                
            }
        )
        
        if not created and (video.fileName != fileName and video.fileSize != fileSize):
            return JsonResponse({"error":"upload original file"})
        
            
            
        temPath = os.path.join(settings.MEDIA_ROOT, "tmps", f"{fileId}_{fileName}")
        os.makedirs(temPath, exist_ok=True)
        
        chunkPath = os.path.join(temPath, f"chunk_{chunkIndex}")
        
        with open(chunkPath, "wb") as chunk:
            for i in file.chunks():
                chunk.write(i)
        
        video.chunkIndex += 1
                
        
        if len(os.listdir(temPath)) == totalChunks:
          
          mainPath = os.path.join(settings.MEDIA_ROOT, "videos", f"{fileId}_{fileName}")
          os.makedirs(os.path.dirname(mainPath), exist_ok=True)
          
          with open(mainPath, "wb") as mainFile:
              for i in range(totalChunks):
                  
                  chunkFile = os.path.join(temPath, f"chunk_{i}")
                  with open(chunkFile, "rb") as fileCo:
                      mainFile.write(fileCo.read())
          
          for i in os.listdir(temPath):
              os.remove(os.path.join(temPath,i))
          os.rmdir(temPath)
          
          video.path = f"videos/{fileId}_{fileName}"
          
          video.is_finished = True
          
          video.save()
          
          return JsonResponse({"status":"completed", "url":video.path.url})
        video.save()
        return JsonResponse({"status":"received"})
    else:
        return JsonResponse({"error":"invalid request"})