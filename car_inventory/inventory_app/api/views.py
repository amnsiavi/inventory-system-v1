from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,HTTP_401_UNAUTHORIZED,
    HTTP_405_METHOD_NOT_ALLOWED
    
)
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import (
    generics, mixins
)
import qrcode

# Models and Serializers
from inventory_app.models import CarInventory
from inventory_app.api.serializers import CarInventorySerializer




METHODS = {
    'post':'post'.upper(),
    'get':'get'.upper(),
    'delete':'delete'.upper(),
    'put':'put'.upper(),
    'patch':'patch'.upper()
}

GET_ONLY = [METHODS['get']]
POST_ONLY = [METHODS['post']]

GET_AND_POST = [i.upper() for i in METHODS.keys() if i != 'delete' and i !='put' and i !='patch']

GET_DELETE_PUT_PATCH = [i.upper() for i in METHODS.keys() if i != 'post']


# Function Based Views

@api_view(GET_ONLY)
def get_inventory(request):
    
    try:
        username = request.headers.get('Authorization')

        if username == None:
            return Response({
                'error':'User Does Not Exsists',
               'msg':'Check header'
            },status=HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({
                'error':'Auth Failed',
                'msg':'User Does Not Exsist'
            },status=HTTP_401_UNAUTHORIZED)
        else:
            instance = CarInventory.objects.all()
            serializer = CarInventorySerializer(instance, many=True)
            return Response({
                'data':serializer.data,
                'status':'Sucessful'
            },status=HTTP_200_OK)
    except Exception as e:
        return Response({
            'status':'Failed',
            'errors':str(e)
        },status=HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(GET_DELETE_PUT_PATCH)
def get_car(request,pk):
    
    try:
        username = request.headers.get('Authorization')
        if username == None:
            return Response({
                'status':'Auth Failed',
                'msg':'Provide Header Authorization'
            },status=HTTP_401_UNAUTHORIZED)
        if request.method == 'get'.upper():
            user = User.objects.filter(username=username).first()
            if not user:
                return Response({
                    'status':'Auth Failed',
                    'msg':'User Does Not Exsist'
                },status=HTTP_401_UNAUTHORIZED)
            car = CarInventory.objects.get(pk=pk)
            serializer = CarInventorySerializer(car)
            return Response({
                'status':'Sucessful',
                'data':serializer.data
            },status=HTTP_200_OK)
        elif request.method == 'delete'.upper():
            user = User.objects.filter(username=username).first()
            if not user:
                return Response({
                    'error':'User Does Not Exsists',
                    'msg':'Check header'
                },status=HTTP_401_UNAUTHORIZED)
            else:
                is_admin = user.is_superuser
                if not is_admin:
                    return Response({
                        'msg':'Not Allowed'
                    },status=HTTP_401_UNAUTHORIZED)
                else:
                    car = CarInventory.objects.get(pk=pk)
                    car.delete()
                    return Response({
                        'status':'Sucess',
                        'msg':'User Deleted'
                    },status=HTTP_200_OK)
        elif request.method == 'put'.upper():
            user = User.objects.filter(username=username).first()
            if not user:
                return Response({
                    'error':'Auth Failed',
                    'msg':'User Does Not Exsist'
                },status=HTTP_401_UNAUTHORIZED)
            is_admin = user.is_superuser
            if is_admin:
                if len(request.data) == 0:
                    return Response({
                        'status':'Failed',
                        'errors':'Recieved Empty Object'
                    },status=HTTP_400_BAD_REQUEST)
                instance = CarInventory.objects.get(pk=pk)
                serializer = CarInventorySerializer(instance,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status':'Updated Sucessfully',
                        'data':serializer.data
                    },status=HTTP_200_OK)
                else:
                    return Response({
                        'status':'Failed',
                        'errors':serializer.errors
                    },status=HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status':'Failed',
                    'errors':'User Not Allowed'
                },status=HTTP_401_UNAUTHORIZED)
        elif request.method == 'patch'.upper():
            user = User.objects.filter(username=username).first()
            if not user:
                return Response({
                    'error':'Auth Failed',
                    'msg':'User Does Not Exsist'
                },status=HTTP_401_UNAUTHORIZED)
            is_admin = user.is_superuser
            if is_admin:
                if len(request.data) == 0:
                    return Response({
                        'status':'Failed',
                        'errors':'Recieved Empty Objects'
                    },status=HTTP_400_BAD_REQUEST)
                instance = CarInventory.objects.get(pk=pk)
                serializer = CarInventorySerializer(instance,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status':'Sucessful',
                        'data':serializer.data
                    },status=HTTP_200_OK)
                else:
                    return Response({
                        'status':'Failed'
                    },status=HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status':'Failed',
                    'errors':'User Not Allowed'
                },status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status':'Operation Failed'
            },status=HTTP_405_METHOD_NOT_ALLOWED)
    except ValidationError as ve:
        return Response({
            'status':'Operation Failed',
            'errors':ve.detail
        })
    except Exception as e:
        return Response({
            'status':'Failed',
            'errors':str(e)
        },status=HTTP_500_INTERNAL_SERVER_ERROR)


#Class Base Views


class CreateItem(
    generics.GenericAPIView,
    mixins.CreateModelMixin
):
    queryset = CarInventory.objects.all()
    serializer_class = CarInventorySerializer

    def post(self, request, *args, **kwargs):

        try:
            if len(request.data) == 0:
                return Response({
                    'status':'Failed',
                    'errors':'Recieved Empty Object'
                },status=HTTP_400_BAD_REQUEST)
            
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data':serializer.data,
                    'status':'Sucess'
                },status=HTTP_200_OK)
            else:
                return Response({
                    'status':'Failed',
                    'errors':serializer.errors
                },status=HTTP_400_BAD_REQUEST)

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
        


