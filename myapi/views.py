#from django.shortcuts import render
#from rest_framework import viewsets
from bson import json_util
from django.http import HttpResponse
from django.http import JsonResponse
import json
from bson.json_util import dumps
from bson import ObjectId
from datetime import datetime
#from .serializers import HeroSerializer
#from .models import Hero
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import pymongo
#from django.conf import settings

client = pymongo.MongoClient("mongodb+srv://admin2:poolcool@cluster1.syijvpg.mongodb.net/?retryWrites=true&w=majority")

dbname = client['eduClimateAnalysis']

collection = dbname['climateData']

collection1 = dbname['stations']


collection2 = dbname['users']

               
def index(request):
    return HttpResponse("<h1>Hello this is the django</h1>")

@csrf_exempt
def TheModelView(request):
    if(request.method == "GET"):
        cursor = collection.find().limit(1)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("nJson Data:", json_data)
        return JsonResponse(json_data, safe=False)
    
    if(request.method == "POST"):
        body = json.loads(request.body.decode("utf-8"))
        print(body)
        newrecord = {
                "name": body['name'],
                "year": body['year']
                }
        print(newrecord)
        x = collection.insert_one(newrecord)
        data = dumps(newrecord)                                
        return JsonResponse(data, safe=False)
                           
@csrf_exempt
def WeatherStation(request):
    
    if(request.method == "GET"):
        cursor = collection1.find().limit(1)
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("nJson Data:", json_data)
        return JsonResponse(json_data, safe=False)

    if(request.method == "POST"):
        body = json.loads(request.body.decode('utf-8'))
        print(body)                          
        newstation = {
                "Device_ID": body['deviceid'],
                "Device_Name": body['devicename'],
                "Latitude": body['latitude'],
                "Longitude": body['longitude'],
                "Location": body['location'],
                "State": body['state'],
                "Last_Reading": body['lastreading'],
                "New_Station": body['newstation']
                }
        x = collection1.insert_one(newstation)
        newstation['_id'] = str(x.inserted_id) # Convert ObjectId to string
        response_data = {
            'status': 'success',
            'message': 'New station added successfully',
            'data': newstation
            }
        
        return JsonResponse(response_data, status=201)

@csrf_exempt
def Users(request):

    if(request.method == "POST"):
        body = json.loads(request.body.decode('utf-8'))
        newuser = {
                "Access Level": body['accesslevel'],
                "Last Login": body['lastlogin'],
                "Name": body['name'],
                "Password": body['password'],
                "User Name": body['username']
                }
        x = collection2.insert_one(newuser)
        newuser['_id'] = str(x.inserted_id) # Convert ObjectId to string
        response_data = {
            'status': 'success',
            'message': 'New user added successfully',
            'data': newuser
            }

        return JsonResponse(response_data, status=201)

@csrf_exempt
def WeatherData(request):
    
    if(request.method == "PUT"):
    #body = json.loads(request.body.decode('utf-8'))
    

        x = collection.update_one({"_id": "ObjectID('641a51cc26927432b74c0776')"}, {"$set": {"Device_ID": "test device id"}})

    data = {"Fahrenheit": "96"}
    return JsonResponse(data, safe=False) 

@csrf_exempt
def MaxRain(request):
    json_data = {}
    if(request.method == "GET"):
        #cursor = collection.find_one(sort=[("Precipitation mm/h", -1)])
        #cursor = collection.find({}, {"TTN metadata": 0, "TTN payload fields": 0}).sort([("Precipitation mm/h", pymongo.DESCENDING)]).limit(1)
        #cursor = collection.find().limit(1)
        cursor = collection.find({}, {"_id": 1, "Precipitation mm/h": 1}).sort([("Precipitation mm/h", pymongo.DESCENDING)]).limit(1)
        print(cursor)
        list_cur = list(cursor)
        print(list_cur)
        #json_data = dumps(list_cur)
        print("nJSON data:", json_data)
        #return JsonResponse(json_data, safe=False)
        json_data = dumps(list_cur)
        response_data = {
            'status': 'success',
            'message': 'Retrieved document containing highest precipitation:',
            'data': json_data
            }

        return JsonResponse(response_data, safe=False)

@csrf_exempt
def AddFahrenheitTemps(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            document_ids = data.get('_id', [])
            result = []
            for document_id in document_ids:
                # Convert the string document_id to ObjectId
                obj_id = ObjectId(document_id)

                # Get the temperature document from the collection
                temp = collection.find_one({"_id": obj_id, "Temperature (°C)": {"$exists": True}})

                # If the document exists and has a temperature field, update it with Fahrenheit values
                if temp:
                    celsius_temp = temp["Temperature (°C)"]
                    fahrenheit_temps = {"Fahrenheit": celsius_temp * 1.8 + 32}
                    collection.update_one({"_id": obj_id}, {"$set": {"Fahrenheit": fahrenheit_temps}})
                    result.append({"status": "success", "message": f"Temperature record with ID {document_id} updated with Fahrenheit values."})
                else:
                    result.append({"status": "error", "message": f"Temperature record with ID {document_id} not found or missing 'Temperature (°C)' field."})
            return JsonResponse(result, safe=False)
        except:
            return JsonResponse({"status": "error", "message": "Invalid payload format or document ID."})

@csrf_exempt          
def GetStationData(request, station_name, date_time):

    # Convert date_time string to datetime object in ISO 8601 format
    date_time_obj = datetime.fromisoformat(date_time)

    # Query the collection for the specified station and date/time
    result = collection.find_one({
        "Device Name": station_name,
        "Time": date_time_obj
    }, {
        "Temperature (°C)": 1,
        "Atmospheric Pressure (kPa)": 1,
        "Solar Radiation (W/m2)": 1,
        "Precipitation (mm/h)": 1,
        "_id": 0
    })

    # If the query returned a result, return the data as JSON
    if result:
        return JsonResponse({"status": "success", "data": result})
    else:
        return JsonResponse({"status": "error", "message": "No data found for the specified station and date/time."})

def GetTemperatures(request):
    if request.method == "GET":
        try:
            # Get the limit and skip values from the request parameters, or use default values
            limit = int(request.GET.get("limit", 10))
            skip = int(request.GET.get("skip", 0))

            # Retrieve the temperature documents from the collection using batchSize operation
            temps = []
            for temp in collection.find().batch_size(5).limit(limit).skip(skip):
                temps.append({"_id": str(temp["_id"]), "Temperature (°C)": temp["Temperature (°C)"]})
            
            # Return the temperatures as a JSON response
            return JsonResponse({"status": "success", "temperatures": temps})
        except:
            return JsonResponse({"status": "error", "message": "An error occurred while retrieving temperature records."})

def IndexQuery(request, index_value):
    if request.method == "GET":
        # Create an index on the specified field
        collection.create_index(index_value)

        # Perform the query using the created index
        result = collection.find({index_value: {'$gt': 5}}).hint(index_value)

        # Serialize the result to JSON and return as a response
        json_data = json_util.dumps(result)
        return JsonResponse(json.loads(json_data), safe=False)

@csrf_exempt
def delete_user(request, user_name):
    if request.method == "DELETE":
        result = collection2.delete_one({'User Name': user_name})
        if result.deleted_count == 1:
            return JsonResponse({'message': f"{user_name} has been deleted"})
        else:
            return JsonResponse({'message': f"{user_name} was not found"})
# Create your views here.

@csrf_exempt
def delete_users(request):
    if request.method == "DELETE":
        user_names = request.GET.getlist('User Name')
        result = collection2.delete_many({'User Name': {'$in': user_names}})
        if result.deleted_count > 0:
            return JsonResponse({'message': f"{result.deleted_count} users have been deleted"})
        else:
            return JsonResponse({'message': f"No users were found"})

@csrf_exempt
def update_weather_station(request, station_id):
    if request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        if "longitude" in data and "latitude" in data:
            result = collection1.update_one({"_id": ObjectId(station_id)}, {"$set": {"longitude": data["longitude"], "latitude": data["latitude"]}})
            if result.modified_count == 1:
                return JsonResponse({'message': f"Weather station {station_id} updated successfully"})
            else:
                return JsonResponse({'message': f"Weather station {station_id} was not found"})
        else:
            return JsonResponse({'message': f"Both longitude and latitude are required"})

@csrf_exempt
def update_access_level(request):
    if request.method == "PUT":
        user_names = request.GET.getlist('user_name')
        access_level = request.GET.get('access_level')
        result = collection2.update_many({'User Name': {'$in': user_names}}, {'$set': {'Access Level': access_level}})
        if result.modified_count > 0:
            return JsonResponse({'message': f"Access level updated for {result.modified_count} users"})
        else:
            return JsonResponse({'message': f"No users were found"})
