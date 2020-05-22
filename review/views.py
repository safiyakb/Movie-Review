from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg
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
    reviews = Review.objects.filter(movie=id).order_by("-review")
    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average,2)
    context = {
        "movie":movie,
        "reviews":reviews,
        "average":average
    }
    return render(request,'review/details.html',context)

#add movies to database
def add_movies(request):
    #check if user is authenticated
    if request.user.is_authenticated:
        #check if the user is superuser
        if request.user.is_superuser:
            if request.method == "POST":
                form = MovieForm(request.POST or None)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("review:home")
            else:
                form = MovieForm()
            return render(request,'review/addmovies.html',{'form':form, "controller":"Add Movies"})
        #if the user is not superuser 
        else:
            return redirect("review:home")

    #if the user is not logged in
    return redirect("accounts:login")


#Edit movie
def edit_movies(request,id):
    if request.user.is_authenticated:
        #check if the user is superuser
        if request.user.is_superuser:
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
        else:
            return redirect("review:home")

    #if the user is not logged in
    return redirect("accounts:login")

#delete Movie
def delete_movies(request,id):
    if request.user.is_authenticated:
        #check if the user is superuser
        if request.user.is_superuser:
            movie = Movie.objects.get(id=id)
            movie.delete()
            return redirect("review:home")

        else:
            return redirect("review:home")

    #if the user is not logged in
    return redirect("accounts:login")


#add review
def add_review(request,id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid:
                data = form.save(commit = False)
                data.review = request.POST["review"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("review:detail",id)
        else:
            return render(request,"review/details.html", {"form":form})

    else:
        return redirect("accounts:login")

#edit review
def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        review = Review.objects.get(id=review_id)

        #check if the review is given by the user that has logged in
        if request.user == review.user:
            #allow the user to edit his review
            if request.method == "POST":
                form = ReviewForm(request.POST, instance = review)
                if form.is_valid():
                    data = form.save(commit = False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Rating out of range"
                        return render(request,"review/edit_review.html",{"error":error, "form":form})
                    else:
                        data.save()
                        return redirect("review:detail",movie_id)
            else:
                form = ReviewForm(instance = review)
                return render(request,"review/edit_review.html",{"form":form})
        else:
            return redirect("review:detail",movie_id)
    else:
        return redirect("accounts:login")

#delete review
def delete_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=movie_id)
        review = Review.objects.get(id=review_id)

        #check if the review is given by the user that has logged in
        if request.user == review.user:
            #allow the user to delete his review
            review.delete()
        return redirect("review:detail",movie_id)
    else:
        return redirect("accounts:login")