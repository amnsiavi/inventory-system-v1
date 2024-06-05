from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_404_NOT_FOUND
)

#Model
from django.contrib.auth.models import User
from Auth.api.serializers import AuthSerializer

@api_view(['GET'])
def get_all_users(request):

    try:
        
        if request.method == 'GET':
            instance = User.objects.all()
            serializer = AuthSerializer(instance, many=True)
            return Response({
                'status':'Sucess',
                'data':serializer.data
            },status=HTTP_200_OK)
        else:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({
            'status':'Failed',
            'errors':str(e)
        },status=HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def create_user(request):
    
    try:
        if request.method == 'POST':
            
            if len(request.data) == 0:
                return Response({
                    'status':'Failed',
                    'errors':'Recieved Empty Object'
                },status=HTTP_400_BAD_REQUEST)
            
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            is_admin = request.data.get('is_superuser')

            if User.objects.filter(username=username).exists():
                return Response({
                    'status':'Failed',
                    'errors':'Username Already Exists'
                },status=HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({
                    'status':'Failed',
                    'errors':'Email Already Exists'
                },status=HTTP_400_BAD_REQUEST)

            if is_admin:
                user = User.objects.create_superuser(
                    username=username,email=email,
                    password=password
                )
                return Response({
                    'data':{
                        'username':user.username,
                        'email':user.email,
                        'is_superuser':user.is_superuser
                    },'msg':'Admin Created'
                })
            else:
                user = User.objects.create_user(
                    username=username, email=email,
                    password=password
                )
                return Response({
                  'data':{
                        'username':user.username,
                        'email':user.email,
                        'is_superuser':user.is_superuser
                    },'msg':'User Created'                    
                })
            


            
        else:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
    except ValidationError as ve:
        return Response({
            'status':'Failed',
            'errors':ve.detail
        },status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'status':'Failed',
            'errors':str(e)
        },status=HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET','DELETE'])
def get_user(request,pk):
    
    try:
        if request.method == 'GET':
            user =  User.objects.get(pk=pk)
            serializer = AuthSerializer(user)
            return Response({
                'data':serializer.data,
                'status':'Sucess'
            },status=HTTP_200_OK)
        
        elif request.method == 'DELETE':
            user = User.objects.filter(id=pk).first()

            if not user:
                return Response({
                    'errors':"User not found"
                },status=HTTP_404_NOT_FOUND)
            user.delete()
            return Response({
                'message':'User Deleted Sucessful'
            })
        else:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as e:
        return Response({
            'status':'Failed',
            'errors':str(e)
        },status=HTTP_500_INTERNAL_SERVER_ERROR)