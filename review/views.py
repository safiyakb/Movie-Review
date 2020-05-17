from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.
def home(request):
    allmovies = Movie.objects.all()

    context = {
        "movies": allmovies,
    }
   
    return render(request,'review/index.html',context)
#details page
def detail(request,id):
    movie = Movie.objects.get(id=id)
    context = {
        "movie":movie
    }
    return render(request,'review/details.html',context)

#add movies to database
def add_movies(request):
    if request.method == "POST":
        form = MovieForm(request.POST or None)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("review:home")
    else:
        form = MovieForm()
    return render(request,'review/addmovies.html',{'form':form, "controller":"Add Movies"})

#Edit movie
def edit_movies(request,id):
    movie = Movie.objects.get(id=id)

    if request.method == "POST":
        form = MovieForm(request.POST or None, instance = movie)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("review:detail", id)
    else:
        form = MovieForm(instance = movie)
    return render(request,'review/addmovies.html',{'form':form, "controller":"Edit Movies"})

#delete Movie
def delete_movies(request,id):
    movie = Movie.objects.get(id=id)
    movie.delete()
    return redirect("review:home")

