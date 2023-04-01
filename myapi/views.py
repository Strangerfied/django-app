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


# now it updates the longitude and latitude based on object ID :D
@login_required
@csrf_exempt
def update_weather_station(request):
    # Check if request method is PUT
    if request.method == "PUT":
        
        # Check if user is authenticated as manager or admin
        if not request.user.is_authenticated or not (
            request.user.is_staff or request.user.is_superuser
        ):
            return JsonResponse({"error": "Unauthorized access."}, status=401)
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


def GetStationData(request):
    if request.method == "GET":
        """
        # Check if user is authenticated as manager or admin
        if not request.user.is_authenticated or not (
            request.user.is_staff or request.user.is_superuser
        ):
            return JsonResponse({"error": "Unauthorized access."}, status=401)"""
        # Load the request body as a JSON string
        body = json.loads(request.body.decode("utf-8"))

        # Get the station name and date time from the request body
        station_name = body.get("Device Name", "")
        date_time_str = body.get("Time", "")

        # Convert date_time string to datetime object in ISO 8601 format
        try:
            date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%f%z")

        except ValueError:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Invalid query parameter. Time is required.",
                }
            )

        # Query the collection for the specified station and date/time
        result = collection.find_one(
            {"Device Name": station_name, "Time": date_time_obj},
            {
                "Temperature (°C)": 1,
                "Atmospheric Pressure (kPa)": 1,
                "Solar Radiation (W/m2)": 1,
                "Precipitation mm/h": 1,
                "_id": 0,
            },
        )

        # If the query returned a result, return the data as JSON
        if result:
            return JsonResponse({"status": "success", "data": result})
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "No data found for the specified station and date/time.",
                }
            )
    else:
        return JsonResponse(
            {
                "status": "error",
                "message": "Invalid request method. Only GET and POST methods are allowed.",
            }
        )


def index(request):
    return HttpResponse("<h1>Hello this is the django</h1>")


@csrf_exempt
def TheModelView(request):
    if request.method == "GET":
        """
        # Check if user is authenticated as manager or admin
        if not request.user.is_authenticated or not (
            request.user.is_staff or request.user.is_superuser
        ):
            return JsonResponse({"error": "Unauthorized access."}, status=401)"""
        cursor = collection.find().limit(1)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("nJson Data:", json_data)
        return JsonResponse(json_data, safe=False)

    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        print(body)
        newrecord = {"name": body["name"], "year": body["year"]}
        print(newrecord)
        x = collection.insert_one(newrecord)
        data = dumps(newrecord)
        return JsonResponse(data, safe=False)


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


@csrf_exempt
# @user_passes_test(lambda user: user.is_superuser)
def Users(request):
    if request.method == "POST":
        """
        # Check if user is authenticated as manager or admin
        if not request.user.is_authenticated or not (
            request.user.is_staff or request.user.is_superuser
        ):
            return JsonResponse({"error": "Unauthorized access."}, status=401)"""
        body = json.loads(request.body.decode("utf-8"))
        newuser = {
            "Access Level": body["Access Level"],
            "Last Login": body["Last Login"],
            "First Name": body["First Name"],
            "Password": body["Password"],
            "User Name": body["User Name"],
            "Surname": body["Surname"],
            "Email": body["Email"],
        }
        x = collection2.insert_one(newuser)
        newuser["_id"] = str(x.inserted_id)  # Convert ObjectId to string
        response_data = {
            "status": "success",
            "message": "New user added successfully",
            "data": newuser,
        }

        return JsonResponse(response_data, status=201)

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            user_ids = data.get("_id", [])
            if not user_ids:
                return JsonResponse(
                    {"message": "Please provide at least one valid _id."}
                )
            deleted_count = 0
            not_found_count = 0
            for user_id in user_ids:
                result = collection2.delete_one({"_id": ObjectId(user_id)})
                if result.deleted_count > 0:
                    deleted_count += 1
                else:
                    not_found_count += 1
            if deleted_count > 0:
                message = f"{deleted_count} user(s) have been deleted."
                if not_found_count > 0:
                    message += f" {not_found_count} _id(s) not found in the database."
                return JsonResponse({"message": message})
            else:
                return JsonResponse({"message": "No user(s) were found."})
        except:
            return JsonResponse({"message": "Invalid payload format or _id."})


@csrf_exempt
def WeatherData(request):
    if request.method == "PUT":
        """
        # Check if user is authenticated as manager or admin
        if not request.user.is_authenticated or not (
            request.user.is_staff or request.user.is_superuser
        ):
            return JsonResponse({"error": "Unauthorized access."}, status=401)"""
        # body = json.loads(request.body.decode('utf-8'))

        x = collection.update_one(
            {"_id": "ObjectID('641a51cc26927432b74c0776')"},
            {"$set": {"Device_ID": "test device id"}},
        )

    data = {"Fahrenheit": "96"}
    return JsonResponse(data, safe=False)


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


@csrf_exempt
def AddFahrenheitTemps(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            document_ids = data.get("_id", [])
            result = []
            for document_id in document_ids:
                # Convert the string document_id to ObjectId
                obj_id = ObjectId(document_id)

                # Get the temperature document from the collection
                temp = collection.find_one(
                    {"_id": obj_id, "Temperature (°C)": {"$exists": True}}
                )

                # If the document exists and has a temperature field, update it with Fahrenheit values
                if temp:
                    celsius_temp = temp["Temperature (°C)"]
                    fahrenheit_temps = celsius_temp * 1.8 + 32
                    collection.update_one(
                        {"_id": obj_id}, {"$set": {"Fahrenheit": fahrenheit_temps}}
                    )
                    result.append(
                        {
                            "status": "success",
                            "message": f"Temperature record with ID {document_id} updated with Fahrenheit values.",
                        }
                    )
                else:
                    result.append(
                        {
                            "status": "error",
                            "message": f"Temperature record with ID {document_id} not found or missing 'Temperature (°C)' field.",
                        }
                    )
            return JsonResponse(result, safe=False)
        except:
            return JsonResponse(
                {"status": "error", "message": "Invalid payload format or document ID."}
            )


def GetTemperatures(request):
    if request.method == "GET":
        try:
            # Get the limit and skip values from the request parameters, or use default values
            limit = int(request.GET.get("limit", 10))
            skip = int(request.GET.get("skip", 0))

            # Retrieve the temperature documents from the collection using batchSize operation
            temps = []
            for temp in collection.find().batch_size(5).limit(limit).skip(skip):
                temps.append(
                    {
                        "_id": str(temp["_id"]),
                        "Temperature (°C)": temp["Temperature (°C)"],
                    }
                )

            # Return the temperatures as a JSON response
            return JsonResponse({"status": "success", "temperatures": temps})
        except:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "An error occurred while retrieving temperature records.",
                }
            )


def IndexQuery(request, index_value):
    if request.method == "GET":
        # Create an index on the specified field
        collection.create_index(index_value)

        # Perform the query using the created index
        result = collection.find({index_value: {"$gt": 5}}).hint(index_value)

        # Serialize the result to JSON and return as a response
        json_data = json_util.dumps(result)
        return JsonResponse(json.loads(json_data), safe=False)


@csrf_exempt
# @user_passes_test(lambda user: user.is_superuser)
def update_access_level(request):
    if request.method == "PUT":
        user_names = request.GET.getlist("user_name")
        access_level = request.GET.get("access_level")
        result = collection2.update_many(
            {"User Name": {"$in": user_names}}, {"$set": {"Access Level": access_level}}
        )
        if result.modified_count > 0:
            return JsonResponse(
                {"message": f"Access level updated for {result.modified_count} users"}
            )
        else:
            return JsonResponse({"message": f"No users were found"})


# FML i made this update an existing weather station based on longitude and latitude input :facepalm
"""
@csrf_exempt
def update_weather_station(request):
    if request.method == "PUT":
        # Parse the request body and extract the longitude and latitude values
        data = json.loads(request.body.decode("utf-8"))
        try:
            longitude = float(
                data.get(
                    "Longitude",
                )
            )
            latitude = float(
                data.get(
                    "Latitude",
                )
            )
        except ValueError:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Invalid longitude or latitude value. Must be a float.",
                }
            )

        state = data.get("State", "")
        is_new_station = data.get("IsNewStation", "")
        last_reading = data.get("LastReading", "")
        station_code = data.get("StationCode", "")
        station_name = data.get("StationName", "")

        # Query the collection for the specified longitude and latitude
        result = collection1.find_one(
            {"Longitude": longitude, "Latitude": latitude}, {"_id": 1}
        )

        if result:
            # Update the document with the new field values
            update_result = collection1.update_one(
                {"_id": result["_id"]},
                {
                    "$set": {
                        "State": state,
                        "IsNewStation": is_new_station,
                        "LastReading": last_reading,
                        "StationCode": station_code,
                        "StationName": station_name,
                    }
                },
            )
            if update_result.modified_count == 1:
                return JsonResponse(
                    {"message": f"Weather station {result['_id']} updated successfully"}
                )
            else:
                return JsonResponse(
                    {"message": f"Failed to update weather station {result['_id']}"}
                )
        else:
            return JsonResponse(
                {
                    "message": "No weather station found for the specified longitude and latitude"
                }
            )
"""
