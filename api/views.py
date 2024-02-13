from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import firebase_admin

from firebase_admin import auth , credentials

# Create your views here.

# firebase_credentials=credentials.Certificate({
#   "type": "service_account",
#   "project_id": "fir-project-ec62e",
#   "private_key_id": "d3d94da53203370ca8a34145f00b7a2efbae4e3e",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC10yqaRPJmzpsB\nutHV/Wc9aWPxzuoaw6A2nzItOchCWXeHDdE2252NG7m4ndNj1M5tU6fK31i/uTR+\nxxNjEjoZnZj2L8eOmoWh4XQab2elcEooSDu66nNzc0UW/3lB7TYdO5/6xJn9Bgs+\n+IgiLt+NSRS8cKI1J8dAvI0ZJ8kZE/FgmEwjbHW3UB9oHjlIvmRebzdI9XKNd5VU\nPmrH8g2dJXZLrmGMSqts3De6Lypn1Nv2dovkk5cq1yMJYQEp3L89XVT4q5iQ+UR3\nfMc/J0HDsLKwRFUj6HHV5jupvnKWXlGGLcjhzYQaj/kNfJTgJvQCl0emHePTf+GD\ngnBjCRXFAgMBAAECggEABJKeKnly7GrrX43m/T4J32WKGzwwrxdaV9Y3KflJ549F\nSOrsEbFQhrxFaEFlbFZYIFp4U0suZHUVhjMJVc9RAyK9tl8UMKNKRTx8tW61w/PX\n+ERuyiAYYu4pkXYjLXd4La6H1nyzAbfGY5LzQp+1UzAc9yQmImh7jmMKOJwKn5iK\nz3T+Yxknl+ddaOT9F4Hg4jIFlcoxHYR2aQtn+B5JTbbN1FH5Rmvw79XEqjoe3qIw\n0JtAYLWY8FEZz8t78VC9VHOonIY6SOG3m1FSwSQ1WUI1YZE4RhtGFtHtkE8nrYW0\nGD1EKKP10QFkUhGD8/0GDh1ML6TBUMShI2/+OhYm6QKBgQDZpvJgYARKQ9QyNfH5\nqdeQ1wFMlis0ViEj/SSJlUqlAOb1D4sjNr0yyCeePodYqPyA6diNOGlLPXoeStpi\ndjraLHqRwDkOWA7uofLDVxAUE8Y4P9MmG6oVSxYQOQihstH0DtumLGk/YidL1c3f\n2pUsU/lN8iy1D7An0SZhtVPXaQKBgQDV3EE9ojahmTmdsQafv4GsQFzng2vg3rXZ\n/uB12p7M6LteL7HwXbmlzsLsc4nuSQC64S+V0/YpyXyQN7IEV+DNpbzBTWXNk3aT\nO4Ok/k/Ez7wpgieYOqRwDhZc4/1QNkVnYqZxikIvttGqnQiazmzhTTgIlGqq7YhM\n9zGtL0g7/QKBgHgBo+xdpJ/qDErvEY9OBUyYL+AxgHrn7nfwcL/nb/PQrod6XYY5\n/VHNqIKJCYlqC2dtCHi9HNleeUHQld7qP4LiOWa5rPvqs7kB1F++VmArkwSatGpz\noHEDKJQjTk4R0c+WjadvH0zSasZWiaAe3ldFqdU/bUUb9E3P9TC0kRjZAoGAboV2\nXfDQBPGX2gvbnYEt9aQJn0fG356ZIoDa5W1HNiRseH9zmQIG6E6TY/lN5gxqSSoJ\nGohBJlVPf4SZBi+YKQ8nHkruerBjzjEqloErHk4xMs5lwgFEa/iLzBOzHNn/Qi+0\nTuchz2DOuDqRcNePY1wxwhVZjt5U21nAnXza+s0CgYBRfl9v5XoBj4oNVKev2xf4\n/B9d4AjtpcSjQ55ORU4EhC24cppy8nZviZSgj7NQXmp/IV3ICWZzfJx5lxnX1Ti0\nZkMAR/rtWqnutsjmejsl+Qh6R15dPNCe2Zjto2gx7xE2HsKhps5zrRj+Ye9YNxg9\n8bnsvefnuwPy/gbzwnsVQw==\n-----END PRIVATE KEY-----\n",
#   "client_email": "firebase-adminsdk-e9i2c@fir-project-ec62e.iam.gserviceaccount.com",
#   "client_id": "100430793027946226733",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-e9i2c%40fir-project-ec62e.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# })
firebase_credentials=credentials.Certificate('./api/firebase_credentials.json')
firebase_admin.initialize_app(firebase_credentials)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    @permission_classes([AllowAny])
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def getRoutes(request):
    routes={
        "user":"true"

    }
    return Response(routes)

@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request,*args, **kwargs):
    hashedPassword=make_password(request.data['password'])
    request.data['password']=hashedPassword
    print('entered',hashedPassword)

    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print('user created',serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({'message': 'User creation endpoint'}, status=status.HTTP_200_OK)
    
    # user=User.objects.create_user(request.data)
    # print('user is ',user)
    # return Response({'message': 'User creation endpoint'}, status=status.HTTP_200_OK)



# def decode_firebase_access_token(token):
#     try:
#         decoded_token=auth.verify_id_token(token)
#         return decoded_token
#     except auth.InvalidIdTokenError as e:
#         print("Invalid token: ",e)
#         return None
#     except Exception as e:
#         print("Error decoding Token :",e)
#         return None
    
# token=''
# @api_view(['POST','GET'])
# @permission_classes([AllowAny])
# def registerUser(request):
#     print('in register',request)
#     routes={
# "register":"routes"
#     }
    
#     return Response(routes)
# decoded_token = decode_firebase_access_token(token)
# if decoded_token:
#     print("Token decoded successfully.")
#     print("User ID:", decoded_token.get('uid'))
#     # Access other claims as needed
# else:
#     print("Failed to decode token.")