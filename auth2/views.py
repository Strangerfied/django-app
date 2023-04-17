import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import json
from bson.json_util import dumps
import pymongo
from django.http import HttpResponse
from datetime import datetime

@csrf_exempt
def login(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))
        username = body.get("username")
        password = body.get("password")
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest().upper()
        print(hashed_password)
        #client = pymongo.MongoClient("mongodb+srv://" + username + ":" + hashed_password + "@cluster1.syijvpg.mongodb.net/test?retryWrites=true&w=majority&tls=true")
        client = pymongo.MongoClient("mongodb+srv://admin2:poolcool@cluster1.syijvpg.mongodb.net/?retryWrites=true&w=majority&tls=true")
        print(client)
        db = client['eduClimateAnalysis']
        users = db['users']
        user = users.find_one({'User Name': username, 'Password': hashed_password})
        if user:
            users.update_one({'User Name': username, 'Password': hashed_password}, {'$set': {'Last Login': "New Login"}})
            # Set client connection string to the authenticated user's username and password
            request.session['mongo_client_uri'] = "mongodb+srv://" + username + ":" + hashed_password + "@cluster1.syijvpg.mongodb.net/test?retryWrites=true&w=majority&tls=true"
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method LOGIN'})

#tes againt final
def logout(request):
    request.session.clear()
    return HttpResponse("User logged out")
# Create your views here

