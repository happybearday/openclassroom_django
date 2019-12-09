from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import datetime
from .models import Album, Artist, Contact, Booking
from django.db.models import Q
from django.template import loader

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def create_artist( artist_names ):
    for i in artist_names:
        Artist.objects.create(name = i)

def create_album( albums_list ):
    for curr_album_dict in albums_list:

        curr_album = Album.objects.create( title = curr_album_dict["title"])
        list_artists = [ Artist.objects.filter(name = curr_artist_name)[0]  for curr_artist_name in curr_album_dict["artists"]]
        curr_album.artists.add(*list_artists)
        curr_album.save()


def init_db(request):
    #Album.objects.all().delete()
    #Artist.objects.all().delete()
    #Contact.objects.all().delete()
    #Booking.objects.all().delete()
    ARTISTS = ['Francis Cabrel', 'Elijay', 'Rosana', 'María Dolores Pradera']

    ALBUMS = [
        {'title': 'Sarbacane', 'artists': ['Francis Cabrel']},
        {'title': 'La Dalle', 'artists': ['Elijay']},
        {'title': 'Luna Nueva', 'artists': ['Rosana', 'María Dolores Pradera']}
    ]

    #create_artist( ARTISTS )
    #create_album( ALBUMS )
    return HttpResponse("Ok")



def index(request):

    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {
        "albums" : albums
    }
    template = loader.get_template("store/index.html")
    return HttpResponse(template.render(context, request=request))


def create_pagination(albums_list, request, nb_elems = 3):
    
    paginator = Paginator(albums_list, nb_elems)
    albums = paginator.page(1)

    if "page" in request.GET:
        page = request.GET["page"]
        try :
            albums = paginator.page(page)
        except PageNotAnInteger:
            albums = paginator.page(1)
        except EmptyPage:
            albums = paginator.page(paginator.num_pages)
    return albums

def listing(request):
    albums_list = Album.objects.filter(available=True)
    
    albums = create_pagination(albums_list,request = request, nb_elems = 3)

    context = {
        "albums" : albums,
        "paginate" : True
    }
    template = loader.get_template("store/listing.html")
    return HttpResponse(template.render(context, request=request))

def detail(request, album_id):
    #album = Album.objects.get(pk = album_id)
    album = get_object_or_404(Album, pk = album_id )
   
    artists_name = ", ".join([curr_artist.name for curr_artist in album.artists.all()] )
    
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture}
    template = loader.get_template("store/detail.html")
    return HttpResponse(template.render(context, request=request))


def search(request):
    if "query" not in request.GET:
        albums_list = Album.objects.all()
        albums = create_pagination(albums_list,request=request, nb_elems = 3)

        context = {
            "albums" : albums,
            "list_title" : "Aucun parametre de recherche",
            "paginate" : True
        }

    else:
        query = request.GET["query"]
        albums_list = Album.objects.filter(Q(title__icontains = query) | Q(artists__name__icontains = query)).distinct()
        albums = create_pagination(albums_list,request=request, nb_elems = 3)
        context = {
            "albums" : albums,
            "list_title" : f"Résultat de votre recherche : '{query}'",
            "paginate" : True
        }

    template = loader.get_template("store/search.html")
    return HttpResponse(template.render(context, request=request))
