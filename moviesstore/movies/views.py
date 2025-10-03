from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition, PetitionVote
from .forms import PetitionForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count  # ADD THIS IMPORT
from django.contrib.auth.models import User  # ADD THIS IMPORT
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})
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


def petitions(request):
    """List all petitions ordered by creation date (newest first)."""
    petitions = Petition.objects.select_related('created_by').order_by('-created_at')
    template_data = {
        'title': 'Petitions',
        'petitions': petitions,
    }
    return render(request, 'movies/petitions.html', {'template_data': template_data})

def petitions_list(request):
    """List all petitions ordered by creation date (newest first)."""
    petitions = Petition.objects.select_related('created_by').order_by('-created_at')
    template_data = {
        'title': 'Petitions',
        'petitions': petitions,
    }
    return render(request, 'movies/petitions_list.html', {'template_data': template_data})


@login_required
def petition_create(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            return redirect('movies.petitions_list')
    else:
        form = PetitionForm()
    template_data = {'title': 'Create Petition', 'form': form}
    return render(request, 'movies/petition_create.html', {'template_data': template_data})


@login_required
def petition_vote(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    # Expect POST with 'vote' = 'yes' or 'no'
    if request.method == 'POST' and request.POST.get('vote') in ['yes', 'no']:
        vote_value = True if request.POST.get('vote') == 'yes' else False
        # Create or update the user's vote
        pv, created = PetitionVote.objects.update_or_create(
            petition=petition, user=request.user, defaults={'vote': vote_value}
        )
    return redirect('movies.petitions_list')