from django.db import models


class Team(models.Model):
    team_id = models.CharField(max_length=20, primary_key=True)
    team_name = models.CharField(max_length=40)
    location = models.CharField(max_length=40)
    sport = models.CharField(max_length=40)
    image_path = models.CharField(max_length=40)

    def __str__(self):
        return self.team_id


class Matchup(models.Model):
    matchup_id = models.CharField(max_length=40, primary_key=True)
    home_team = models.ForeignKey(Team, related_name='home_team_id', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team_id', on_delete=models.CASCADE)
    matchup_title = models.CharField(max_length=120)
    time = models.DateTimeField(auto_now=False, null=True)


class Bet(models.Model):
    bet_id = models.BigAutoField(primary_key=True)
    matchup_id = models.ForeignKey(Matchup, on_delete=models.CASCADE)
    selected_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    bookmaker = models.CharField(max_length=40)
    bet_type = models.CharField(max_length=40)
    last_updated = models.DateTimeField(auto_now=False, null=True)
    price = models.IntegerField()
    version = models.IntegerField()
