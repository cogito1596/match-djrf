from django.db import models

# Create your models here.
class Match(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    current_score = models.IntegerField(default=0)
    wickets_fallen = models.IntegerField(default=0)
    overs_completed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Over(models.Model):
    match = models.ForeignKey(Match,related_name="overs",on_delete=models.CASCADE)
    over_number = models.PositiveIntegerField()
    
class Ball(models.Model):
    over = models.ForeignKey(Over,related_name="balls",on_delete=models.CASCADE)
    ball_number = models.PositiveIntegerField()
    runs = models.IntegerField()
    is_wicket = models.BooleanField(default=False)
    extras = models.IntegerField(default=0)