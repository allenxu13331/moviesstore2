from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Count  # ADD THIS IMPORT
from django.contrib.auth.models import User  # ADD THIS IMPORT
from .models import Movie, Review, HiddenMovie  # Add HiddenMovie import

@login_required
def hide_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    HiddenMovie.objects.get_or_create(user=request.user, movie=movie)
    return redirect('movies.index')

@login_required
def unhide_movie(request, id):
    hidden = HiddenMovie.objects.filter(user=request.user, movie_id=id)
    hidden.delete()
    return redirect('movies.hidden_list')

@login_required
def hidden_list(request):
    hidden_movies = Movie.objects.filter(hiddenmovie__user=request.user)
    template_data = {
        'title': 'Hidden Movies',
        'movies': hidden_movies,
    }
    return render(request, 'movies/hidden_list.html', {'template_data': template_data})

def index(request):
    search_term = request.GET.get('search')
    movies = Movie.objects.all()
    if request.user.is_authenticated:
        hidden_ids = HiddenMovie.objects.filter(user=request.user).values_list('movie_id', flat=True)
        movies = movies.exclude(id__in=hidden_ids)
    if search_term:
        movies = movies.filter(name__icontains=search_term)
    template_data = {
        'title': 'Movies',
        'movies': movies,
    }
    return render(request, 'movies/index.html', {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

# ADD THIS NEW FUNCTION
def top_comments(request):
    """
    View to display top comments and most active users
    """
    # Get the most recent reviews with user and movie data
    top_reviews = Review.objects.select_related('user', 'movie').order_by('-date')[:25]
    
    # Get users with the most reviews (top commenters)
    top_commenters = User.objects.annotate(
        review_count=Count('review')
    ).order_by('-review_count')[:10]
    
    template_data = {}
    template_data['title'] = 'Top Comments'
    template_data['reviews'] = top_reviews
    template_data['top_commenters'] = top_commenters
    
    return render(request, 'movies/top_comments.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)