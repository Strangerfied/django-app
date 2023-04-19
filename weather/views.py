from bson import json_util
from django.http import HttpResponse
from django.http import JsonResponse
import json
from bson.json_util import dumps
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
import pymongo
from django.views.decorators.csrf import csrf_exempt
import ssl
from django.contrib.auth.decorators import login_required
from django.http import request
#Create your views here.

#testin

#client = pymongo.MongoClient(
 #  "mongodb+srv://admin2:poolcool@cluster1.syijvpg.mongodb.net/?retryWrites=true&w=majority&tls=true"
#)

#client = pymongo.MongoClient(request.session['mongo_client_uri'])


#dbname = client["eduClimateAnalysis"]

#collection = dbname["climateData"]
#test aain
#@csrf_exempt
    #if request.method == "GET":
     #  
      #  # Check if user is authenticated as manager or admin
       # if not request.user.is_authenticated or not (
       #     request.user.is_staff or request.user.is_superuser
       # ):
       #     return JsonResponse({"error": "Unauthorized access."}, status=401)
       # cursor = collection.find().limit(1)
       # list_cur = list(cursor)
       # json_data = dumps(list_cur)
       # print("nJson Data:", json_data)
       # return JsonResponse(json_data, safe=False)"""

def ConnectionTest(request):
    client = pymongo.MongoClient(request.session['mongo_client_uri'])


    dbname = client["eduClimateAnalysis"]

    collection = dbname["climateData"]

    try:
        collection.find_one()
        result = {"status": "success", "message": "MongoDB connection successful!"}
    except Exception as e:
        result = {"status": "error", "message": f"Failed to connect to MongoDB: {e}"}
    return JsonResponse(result)

@csrf_exempt
def Weather(request):
    client = pymongo.MongoClient(request.session['mongoclient'])


    dbname = client["eduClimateAnalysis"]

    collection = dbname["climateData"]

    if 'mongoclient' in request.session and request.session['mongoclient'] is not None:
        if request.method == "PATCH":
            try:
                data = json.loads(request.body)
                print(data)
                document_ids = data.get("_id", [])
                print(document_ids)
                result = []
                for document_id in document_ids:
                    obj_id = ObjectId(document_id)
                    print(obj_id)

                    temp = collection.find_one(
                        {"_id": obj_id, "Temperature (°C)": {"$exists": True}}
                    )

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
            except Exception as exception:
                return JsonResponse(
                    {"status": "error", "message": f"An exception occurred: {str(exception)}"}
                )
        if request.method == "PUT":
            body = json.loads(request.body.decode("utf-8"))
            station_name = body.get("Device Name", "")
            date_time_str = body.get("Time", "")

            try:
                date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            except ValueError:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Invalid format",
                    }
                )

            result = collection.find_one(
                {"Time": date_time_obj, "Device Name": station_name},
                {
                    "Temperature (°C)": 1,
                    "Atmospheric Pressure (kPa)": 1,
                    "Solar Radiation (W/m2)": 1,
                    "Precipitation mm/h": 1,
                    "_id": 0,
                },
                hint=[("Time", 1)],
            )

            if result:
                return JsonResponse({"status": "success", "data": result})
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "No data found for the specified station and date/time",
                    }
                )
        if request.method == "GET":
            batch_size = int(request.GET.get('batch_size', 10))
            page_number = int(request.GET.get('page_number', 1))

            skip = (page_number - 1) * batch_size

            documents = collection.find().skip(skip).limit(batch_size)

            document_list = []
            for doc in documents:
                doc['_id'] = str(doc['_id'])
                document_list.append(doc)

            return JsonResponse(document_list, safe=False)
        if request.method == "GET1":
            try:
                temps = []
                num_docs_per_batch = 5
                for temp in collection.find().batch_size(num_docs_per_batch).limit(50):
                    temps.append(
                        {
                            "_id": str(temp["_id"]),
                            "Temperature (°C)": temp["Temperature (°C)"],
                        }
                    )
                    if len(temps) == num_docs_per_batch:
                        print(f"Processed {num_docs_per_batch} documents in this batch")
                        num_docs_per_batch += 5

                return JsonResponse({"status": "success", "temperatures": temps})
            except:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "An error occurred while retrieving temperature records",
                    }
                )

        if request.method == "POST":
            body = json.loads(request.body)
            index_value = body.get('index_value')

            index_info = collection.index_information()
            if index_value not in index_info:
                collection.create_index(index_value)

            result = collection.find().hint(index_value).limit(10)
            json_data = json_util.dumps(result)
            return JsonResponse(json.loads(json_data), safe=False)

        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    else:
        return JsonResponse(
            {"status": "error", "message": "Please login to access this"}
        )
"""
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
@csrf_exempt
def IndexQuery(request):
    if request.method == "POST":
        # Get the index value from the JSON body of the request
        body = json.loads(request.body)
        index_value = body.get('index_value')

        index_info = collection.index_information()
        if index_value not in index_info:
            # Create an index on the specified field if it doesn't already exist
            collection.create_index(index_value)

        # Perform the query using the created index
        result = collection.find().hint(index_value).limit(10)
        # Serialize the result to JSON and return as a response
        json_data = json_util.dumps(result)
        return JsonResponse(json.loads(json_data), safe=False)

    # Return a 405 Method Not Allowed error if the request method is not POST
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)"""
