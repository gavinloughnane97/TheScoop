from django.db import models


class Team(models.Model):
    team_id = models.CharField(max_length=20, primary_key=True)
    team_num_id = models.IntegerField()
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

class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    game_date = models.DateField(auto_now=False, null=True)
    game_type = models.CharField(max_length=1)
    away_team = models.ForeignKey(Team, related_name='game_away_team_id', on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='game_home_team_id', on_delete=models.CASCADE)
    doubleheader = models.CharField(max_length=1)
    game_num = models.IntegerField()
    home_probable_pitcher = models.CharField(max_length=40, null=True)
    away_probable_pitcher = models.CharField(max_length=40, null=True)
    home_pitcher_note = models.TextField()
    away_pitcher_note = models.TextField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    venue_id = models.IntegerField()
    venue_name = models.CharField(max_length=40)
    winning_team = models.ForeignKey(Team, related_name='winning_team_id', on_delete=models.CASCADE)
    losing_team = models.ForeignKey(Team, related_name='losing_team_id', on_delete=models.CASCADE)
    winning_pitcher = models.CharField(max_length=40, null=True)
    losing_pitcher = models.CharField(max_length=40, null=True)
    save_pitcher = models.CharField(max_length=40, null=True)
    summary = models.TextField()

