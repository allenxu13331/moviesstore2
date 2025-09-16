from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('top-comments/', views.top_comments, name='movies.top_comments'),  # ADD THIS LINE
    path('hide/<int:id>/', views.hide_movie, name='movies.hide_movie'),
    path('unhide/<int:id>/', views.unhide_movie, name='movies.unhide_movie'),
    path('hidden/', views.hidden_list, name='movies.hidden_list'),
]
