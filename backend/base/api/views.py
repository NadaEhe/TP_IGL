from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from base.models import User
from .serializers import userSerializer,registrationSerializer
from rest_framework.generics import UpdateAPIView
from django.core.mail import send_mail
from random import randint
from google.auth import jwt as gjwt
from google.auth import jwt

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['given_name'] = user.given_name
        token['family_name'] = user.family_name
        token['email'] = user.email
        token['address'] = user.address
        token['picture'] = user.picture.url
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/authApi/token',
        '/authApi/token/refresh',
    ]
    return Response(routes)


@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = userSerializer(users, many = True)
    return Response(serializer.data)    
@api_view(['POST'])
def getUserbyEmail(request):
    user = User.objects.get(email=request.data['email'])
    serializer = userSerializer(user, many = False)
    return Response(serializer.data)    

@api_view(['POST'])
def registrationView(request):
        serializer = registrationSerializer(data=request.data)
        
        data = {}
        if serializer.is_valid() :
            user = serializer.save()
            data['response'] = "Successfully registered new user."
            data['email'] = user.email
            data['name'] = user.name
        else:
            
            print('serializer not valid')   
            print(serializer.errors)
 
        
        return Response(data)

 

@api_view(['POST'])
def login(request):
    token = request.headers.get('Authorization')  
    id_token = token.rsplit("Bearer ")[1]
    
    try:
        claims = gjwt.decode(id_token, verify=False)
        token_valide= True
        user_data= {
            "given_name":claims["given_name"],
         "family_name":claims["family_name"],
        "email":claims["email"],
        "picture":claims["picture"],
       
        "name":claims["name"],
        }    
    except User.DoesNotExist:
        return Response({'detail':'token not valid'},status=status.HTTP_404_NOT_FOUND)

    user=userSerializer(data=user_data)         
    test=User.objects.filter(email=user_data["email"]).first()

    if token_valide:
        if not test:
            if user.is_valid():
                user.save()
                return Response({
                    'token':jwt.encode(user_data,"secret",algorithm="HS256"),
                    #'status':"200_signup",
                    
                },  status=status.HTTP_200_OK

                )
            else:return Response('email and username are not identical')
        else: return Response({'token':jwt.encode(user_data,"secret",algorithm="HS256")},  
         #'status':"200_signup",
         status=status.HTTP_200_OK) 
    else:return Response(status=status.HTTP_404_NOT_FOUND)



