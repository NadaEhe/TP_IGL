from django.http import response

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from .models import Annonce , Fav , Photo
from .serializers import AnnonceSerializer , FavSerializer , PhotoSerializer
from annonce import serializers
from .utils import updateAnnonce, getAnnonceDetail, deleteAnnonce, getAnnoncesList, createAnnonce , getAnnounceByName , createFavorites , getFavorites
from django.shortcuts import get_object_or_404
from rest_framework import filters , generics
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from base.models import User
# from django_filters import rest_framework as filters

import django_filters
from django.utils import timezone
from django.utils.dateparse import parse_datetime


# from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.


@api_view(['GET', 'POST'])
def getRoutes(request):

    routes = [
        {
            'Endpoint': '/annonces/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of annonces'
        },
        {
            'Endpoint': '/annonces/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single Annonce object'
        },
        {
            'Endpoint': '/search/keyword=name',

            'method': 'GET',
            'body': None,
            'description': 'Returns annonces by name '
        },
        {
            'Endpoint': '/annonces/create/',
            'method': 'POST',
            'body': {'body': "" , 'title': ""},
            'description': 'Creates new Annonce with data sent in post request'
        },
        {
            'Endpoint': '/annonces/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing Annonce with data sent in post request'
        },
        {
            'Endpoint': '/annonces/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting Annonce'
        },
        {
            'Endpoint': '/favorites/id/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of annonces'
        },
        {
            'Endpoint': '/favorites/',
            'method': 'POST',
            'body': None,
            'description': 'Returns an array of annonces'
        },
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
def getAnnonces(request):

    if request.method == 'GET':
        return getAnnoncesList(request)

    if request.method == 'POST':
        return createAnnonce(request)
    
@api_view(['POST', 'GET'])
def createFavoriteRequest(request):
    if request.method == 'POST':
        return createFavorites(request)
    
# @api_view(['GET'])
# def getFavoritesRequest(request):
#     if request.method == 'GET':
#         return getFavorites(request)
@api_view(['POST', 'GET'])
def getFavorites(request , user_id):

    favorites = Fav.objects.filter(user = user_id)
    serializer = FavSerializer(favorites, many=True)
    fav_data = serializer.data
    for fav in fav_data:
        annonce = Annonce.objects.get(id=fav['annonce'])
        fav['annonce'] = AnnonceSerializer(annonce).data

    return Response(fav_data , content_type='application/json' )

@api_view(['POST', 'GET'])
def getUserAnnonces(request , user_id):
    annonces = Annonce.objects.filter(author = user_id)
    serializer = AnnonceSerializer(annonces, many=True)
    annonce_data = serializer.data
    for item in annonce_data:
        for item2 in item['images']:
            item2["image"] = "http://127.0.0.1:8000" + item2["image"]


    return Response(annonce_data, content_type='application/json' )




@api_view(['GET', 'PUT', 'DELETE'])
def getAnnonce(request, pk):

    if request.method == 'GET':
        return getAnnonceDetail(request, pk)

    if request.method == 'PUT':
        return updateAnnonce(request, pk)

    if request.method == 'DELETE':
        return deleteAnnonce(request, pk)

@api_view(['GET', 'POST'])
def getAnnounceByNameView(request, name):

    return getAnnounceByName(request, name)


# class AnnonceFilter(filters.FilterSet):
#     created__gte = filters.DateTimeFilter(field_name='created', lookup_expr='gte')

#     class Meta:
#         model = Annonce
#         fields = ['created__gte']

class AnnonceDateFilter(django_filters.FilterSet):
    created__gte = django_filters.DateTimeFilter(field_name='created', method='filter_by_date_range')
    created__lte = django_filters.DateTimeFilter(field_name='created', method='filter_by_date_range')
    wilaya = django_filters.CharFilter(field_name='wilaya', lookup_expr='exact')
    commune = django_filters.CharFilter(field_name='commune', lookup_expr='exact')

    class Meta:
        model = Annonce
        fields = ['wilaya', 'commune']

    def filter_by_date_range(self, queryset, name, value):
        if not value:
            return queryset

        start_date = None
        end_date = None

        if self.data.get('created__gte'):
            start_date = parse_datetime(self.data['created__gte'])
        if self.data.get('created__lte'):
            end_date = parse_datetime(self.data['created__lte'])

        if start_date and end_date:
            return queryset.filter(created__gte=start_date, created__lte=end_date)

        if start_date:
            return queryset.filter(created__gte=start_date)

        if end_date:
            return queryset.filter(created__lte=end_date)

        return queryset



class AnnonceSearch(generics.ListAPIView):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]

    search_fields = ['^title' , "^description", "id"]
    filterset_fields = ["wilaya", "commune"]
    filterset_class = AnnonceDateFilter



    # def get(self, request, *args, **kwargs):
    #     print(request.GET)
    #     queryset = self.filter_queryset(self.queryset)
    #     print(queryset.query)
    #     return super().get(request, *args, **kwargs)


class AnnonceViewSet(ModelViewSet):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title' ,"^description", ]
    filterset_fields = [ 'wilaya',"created"]
    ordering = ('-created' , )
    pagination_class = PageNumberPagination

class Favorites(ModelViewSet):
    # permission_classes = [AllowAny]
    serializer_class = FavSerializer
    queryset = Fav.objects.all()


    # def get_queryset(self):
    #     return Fav.objects.filter(liker__fname ="dante" )   

    # DjangoFilterBackend



class WithImages(generics.ListAPIView):
    # permission_classes = [AllowAny]

    serializer_class = PhotoSerializer
    def get_queryset(self):
        return Photo.objects.all()
    


# http://127.0.0.1:8000/api/annonces/custom/?search=second&body=testing+df
# http://127.0.0.1:8000/api/annonces/custom/?search=second&created=2022-12-13T22:24:26.615288Z
# http://127.0.0.1:8000/api/annonces/custom/?search=second&created__get2022-12-13T00:00:00.000000Z