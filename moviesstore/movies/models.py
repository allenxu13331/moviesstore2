from django.db import models
from django.contrib.auth.models import User
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
class Petition(models.Model):
    """A user-submitted petition requesting that an admin add a movie to the catalog."""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

    def votes_summary(self):
        """Return a dict with yes/no counts and total."""
        yes = self.votes.filter(vote=True).count()
        no = self.votes.filter(vote=False).count()
        total = yes + no
        percent_yes = (yes / total * 100) if total > 0 else 0
        return {"yes": yes, "no": no, "total": total, "percent_yes": percent_yes}

class PetitionVote(models.Model):
    """A vote (yes/no) by a user on a petition.

    Each user may only vote once per petition (enforced by unique_together).
    """
    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField()  # True means 'yes' (include), False means 'no'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('petition', 'user'),)

    def __str__(self):
        return f"{self.user.username} -> {self.petition.title} : {'YES' if self.vote else 'NO'}"
# Create your models here.
