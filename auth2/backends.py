from pymongo import MongoClient
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class MongoDBBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        users = db['users']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = users.find_one({'username': username, 'password': hashed_password})
        if user:
            # Create a Django User object for the authenticated user
            user_obj, created = User.objects.get_or_create(username=username)
            return user_obj

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

