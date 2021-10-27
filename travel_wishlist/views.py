from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
# Create your views here.

def place_list(request): # this function will be called by django and given info about the request the user makes

    if request.method == 'POST': 
        # create new place
        form = NewPlaceForm(request.POST) # creating a new place form but from data on the page
        place = form.save() # save the form and creating a model object from the form
        if form.is_valid(): # validation db constraints
            place.save() # saves model to db
            return redirect('place_list') # reloading place list as response - reloads homepage

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # this is the other way to create a new form - brand new and send it to be rendered in html
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk) # get will get the object from the DB and return 0 or 1 items, pk is DB column
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    
    return redirect('place_list') # redirect to wishlist places
    # return redirect('places_visited') # redirect to places visited


def about(request):
    author = 'niko'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
