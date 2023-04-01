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
import datetime
from django.contrib.auth.decorators import login_required
#testin
# from .serializers import HeroSerializer
# from .models import Hero
from django.views.decorators.csrf import csrf_exempt
import bcrypt
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
# @user_passes_test(lambda user: user.is_superuser)
def Users(request):
    if request.method == "GET":
        cursor = collection2.find()
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        print("nJson Data:", json_data)
        return JsonResponse(json_data, safe=False)
    
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        last_login_str = body["Last Login"]
        last_login = datetime.datetime.fromisoformat(last_login_str)
        password = body["Password"].encode("utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        newuser = {
            "User Name": body["User Name"],
            "Password": hashed_password.decode("utf-8"),
            "Access Level": body["Access Level"],
            "First Name": body["First Name"],
            "Surname": body["Surname"],
            "Email": body["Email"],
            "Last Login": last_login,
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
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user_ids = data.get("user_ids", [])
            access_level = data.get("access_level")
            if not user_ids:
                return JsonResponse({"message": "Please provide at least one user ID."})
            object_ids = [ObjectId(user_id) for user_id in user_ids]
            result = collection2.update_many(
                {"_id": {"$in": object_ids}}, {"$set": {"Access Level": access_level}}
            )
            if result.modified_count > 0:
                return JsonResponse(
                    {"message": f"Access level updated for {result.modified_count} users"}
                )
            else:
                return JsonResponse({"message": f"No users were found"})
        except:
            return JsonResponse({"message": "Invalid payload format."})
