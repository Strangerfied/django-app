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

@csrf_exempt
def WeatherStation(request):
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
            "LastReading": body["LastRead"],
            "StationCode": body["Code"],
            "StationName": body["Name"],

        }
        x = collection1.insert_one(newstation)
        newstation["_id"] = str(x.inserted_id)  # Convert ObjectId to string
        response_data = {
            "status": "success",
            "message": "New station added successfully",
            "data": newstation,
        }

        return JsonResponse(response_data, status=201)
    if request.method == "PUT":

        """# Check if user is authenticated as manager or admin
        if not request.user.is_authenticated or not (
            request.user.is_staff or request.user.is_superuser
        ):
            return JsonResponse({"error": "Unauthorized access."}, status=401)"""
        # Get the JSON object from request body
        data = json.loads(request.body)

        # Get the ID of the weather station to be updated
        station_id = data.get("_id")

        # Check if the station ID is provided
        if not station_id:
            return JsonResponse(
                {"error": "Weather station ID is required."}, status=400
            )

        # Check if the station exists
        station = collection1.find_one({"_id": ObjectId(station_id)})
        if not station:
            return JsonResponse({"error": "Weather station not found."}, status=404)

        # Update the longitude and latitude values
        longitude = data.get("Longitude")
        latitude = data.get("Latitude")
        if longitude is not None and latitude is not None:
            collection1.update_one(
                {"_id": ObjectId(station_id)},
                {"$set": {"Longitude": longitude, "Latitude": latitude}},
            )

        # Return a success response
        return JsonResponse(
            {"message": f"Weather station {station_id} updated successfully."},
            status=200,
        )

    else:
        # Return an error response for invalid request method
        return JsonResponse({"error": "Invalid request method."}, status=405)

