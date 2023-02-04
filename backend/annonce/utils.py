from rest_framework import generics
from rest_framework.response import Response
from .models import Annonce , Photo , Fav
from .serializers import AnnonceSerializer , FavSerializer
from django.shortcuts import get_object_or_404
from rest_framework import filters
from base.models import User




def getAnnoncesList(request):
    notes = Annonce.objects.all().order_by('-created')
    # notes = Annonce.objects.prefetch_related('tracks')

    # images = Photo.objects.all()
    serializer = AnnonceSerializer(notes, many=True)
    return Response(serializer.data)

def getFavorites(request , user_id):
    print("heere")
    user = get_object_or_404(User, pk=user_id)

    favorites = Fav.objects.all(user = user)
    serializer = FavSerializer(favorites, many=True)
    fav_data = serializer.data
    for fav in fav_data:
        annonce = Annonce.objects.get(id=fav['annonce'])
        fav['annonce'] = AnnonceSerializer(annonce).data

    return Response(fav_data)

def createFavorites(request):
    data = request.data
    user = User.objects.get(id=data['user'])
    annonce = Annonce.objects.get(id=data['annonce'])
    fav = Fav.objects.create(user = user,annonce = annonce)
    serializer = FavSerializer(fav, many=False)
    return Response(serializer.data)




def getAnnonceDetail(request, pk):
    notes = Annonce.objects.get(id=pk)
    serializer = AnnonceSerializer(notes, many=False)
    fav_data = serializer.data
    for fav in fav_data['images']:
        fav["image"] = "http://127.0.0.1:8000" + fav["image"]
    return Response(serializer.data)


def createAnnonce(request):
    data = request.data
    note = Annonce.objects.create(
        body=data['body'],
        title=data['title']

    )
    image = Photo.objects.create(
        owner = note,
        desc = data['desc']
    )
    serializer = AnnonceSerializer(note, many=False)
    return Response(serializer.data)

def updateAnnonce(request, pk):
    data = request.data
    note = Annonce.objects.get(id=pk)
    serializer = AnnonceSerializer(instance=note, data=data)

    if serializer.is_valid():
        serializer.save()

    return serializer.data


def deleteAnnonce(request, pk):
    note = Annonce.objects.get(id=pk)
    note.delete()
    return Response('Note was deleted!')

def getAnnounceByName(request , name):
    annonces = Annonce.objects.filter(title='third')
    print(annonces)
    # annonces = Annonce.objects.get(title=name)
    serializer = AnnonceSerializer(annonces, many=True)
    return Response(serializer.data)
# >>> cheese_blog = Blog.objects.get(name="Cheddar Talk")

class AnnonceSearch(generics.ListAPIView):
    # permission_classes = [AllowAny]
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Annonce, title=item)

    def get_queryset(self):
        return Annonce.objects.all()
