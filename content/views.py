from django.shortcuts import render
from .models import shows_collection , users
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer , RegisterSerializer , ShowSerializer
from django.contrib.auth import authenticate , login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from math import ceil
from bson.json_util import dumps
from urllib.parse import urlencode
# Create your views here.


def index(request):
    return HttpResponse("<h1>app is running</h1>")


# def show_list(request):
#     shows = shows_collection.find()

#      # Pagination parameters
#     page = int(request.GET.get('page', 1))
#     page_size = 15
#     total_items = shows_collection.count_documents({})
#     total_pages = ceil(total_items / page_size)

#     skip = (page - 1) * page_size
#     shows = shows_collection.find().skip(skip).limit(page_size)

#     serialized_shows = dumps(shows)

#     metadata = {
#         'page': page,
#         'page_size': page_size,
#         'total_items': total_items,
#         'total_pages': total_pages,
#     }

#     return Response({
#         'metadata': metadata,
#         'data': serialized_shows
#     }, content_type='application/json')


class User(APIView):
    def get(self,request):
        queryset = users.objects.all()


class LoginAPI(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                serializer = UserSerializer(user)
                token , _ = Token.objects.get_or_create(user=user)
                print(token, 'token')
                return Response({
                    "status" : "success",
                    "data" : {"token" : str(token) , "user" : serializer.data}
                })
            else:
                return Response({'error': 'Invalid email or password'}, status=404)
        except Exception as e :
            import traceback
            print(traceback.print_exc()) 
            return Response({'error' : e , 'status' : 'failed'})


class RegisterApi(APIView):
    def post(self , request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            print(data , 'data')
            if not serializer.is_valid():
                return Response({
                    "status" : "failed",
                    "data" : serializer.errors
                })
            else:
                # try:
                user_data = users.find({'email' : data['email']})
                print(user_data)
                if len(dumps(user_data)) > 2:
                    return Response({
                        "status" : "failed",
                        "data" : "User with this email already exists"
                    })
                else:
                    # username = serializer.data['username']
                    # password = serializer.data['password']
                    # age = serializer.data['age']
                    # user_obj = {
                    #     "username" : username,
                    #     "password" : password,
                    #     "age" : age
                    # }
                    # users.insert_one(user_obj)
                    serializer.save()
                    return Response({
                        "status" : "success",
                        "data" : "User saved successfully"
                    })

        except Exception as e :
            import traceback
            print(traceback.print_exc())
            return Response({'error' : e , 'status' : 'failed'})

class ContentApi(APIView):
    def get(self , request):
        try : 
            query = {}
            search = request.GET.get("search", None)
            content_type = request.GET.get("type", None)
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 15)) 
            if search:
                query["$or"] = [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"cast": {"$regex": search, "$options": "i"}}
                ]
            if content_type and content_type != 'all':
                query['type'] = content_type
            total_items = shows_collection.count_documents(query)
            total_pages = ceil(total_items / page_size)
            skip = (page - 1) * page_size

            shows = shows_collection.find(query).skip(skip).limit(page_size)
            serialized_shows = dumps(shows)
            next_page_url = None
            if page < total_pages:
                params = {
                    "page": page + 1,
                    "page_size": page_size,
                    "search": search,
                    "type": content_type,
                }
                base_url = request.build_absolute_uri(request.path)
                next_page_url = f"{base_url}?{urlencode({k: v for k, v in params.items() if v})}"

            previous_page_url = None
            if page > 1:
                params = {
                    "page": page - 1,
                    "page_size": page_size,
                    "search": search,
                    "type": content_type,
                }
                base_url = request.build_absolute_uri(request.path)
                previous_page_url = f"{base_url}?{urlencode({k: v for k, v in params.items() if v})}"

            metadata = {
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': page,
                'page_size': page_size,
                'next_page_url': next_page_url,
                'previous_page_url': previous_page_url,
            }

            return Response({
                'metadata': metadata,
                'data': serialized_shows
            }, content_type='application/json')
        except Exception as e:
            return Response({'error' , e})