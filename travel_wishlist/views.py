from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def place_list(request): # this function will be called by django and given info about the request the user makes

    if request.method == 'POST': 
        # create new place
        form = NewPlaceForm(request.POST) # creating a new place form but from data on the page
        place = form.save(commit=False) # save the form and creating a model object from the form
        place.user = request.user
        if form.is_valid(): # validation db constraints
            place.save() # saves model to db
            return redirect('place_list') # reloading place list as response - reloads homepage

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # this is the other way to create a new form - brand new and send it to be rendered in html
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk) # get will get the object from the DB and return 0 or 1 items, pk is DB column
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user: # first check if user logged in is the correct user to update these visited statuses
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    
    return redirect('place_list') # redirect to wishlist places
    # return redirect('places_visited') # redirect to places visited

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # does this place belong to the current user
    if place.user != request.user:
        return HttpResponseForbidden()
    # is this a GET request (show data + form) or a POST request (update Place object)

    # if POST, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place) # make new tripreviewform object from data sent with http request, put in data user has sent, use that to update instance in db
        if form.is_valid(): # are all req'd forms filled in
            form.save()
            messages.info(request, 'Trip information updated!') # messages are way of showing temporary data to user
        else:
            messages.error(request, form.errors) # second item will be shown to user
        
        return redirect('place_details', place_pk=place_pk)
    
    # if GET, show Place info and form
    else:
        # if place is visited, show form; if place not visited, no form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


    return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


def about(request):
    author = 'niko'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
