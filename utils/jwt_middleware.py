import jwt
from django.http import JsonResponse
from django.conf import settings

def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Token is missing or invalid"}, status=401)
        
        token = auth_header.split(" ")[1]
        try:
            # Decodificar el token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            request.user_id = payload.get("user_id")  # Agregar el user_id al request
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        
        return view_func(request, *args, **kwargs)
    return wrapper