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
import random
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

@csrf_exempt
def Stations(request):
    """
    # Check if user is authenticated as manager or admin
    if not request.user.is_authenticated or not (
        request.user.is_staff or request.user.is_superuser
    ):
        return JsonResponse({"error": "Unauthorized access."}, status=401)"""
    if request.method == "GET":
        cursor = collection1.find().limit(1)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("nJson Data:", json_data)
        return JsonResponse(json_data, safe=False)

    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        print(body)
        newstation = {
            "Latitude": body["Lat"],
            "Longitude": body["Long"],
            "State": body["State"],
            "IsNewStation": body["IsNew"],
            "StationCode": body["Code"],
            "StationName": body["Name"],
        }
        x = collection1.insert_one(newstation)
        newstation["_id"] = str(x.inserted_id)  # Convert ObjectId to string
        
        state = newstation['State']
        station_count = collection1.count_documents({'State': state})
        
        while station_count < 10:
            station_name = f"Station {station_count + 1}"
            station_location = {
                "coordinates": [
                    random.uniform(-180, 180),
                    random.uniform(-90, 90),
                ],
            }
            newstations = {
                "Latitude": station_location["coordinates"][1],
                "Longitude": station_location["coordinates"][0],
                "State": state,
                "IsNewStation": True,
                "LastReading": datetime.now(),
                "StationCode": str(station_count + 1),
                "StationName": station_name,
            }
            collection1.insert_one(newstations)
            station_count += 1
        
        stations = collection1.find({"State": state})
        
        stations_data = [
            {
                "StationName": station["StationName"],
                "StationCode": station["StationCode"],
                "Latitude": station["Latitude"],
                "Longitude": station["Longitude"],
            }
            for station in stations
        ]
        
        response_data = {
            "status": "success",
            "message": "New station/s added successfully",
            "data": {
                "new station": newstation,
                "stations": stations_data
            },
        }
        return JsonResponse(response_data, status=201)
    
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

    if request.method == "PUT":

        """# Check if user is authenticated as manager or admin
        if not request.user.is_authenticated or not (
            request.user.is_staff or request.user.is_superuser
        ):
            return JsonResponse({"error": "Unauthorized access."}, status=401)"""
        data = json.loads(request.body)

        station_id = data.get("_id")

        if not station_id:
            return JsonResponse(
                {"error": "Weather station ID is required."}, status=400
            )
        station = collection1.find_one({"_id": ObjectId(station_id)})
        if not station:
            return JsonResponse({"error": "Weather station not found."}, status=404)

        longitude = data.get("Longitude")
        latitude = data.get("Latitude")
        if longitude is not None and latitude is not None:
            collection1.update_one(
                {"_id": ObjectId(station_id)},
                {"$set": {"Longitude": longitude, "Latitude": latitude}},
            )
        return JsonResponse(
            {"message": f"Weather station {station_id} updated successfully."},
            status=200,
        )
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

