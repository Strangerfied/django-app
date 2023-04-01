# from django.shortcuts import render
# from rest_framework import viewsets
from bson import json_util
from django.http import HttpResponse
from django.http import JsonResponse
import json
from bson.json_util import dumps
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
from django.contrib.auth.decorators import login_required
#testin
# from .serializers import HeroSerializer
# from .models import Hero
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

import pymongo

# from django.conf import settings

client = pymongo.MongoClient(
    "mongodb+srv://admin2:poolcool@cluster1.syijvpg.mongodb.net/?retryWrites=true&w=majority"
)

dbname = client["eduClimateAnalysis"]

collection = dbname["climateData"]

collection1 = dbname["stations"]


collection2 = dbname["users"]

# Create your views here.

def MaxRain(request):
    if request.method == "GET":
        cursor = (
            collection.find({}, {"_id": 0, "Time": 1, "Precipitation mm/h": 1})
            .sort([("Precipitation mm/h", pymongo.DESCENDING)])
            .limit(1)
        )
        list_cur = list(cursor)
        if list_cur:
            data = {
                "Time": list_cur[0]["Time"],
                "Precipitation": list_cur[0]["Precipitation mm/h"],
            }
            response_data = {
                "status": "success",
                "message": "Retrieved document containing highest precipitation:",
                "data": data,
            }
        else:
            response_data = {"status": "error", "message": "No document found."}
        return JsonResponse(response_data, safe=False)

