from django.http import JsonResponse
from django.contrib.auth.hashers import make_password , check_password
from .models import User
import json
import jwt
from django.conf import settings
from .serializer import UserSerializer
from utils.jwt_middleware import jwt_required

# Create your views here.
def register(request):
    if request.method == "POST":
        try:

            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            # Validate the data (you can add more validation as needed)
            if not username:
                return JsonResponse({"error": "Username is required"}, status=400)
            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)
            if not password:
                return JsonResponse({"error": "Password is required"}, status=400)
            
            # encrypt the password with bycrypt
            password = make_password(password)
            

            # Create a new user object
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")


            return JsonResponse({"token" : token}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


        # Perform registration logic here (e.g., save user to the database)
        
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            user = User.objects.get(username=username)
            if check_password(password, user.password):

                user = User.objects.get(username=username)
                token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")



                return JsonResponse({"token" : token}, status=200)
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@jwt_required
def get_user(request):
    if request.method == "GET":
            user_id = request.user_id
            user = User.objects.get(id = user_id)

            user_serializer = UserSerializer(user)
            user = user_serializer.data
            return JsonResponse({"user": user}, status=200)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)

@jwt_required
def get_user_by_id(request, user_id):
    if request.method == "GET":
        try:
            user = User.objects.get(id=user_id)
            user_serializer = UserSerializer(user)
            user = user_serializer.data
            return JsonResponse({"user": user}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@jwt_required
def update_user(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user_id = request.user_id
            user = User.objects.get(id = user_id)

            user.username = data.get("username")
            user.email = data.get("email")

            if data.get("password"):
                user.password = make_password(data.get("password"))
            else:
                user.password = None
            
            user.save()

            return JsonResponse({"message": "User updated successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@jwt_required
def delete_user(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            user_id = request.user_id
            user = User.objects.get(id = user_id)

            user.delete()

            return JsonResponse({"message": "User deleted successfully"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)